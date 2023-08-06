# coding: utf-8

import click

from ..classes import Config
from ..classes import Resize
from ..classes import ResizeSimple
from ..utils import abort


@click.command("resize", help="Resize pictures to the specified sizes.")
@click.option(
    "--do-not-track",
    help="Normally resized pictures are stored in the database and can be "
    "regenerated when the source file changes. Set this flag "
    "to not track the resizes in the database.",
    is_flag=True,
)
@click.option("--force", help="Force resizing of all photos irregardless of their state.", is_flag=True)
@click.option(
    "--output-dir",
    "-o",
    help="Set a different output dir. This will overrule the " "resized_photos_dir setting of your config file.",
    type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True),
)
@click.option(
    "--size",
    "-s",
    help="Specify the size(s) to process when resizing. If no size is "
    "specified all sizes will be processed. Can be set multiple times. "
    "Please note that the size names must match the names in your "
    "config file.",
    multiple=True,
    # callback=validate_resize_size,
)
@click.argument("config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def resize(config_file, do_not_track=False, force=False, output_dir=None, size=[], *args, **kwargs):
    resize_class = ResizeSimple if do_not_track else Resize
    try:
        resize = resize_class(Config(config_file), force=force, sizes=size, output_dir=output_dir)
        resize.start()
    except KeyboardInterrupt:
        return abort()
