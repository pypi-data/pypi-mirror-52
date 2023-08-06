# coding: utf-8

import click
import datetime
import os
import peewee
import pickle
import string

from ..models import Album
from ..models import AlbumPicture
from ..models import Picture
from ..models import ResizedPicture
from ..utils import check_and_create_dir
from ..utils import fatal_error
from ..utils import slugify
from ..utils import to_utc_timestamp
from ..utils import write_json


class Json(object):

    copy_failed_for = []
    files_to_copy = []
    templates = []
    anchors = []

    def __init__(self, config, output_dir=None):
        self.config = config
        self.output_dir = output_dir if output_dir else config.json_data_dir

    def _anchor(self, text):
        def _a(anchor, counter):
            return "%s-%s" % (anchor, counter) if counter else anchor

        anchor = slugify(text)
        counter = 0
        while _a(anchor, counter) in self.anchors:
            counter += 1
        return _a(anchor, counter)

    def _generate_albums_json(self):
        abs_dir = os.path.join(self.output_dir, "albums")
        if not check_and_create_dir(abs_dir, create=True):
            return None
        album_titles, album_slugs, album_list = [], [], []
        albums = Album.select().where(Album.hidden == False).order_by(Album.start_date.desc())  # noqa E712
        with click.progressbar(albums, label="Albums exported: ", length=albums.count(), show_pos=True) as bar:
            for album in bar:
                pics = None
                content = []
                meta = pickle.loads(album.meta.encode()) if album.meta else {}
                if album.from_dir and "name_desc" == meta.get("order_by", ""):
                    pics = album.pictures.order_by(Picture.file_name.desc())
                elif album.from_dir and "date_desc" == meta.get("order_by", ""):
                    pics = album.pictures.order_by(Picture.sort_date.desc())
                elif album.from_dir and "date_asc" == meta.get("order_by", ""):
                    pics = album.pictures.order_by(Picture.sort_date.asc())
                elif album.from_dir:
                    pics = album.pictures.order_by(Picture.file_name.asc())
                else:
                    one_day = datetime.timedelta(1)
                    if album.end_date is None:
                        end_date = album.start_date + one_day
                    else:
                        end_date = album.end_date + one_day
                    pics = (
                        Picture.select()
                        .where(Picture.sort_date > album.start_date, Picture.sort_date < end_date)
                        .order_by(Picture.sort_date.asc())
                    )

                chapters = meta.get("chapters", None)
                daily_titles, daily_subs = False, False
                if isinstance(chapters, list):
                    daily_titles = False
                elif chapters == "daily" or self.config.auto_day_paragraphs:
                    daily_titles = True

                cover = meta.get("cover", None)
                if cover:
                    try:
                        cover = Picture.get(Picture.file_name == cover).build_dict(self.config.resized_photos_url)
                    except peewee.DoesNotExist:
                        cover = None

                def _comparable_day(date, alt=0):
                    if isinstance(date, datetime.date):
                        return int(datetime.datetime.strftime(date, "%Y%m%d"))
                    return alt

                if pics is not None:
                    previous_day = 0
                    for pi, pic in enumerate(pics):
                        new_chapter = None
                        day = _comparable_day(pic.sort_date, previous_day)
                        if isinstance(chapters, list):
                            for c in chapters:
                                if c["starts"] == pic.file_name:
                                    new_chapter = c
                            if new_chapter and new_chapter.get("title"):
                                anchor = new_chapter.get("anchor", None)
                                if anchor is None:
                                    anchor = self._anchor(new_chapter["title"])
                                content.append({"type": "title", "text": new_chapter["title"], "anchor": anchor})
                            if new_chapter and new_chapter.get("subtitle"):
                                if new_chapter["subtitle"] == "daily":
                                    daily_subs = True
                                    content.append(
                                        {
                                            "type": "subtitle",
                                            "date": to_utc_timestamp(pic.sort_date),
                                            "anchor": pic.sort_date.strftime("day-%Y-%m-%d"),
                                        }
                                    )
                                else:
                                    daily_subs = False
                                    content.append(
                                        {
                                            "type": "subtitle",
                                            "text": new_chapter["subtitle"],
                                            "anchor": self._anchor(new_chapter["subtitle"]),
                                        }
                                    )
                            elif new_chapter:
                                daily_subs = False

                        if (daily_titles or daily_subs) and not new_chapter and day > previous_day:
                            content.append(
                                {
                                    "type": "subtitle" if daily_subs else "title",
                                    "date": to_utc_timestamp(pic.sort_date),
                                    "anchor": pic.sort_date.strftime("day-%Y-%m-%d"),
                                }
                            )

                        pic_dict = pic.build_dict(self.config.resized_photos_url)

                        # If we do not have a cover, we take the first picture
                        if cover is None:
                            cover = pic_dict.copy()

                        for resize in pic.resized_pictures.where(ResizedPicture.successfully_created).where(
                            ResizedPicture.size << self.config.sizes_in_json
                        ):
                            pic_dict[resize.size.name] = [resize.width, resize.height]
                        content.append(pic_dict)
                        previous_day = day

                    json_name = "%s.json" % album.slug
                    album_titles.append(string.capwords(album.title))
                    album_slugs.append(album.slug)
                    album_dict = {
                        "title": string.capwords(album.title),
                        "start_date": to_utc_timestamp(album.start_date),
                        "end_date": to_utc_timestamp(album.end_date),
                        "json": os.path.join("albums", json_name),
                        "slug": album.slug,
                        "total": pics.count(),
                        "cover": cover,
                    }
                    album_list.append(album_dict.copy())
                    album_dict["content"] = content
                    if album.description:
                        album_dict["description"] = album.description
                    if album.meta:
                        album_dict["meta"] = pickle.loads(album.meta.encode())
                    write_json(os.path.join(abs_dir, json_name), album_dict)
        write_json(
            os.path.join(self.output_dir, "albums.json"),
            {"titles": album_titles, "albums": album_list, "slugs": album_slugs},
        )

    def _generate_timeline_page(self, year=None, include_album_photos=False):
        if include_album_photos:
            base_query = Picture.select().where(Picture.sort_date.is_null(False))
        else:
            base_query = (
                Picture.select()
                .join(AlbumPicture, peewee.JOIN.LEFT_OUTER)
                .join(Album, peewee.JOIN.LEFT_OUTER)
                .where(Album.id.is_null())
                .where(Picture.sort_date.is_null(False))
            )

        if year is not None:
            base_query = base_query.where(
                (Picture.sort_date >= datetime.datetime(year, 1, 1))
                & (Picture.sort_date < datetime.datetime(year + 1, 1, 1))
            )

        base_query = base_query.order_by(Picture.sort_date.desc())

        total = base_query.count()
        if not total:
            return None

        # Create the destination directories
        dir_name = "including" if include_album_photos else "excluding"
        dest = os.path.join(self.output_dir, "timeline", dir_name)
        if not check_and_create_dir(dest, create=True):
            return None
        if year is not None:
            dest = os.path.join(dest, "%s" % year)
            if not check_and_create_dir(dest, create=True):
                return None

        nr_of_pages = int(total / self.config.photos_per_json_file) + (
            1 if total % self.config.photos_per_json_file else 0
        )

        def _get_timeline_pics(base_query, page=0):
            page += 1
            pics = base_query.paginate(page, self.config.photos_per_json_file)
            return pics, page

        if self.config.timeline_granularity == "daily":
            l1, l2, f1, f2 = "month", "day", "month-%Y-%m", "day-%Y-%m-%d"
        else:
            l1, l2, f1, f2 = "year", "month", "year-%Y", "month-%Y-%m"

        pages = []
        pics, page = _get_timeline_pics(base_query)
        previous_date = None
        label = "{:>7}".format("%s | " % year if year else " All | ")
        label += "including:" if include_album_photos else "excluding:"
        with click.progressbar(length=nr_of_pages, label=label, show_pos=True) as bar:
            while pics.count():
                content = []
                for pic in pics:
                    date = pic.sort_date
                    timestamp = to_utc_timestamp(date)
                    if previous_date is None or not getattr(date, l1) == getattr(previous_date, l1):
                        content.append({"type": "title-%s" % l1, "date": timestamp, "anchor": date.strftime(f1)})
                    if previous_date is None or not getattr(date, l2) == getattr(previous_date, l2):
                        content.append({"type": "subtitle-%s" % l2, "date": timestamp, "anchor": date.strftime(f2)})

                    pic_dict = pic.build_dict(self.config.resized_photos_url)

                    for resize in pic.resized_pictures.where(ResizedPicture.successfully_created).where(
                        ResizedPicture.size << self.config.sizes_in_json
                    ):
                        pic_dict[resize.size.name] = [resize.width, resize.height]

                    content.append(pic_dict)
                    previous_date = date
                if not pages:
                    pages.append(to_utc_timestamp(pics[0].sort_date))
                pages.append(to_utc_timestamp(pics[pics.count() - 1].sort_date))
                write_json(os.path.join(dest, "%s.json" % page), {"content": content, "page": page})
                bar.update(1)
                pics, page = _get_timeline_pics(base_query, page=page)
        return pages

    def _generate_timeline_json(self):
        timeline_dir = os.path.join(self.output_dir, "timeline")
        if not check_and_create_dir(timeline_dir, create=True):
            return fatal_error("Could not create Timeline directory.")
        timeline = {"including": {"years": {}}, "excluding": {"years": {}}, "page_dir": "timeline"}
        first_year = (
            Picture.select()
            .where(Picture.sort_date.is_null(False))
            .order_by(Picture.sort_date.asc())
            .limit(1)[0]
            .sort_date.year
        )
        last_year = (
            Picture.select()
            .where(Picture.sort_date.is_null(False))
            .order_by(Picture.sort_date.desc())
            .limit(1)[0]
            .sort_date.year
        )
        # Generate complete timeline:
        # 1. Including album photos
        timeline["including"]["pages"] = self._generate_timeline_page(include_album_photos=True)
        # 2. Excluding album photos
        timeline["excluding"]["pages"] = self._generate_timeline_page()
        # The same per year.
        for year in range(first_year, last_year + 1):
            timeline["including"]["years"][year] = self._generate_timeline_page(year=year, include_album_photos=True)
            timeline["excluding"]["years"][year] = self._generate_timeline_page(year=year)
        write_json(os.path.join(self.output_dir, "timeline.json"), timeline)

    def generate(self, albums=True, timeline=True):
        # Generate JSON
        if albums:
            click.echo("Generating json for albums... ", nl=False)
            self._generate_albums_json()
            click.echo("Done.")
        if timeline:
            click.echo("Generating json for the timeline... ", nl=False)
            self._generate_timeline_json()
            click.echo("Done.")
        click.echo("Exported json files to: %s" % self.output_dir)
