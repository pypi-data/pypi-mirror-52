# -*- coding: utf8 -*-

import click
import datetime
import os

from ..models import Picture
from ..models import ResizedPicture
from ..utils import abort
from ..utils import check_and_create_dir
from ..imaging import resize_and_cache


class Resize(object):

    queue = []
    resizes_processed = 0
    page = 0

    def __init__(self, config, force=False, sizes=[], output_dir=None):
        self.config = config
        self.force = force
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
            with click.progressbar(self.queue, label="Resized:", length=len(self.queue), show_pos=True) as bar:
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
                resizes = {}
                for resize in pic.resized_pictures.where(ResizedPicture.picture_path == self.output_dir):
                    resizes[resize.size.name] = resize
                for size in self.sizes:
                    if size.name not in resizes:
                        self.queue.append((pic, size, None))
                    elif size.name in resizes and (
                        resizes[size.name].resize_date is None
                        or resizes[size.name].resize_date < pic.last_change_indexed
                    ):
                        self.queue.append((pic, size, resizes[size.name]))
                    elif self.force:
                        self.queue.append((pic, size, resizes[size.name]))
            pics = self._get_pictures()

    def _process_resize_job(self, job):
        picture, size, resize = job
        if resize is None:
            resize = ResizedPicture.create(picture=picture, size=size, picture_path=self.output_dir)
        resize.resize_date = datetime.datetime.now()
        resize_dir, name = os.path.split(resize.path)
        image_size = False
        if check_and_create_dir(resize_dir, create=True):
            image_size, msg = resize_and_cache(
                self.config.resize_with,
                picture.file_path,
                resize.path,
                size.width,
                size.height,
                crop=size.crop,
                rotation=picture.rotation,
            )
        if image_size:
            resize.width = image_size[0]
            resize.height = image_size[1]
            resize.successfully_created = True
        resize.save()
