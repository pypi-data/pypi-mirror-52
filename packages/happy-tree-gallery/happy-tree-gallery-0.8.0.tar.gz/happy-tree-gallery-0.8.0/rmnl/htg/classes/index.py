# -*- coding: utf8 -*-

import click
import datetime
import os
import peewee
import pickle
import warnings

from ..imaging import image_metadata
from ..models import Album
from ..models import Picture
from ..utils import abort
from ..utils import checksum
from ..utils import fatal_error
from ..utils import file_name_date
from ..utils import filter_image_files
from ..utils import parse_meta_file
from ..utils import title_and_date_from_dir_name


META_FIELDS = ["title", "start_date", "end_date", "description", "meta"]


class Index(object):

    new, processed, changed, unchanged, duplicates = 0, 0, 0, 0, 0
    checksums = []
    photos = []
    failed_meta_files = []

    def __init__(self, config=None):
        self.config = config

    def _meta_from_path(self, path):
        meta = {}
        meta_file = os.path.join(path, self.config.meta_file_name)
        if os.path.exists(meta_file):
            meta = parse_meta_file(meta_file)
            if meta is None:
                self.failed_meta_files.append(meta_file)
        return {} if meta is None else meta

    def _meta_from_dir_name(self, path, meta={}):
        if meta.get("title") and meta.get("start_date"):
            return meta
        title, start_date = title_and_date_from_dir_name(path, self.config.album_dir_pattern)
        if title and not meta.get("title", False):
            meta["title"] = title
        if start_date and not meta.get("start_date", False):
            meta["start_date"] = start_date
        return meta

    def _album_from_meta(self, path, meta):
        try:
            album = Album.get(album_path=path)
        except peewee.DoesNotExist:
            album = None
        if not meta or meta.get("album") is False:
            if album:
                album.delete_instance(recursive=True)
            return None
        if meta.get("album"):
            key = meta["album"].split("-")[-1].lower()
            try:
                album = Album.get(key=key)
            except peewee.DoesNotExist:
                pass
        # Pickling in protocol 0 and converting to string for Python 2 compatibility
        meta["meta"] = pickle.dumps(meta.get("meta", {}), 0).decode()
        if album is None and meta.get("title"):
            album = Album.create(
                album_path=path,
                start_date=meta.get("start_date"),
                end_date=meta.get("end_date"),
                title=meta["title"],
                description=meta.get("description"),
                meta=meta["meta"],
            )
        else:
            updated = False
            for f in META_FIELDS:
                if meta.get(f) is not None and not getattr(album, f) == meta[f]:
                    setattr(album, f, meta[f])
                    updated = True
            if updated:
                album.save()
        return album

    def _echo_failed_meta_files(self):
        if self.failed_meta_files:
            click.echo(79 * "-")
            click.echo(
                "Please Note: "
                "The YAML parser could not parse the following meta files:"
                "\n- %s" % "\n- ".join(self.failed_meta_files)
            )
            click.echo(79 * "-")

    def _process_single_photo(self, photo, reprocess_image_meta=False):
        path, file_name, album = photo
        file_path = os.path.join(path, file_name)
        md5sum = checksum(file_path)
        changed, duplicate = False, False

        # Detect a duplicate picture in a different place.
        if md5sum in self.checksums:
            self.duplicates += 1
            duplicate = True
        else:
            self.checksums.append(md5sum)

        try:
            pic = Picture.get(checksum=md5sum)
        except peewee.DoesNotExist:
            try:
                pic = Picture.get(file_path=file_path)
                pic.checksum = md5sum
                changed = True
            except peewee.DoesNotExist:
                pic = None

        # Check for changes in existing pic.
        if pic is not None:
            with warnings.catch_warnings():  # For comparing apples and pears
                warnings.simplefilter("ignore")
                if not pic.file_path == file_path and not duplicate:
                    pic.file_path = file_path
                if not pic.file_name == file_name and not duplicate:
                    pic.file_name = file_name
                    changed = True  # Because date in filename could've changed

        if pic is None or changed or reprocess_image_meta:
            meta = image_metadata(file_path)
            if meta["date"] is None:
                meta["date"] = file_name_date(
                    file_path, self.config.file_date_formats, self.config.use_file_creation_date_as_image_date
                )

        if pic is None and not duplicate:
            self.new += 1
            pic = Picture.create(
                checksum=md5sum,
                file_path=file_path,
                file_name=file_name,
                sort_date=meta["date"],
                caption=meta["caption"],
                latitude=meta["gps"][0],
                longitude=meta["gps"][1],
                rotation=meta["rotation"],
            )
        elif changed or reprocess_image_meta:
            self.changed += 1
            pic.sort_date = meta["date"]
            pic.caption = meta["caption"]
            pic.latitude = meta["gps"][0]
            pic.longitude = meta["gps"][1]
            pic.rotation = meta["rotation"]
            if changed:
                pic.last_change_indexed = datetime.datetime.now()
            pic.save()
        else:
            self.unchanged += 1

        if album is not None and album not in pic.albums:
            pic.albums.add(album)

        self.processed += 1
        return pic

    def index(self, dirs=[], reprocess_image_meta=False):
        photo_dirs = dirs if dirs else self.config.original_photos_dirs
        if not photo_dirs:
            return fatal_error("There were no directories to index.")
        click.echo("Finding all photos and directories in: ")
        excluded_paths = []
        album_paths = {}
        try:
            for nr, pd in enumerate(photo_dirs, start=1):
                click.echo("%s. %s" % (nr, pd))
                for path, dirs, files in os.walk(pd):
                    # See if this path should be included.
                    if path == pd:
                        continue
                    if list(filter(lambda p: path.startswith(p), excluded_paths)):
                        continue
                    if os.path.exists(os.path.join(path, self.config.exclude_file_name)):
                        excluded_paths.append(path)
                        continue

                    click.echo("  - %s" % path.replace(pd + "/", ""))
                    # Check if this path is inside an existing album
                    album = None
                    for p in album_paths:
                        if path.startswith(p):
                            album = album_paths[p]
                            short_path = path.replace(p + "/", "")
                            break
                    if album is None:
                        # Check for available meta data
                        meta = self._meta_from_path(path)
                        if self.config.create_albums_from_dir_names:
                            meta = self._meta_from_dir_name(path, meta)

                        # If there is meta data, see which album it goes into.
                        album = self._album_from_meta(path, meta.copy())

                        if album:
                            if isinstance(meta.get("meta", {}).get("exclude"), list):
                                album.exclude = meta["meta"]["exclude"]
                            album_paths[path] = album
                            short_path = None
                    # Index files if they should be included
                    if album and short_path in album.exclude:
                        continue
                    for f in filter_image_files(self.config, files):
                        self.photos.append((path, f, album))
        except KeyboardInterrupt:
            return abort("Cancelled during indexing. Meta data may have been updated.")
        click.echo("All directories have been indexed.\n")

        self._echo_failed_meta_files()

        aborted = False
        click.echo("Processing %s photos." % len(self.photos))
        try:
            with click.progressbar(self.photos, label="Processed:", length=len(self.photos), show_pos=True) as bar:
                for photo in bar:
                    self._process_single_photo(photo, reprocess_image_meta=reprocess_image_meta)
        except KeyboardInterrupt:
            aborted = True
        if aborted:
            msg = "PLEASE NOTE: Aborted after processing %s of %s photos.\n" % (self.processed, len(self.photos))
        else:
            msg = "Done processing photos:\n"
        for name in ["new", "changed", "duplicates", "unchanged"]:
            count = getattr(self, name)
            msg += "{name:>12}: {nr:>5}\n".format(name=name, nr=count)
        msg += "{name:>12}  {nr:>5}\n".format(name="", nr="————— +")
        msg += "{name:>12}: {nr:>5}\n".format(name="total", nr=self.processed)
        click.echo(msg)

    def update_album_meta(self):
        def _get_albums(page=0):
            page += 1
            return Album.select().order_by(Album.id).paginate(page, 1000), page

        click.echo("Checking for updated meta file in existing albums.")
        total = Album.select().order_by(Album.id).count()
        albums, page = _get_albums()
        with click.progressbar(length=total, label="Albums:", show_pos=True) as bar:
            click.echo
            while albums.count():
                for album in albums:
                    bar.update(1)
                    meta = self._meta_from_path(album.album_path)
                    if not meta:
                        continue
                    # Pickling in protocol 0 and converting to string for Python 2 compatibility
                    meta["meta"] = pickle.dumps(meta.get("meta", {}), 0).decode()
                    updated = False
                    for p in META_FIELDS:
                        if meta.get(p) is not None and not getattr(album, p) == meta.get(p):
                            setattr(album, p, meta[p])
                            updated = True
                    if updated:
                        album.save()
                albums, page = _get_albums(page)

        self._echo_failed_meta_files()
        click.echo("Done.")

    def test_meta(self, meta_file):
        return parse_meta_file(meta_file)
