import click

from ..classes import Config
from ..migrate.in2ex import in2ex as in2exfunc
from ..utils.aliased_group import AliasedGroup


@click.group(
    "migrate",
    cls=AliasedGroup,
    help="Migration functions to help with upgrades",
    epilog='Use "htg utils migrate COMMAND --help" for help with ' "subcommands.",
)
def migrate(*args, **kwargs):
    pass


@click.command("in2ex", help="Move from include to exclude in meta_file.")
@click.option(
    "--directory",
    "-d",
    required=False,
    metavar="DIR",
    multiple=True,
    help="The in2ex will default to the original_photos_dirs setting "
    "in the config file if you do not provide root directories.",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
)
@click.argument("config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def in2ex(config_file=None, directory=[], include_all=False):
    config = Config(config_file)
    dirs = directory if directory else config.original_photos_dirs
    in2exfunc(config, dirs)


migrate.add_command(in2ex)
