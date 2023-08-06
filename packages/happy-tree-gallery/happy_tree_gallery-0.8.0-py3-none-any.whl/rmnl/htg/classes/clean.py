# coding: utf-8

import click
import os
import peewee
import re

from ..models import Album
from ..models import Picture
from ..models import ResizedPicture
from ..models import Size

from ..utils import fatal_error


MOVE_MODELS = [(Album, "album_path"), (Picture, "file_path"), (ResizedPicture, "picture_path")]


class Clean(object):

    albums_removed = 0
    pictures_checked = 0
    resized_deleted = 0
    keep_resized = False
    resize_dir = None
    page = 0

    def __init__(self, config):
        self.config = config

    def _remove_picture(self, pic):
        nr = pic.resized_pictures.count()
        pic.albums.clear()
        pic.delete_instance(recursive=not self.keep_resized)
        if nr and not self.keep_resized:
            self.resized_deleted += 1

    def _get_model_instances(self, model, page=0):
        page += 1
        return model.select().order_by(model.id).paginate(page, 1000), page

    def _clean_model_by_path(self, model, path_name, removal_method=None):
        checked = 0
        removed = 0
        instances, page = self._get_model_instances(model)
        while instances.count():
            for instance in instances:
                checked += 1
                path = getattr(instance, path_name)
                if not os.path.exists(path):
                    # click.echo("%s: %s" % (model, path))
                    # continue
                    if removal_method is None:
                        instance.delete_instance()
                    else:
                        self.__getattribute__(removal_method)(instance)
                    removed += 1
            instances, page = self._get_model_instances(model, page)
        return checked, removed

    def _delete_resizes(self):
        checked, deleted = 0, 0
        available_sizes = [size.name for size in Size.select()]
        for path, dirs, files in os.walk(self.resize_dir):
            rel_path = os.path.relpath(path, self.resize_dir)
            for f in files:
                checked += 1
                m = re.match(r"^(?P<key>[a-zA-Z0-9]{6})-(?P<size_name>\w+)\.{1}[a-z]+$", f)
                if m:
                    if m.group("size_name") not in available_sizes:
                        click.echo("Size does not exist: %s" % os.path.join(path, f))
                        # os.unlink(os.path.join(path, f))
                        deleted += 1
                        continue
                    key = "%s%s" % (rel_path, m.group("key"))
                    try:
                        Picture.get(Picture.key == key)
                    except peewee.DoesNotExist:
                        click.echo("Key (%s) does not exist: %s" % (key, os.path.join(path, f)))
                        # os.unlink(os.path.join(path, f))
                        deleted += 1
        return checked, deleted

    def clean(self, keep_resized=False, resize_dir=None):
        self.resize_dir = self.config.resized_photos_dir if resize_dir is None else resize_dir
        self.keep_resized = keep_resized
        # Cleaning pictures
        click.echo("Cleaning pictures... ", nl=False)
        checked, removed = self._clean_model_by_path(Picture, "file_path", "_remove_picture")
        click.echo("Done.")
        click.echo("    Removed %s of the %s pictures." % (removed, checked))
        if self.resized_deleted:
            click.echo("    Deleted %s resized versions." % self.resized_deleted)

        # Removing deleted resizes
        click.echo("Cleaning resizes deleted on the system... ", nl=False)
        checked, removed = self._clean_model_by_path(ResizedPicture, "path")
        click.echo("Done.")
        click.echo("    Removed %s of the %s resizes." % (removed, checked))

        # Removing orphaned resizes
        if self.resize_dir is not None:
            click.echo("Deleting orphaned resized pictures...", nl=False)
            checked, deleted = self._delete_resizes()
            click.echo("Done.")
            click.echo("    Deleted %s orphaned resizes." % deleted)

        # Removing deleted albums
        click.echo("Cleaning folder based albums... ", nl=False)
        checked, removed = self._clean_model_by_path(Album, "album_path")
        click.echo("Done.")
        click.echo("    Removed %s of the %s albums." % (removed, checked))

    def move(self, from_dir=None, to_dir=None):
        click.echo("Changing all save paths that start with:")
        click.echo("    %s" % from_dir)
        click.echo("to:")
        click.echo("    %s" % to_dir)
        if from_dir is None or to_dir is None:
            return fatal_error("Please provide both an old directory and a " "new directory.")
        from_dir = from_dir[:-1] if from_dir[-1] == "/" else from_dir
        to_dir = to_dir[:-1] if to_dir[-1] == "/" else to_dir
        counter = 0
        for model, path in MOVE_MODELS:
            instances = model.select().where(getattr(model, path).startswith(from_dir))
            for instance in instances:
                old_path = getattr(instance, path)
                setattr(instance, path, old_path.replace(from_dir, to_dir))
                instance.save()
                counter += 1
        click.echo("Done.")
        click.echo("Replaced %s instances." % counter)
