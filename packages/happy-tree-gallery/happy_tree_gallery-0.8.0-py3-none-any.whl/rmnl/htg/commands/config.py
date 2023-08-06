# -*- coding: utf8 -*-

import click

from ..classes import Config
from ..classes import HTGConfigError
from ..utils import fatal_error
from ..utils.aliased_group import AliasedGroup


@click.group(
    cls=AliasedGroup,
    help="Create and check your config file",
    epilog='Use "htg config COMMAND --help" for help with subcommands.',
)
def config(*args, **kwargs):
    pass


@click.command("create", help="Create a new config file.")
@click.argument(
    "config-file", required=False, type=click.Path(exists=False, dir_okay=False, resolve_path=True, writable=True)
)
def _create(config_file, *args, **kwargs):
    Config(config_file, create=True)


config.add_command(_create)


@click.command("test", help="Test your config file.")
@click.argument(
    "config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True, writable=True)
)
def _test(config_file, *args, **kwargs):
    try:
        Config(config_file, apply_changes=False)
    except HTGConfigError as e:
        return fatal_error(e.msg)
    click.echo("All OK!")


config.add_command(_test)
