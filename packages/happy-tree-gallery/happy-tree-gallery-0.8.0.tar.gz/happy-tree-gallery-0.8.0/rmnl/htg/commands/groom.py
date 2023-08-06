import click

from ..classes import Config
from ..utils.groom import groom as groomfunc


@click.command(
    "groom",
    help="Groom your photo directories by walking through them and adding "
    "a meta or exclusion file for better indexing",
)
@click.option(
    "--include-all",
    "-a",
    help="By default directories that already have an exclusion or meta_file "
    "will be skipped. Setting this option will also force you to "
    "decide again.",
    is_flag=True,
)
@click.option(
    "--directory",
    "-d",
    required=False,
    metavar="DIR",
    multiple=True,
    help="The grooming will default to the original_photos_dirs setting "
    "in the config file if you do not provide root directories.",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
)
@click.argument("config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def groom(config_file=None, directory=[], include_all=False):
    config = Config(config_file)
    dirs = directory if directory else config.original_photos_dirs
    groomfunc(config, dirs, include_all=include_all)
