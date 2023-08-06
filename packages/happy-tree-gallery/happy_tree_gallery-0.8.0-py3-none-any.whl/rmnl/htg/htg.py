#!/usr/bin/python
# coding: utf-8

"""Happy Tree Gallery: Static Gallery Generator
   If correctly installed type:
                    htg --help for help.
"""

# import os
import click

from .commands import album
from .commands import config
from .commands import groom
from .commands import index
from .commands import jsongen
from .commands import resize
from .commands import util

from . import VERSION
from . import APP_VERBOSE_NAME

from .utils.aliased_group import AliasedGroup


@click.group(
    cls=AliasedGroup,
    help="%s is a static photo gallery generator." % APP_VERBOSE_NAME,
    short_help="%s is a static photo gallery generator." % APP_VERBOSE_NAME,
    epilog='Use "htg COMMAND --help" for help with subcommands.',
)
@click.version_option(version=VERSION, message="%(version)s")
def htg(*args, **kwargs):
    pass


# Add the subcommands
htg.add_command(album)
htg.add_command(config)
htg.add_command(groom)
htg.add_command(index)
htg.add_command(jsongen)
htg.add_command(resize)
htg.add_command(util)
