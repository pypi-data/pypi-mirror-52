# -*- coding: utf8 -*-

import click
import os

from ..models import Picture
from ..utils import abort
from ..utils import check_and_create_dir
from ..imaging import resize_and_cache


class ResizeSimple(object):

    queue = []
    sizes = {}
    resizes_processed = 0
    page = 0

    def __init__(self, config, force=False, sizes=[], output_dir=None):
        self.config = config
        self.output_dir = output_dir if output_dir else self.config.resized_photos_dir
        self.sizes = [self.config.sizes[s] for s in self.config.sizes if s in sizes or not sizes]

    def start(self):
        aborted = False
        click.echo("Filling up resize queue... ", nl=False)
        try:
            self._scan_pictures()
        except KeyboardInterrupt:
            return abort("\nCancelled queueing. Nothing changed.")
        click.echo("Done.")

        click.echo("Resizing %s pictures." % len(self.queue))
        try:
            with click.progressbar(self.queue) as bar:
                for job in bar:
                    self._process_resize_job(job)
                    self.resizes_processed += 1
        except KeyboardInterrupt:
            aborted = True
        if aborted:
            msg = "PLEASE NOTE: Aborted after processing %s of %s resizes.\n" % (
                self.resizes_processed,
                len(self.queue),
            )
        else:
            msg = "Done resizing pictures: "
            msg += "Processed %s resizes." % self.resizes_processed
        click.echo(msg)

    def _get_pictures(self):
        self.page += 1
        return Picture.select().order_by(Picture.id).paginate(self.page, 1000)

    def _scan_pictures(self):
        pics = self._get_pictures()
        while pics.count():
            for pic in pics:
                for size in self.sizes:
                    self.queue.append((pic, size))
            pics = self._get_pictures()

    def _resize_path(self, picture, size):
        path, ext = os.path.splitext(picture.file_path)
        return os.path.join(self.output_dir, picture.key[:2], "%s-%s%s" % (picture.key[2:], size.name, ext))

    def _process_resize_job(self, job):
        picture, size = job
        resize_path = self._resize_path(picture, size)
        if os.path.isfile(resize_path):
            return True
        resize_dir, name = os.path.split(resize_path)
        if check_and_create_dir(resize_dir, create=True):
            success, msg = resize_and_cache(
                self.config.resize_with, picture.file_path, resize_path, size.width, size.height, crop=size.crop
            )
            return success
        return False
