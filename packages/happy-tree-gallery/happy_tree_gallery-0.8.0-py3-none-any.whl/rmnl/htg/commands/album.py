# coding: utf-8

import click
import datetime
import peewee
import pickle
import yaml

from ..classes import Config
from ..models import Album
from ..utils import alphanum_hash
from ..utils import fatal_error
from ..utils.aliased_group import AliasedGroup


def _date_from_input(date_str):
    try:
        return datetime.datetime.strptime("%s" % date_str, "%Y-%m-%d")
    except ValueError:
        try:
            return datetime.datetime.strptime("%s" % date_str, "%Y-%m-%d-%H-%M")
        except ValueError:
            return False
    return None


def _validate_date(ctx, param, value):
    if value is None:
        return None
    date = _date_from_input(value)
    if date is False:
        now = datetime.datetime.now()
        raise click.BadParameter(
            "Please use YYYY-MM-DD or YYYY-MM-DD-hh-mm as a date format. "
            "E.g. %s or %s for now." % (now.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d-%H-%M"))
        )
    else:
        return date


@click.group(
    "album",
    cls=AliasedGroup,
    help="Album management",
    epilog='Use "htg album COMMAND --help" for help with subcommands.',
)
def album(*args, **kwargs):
    pass


@click.command("list", help="List Albums.")
@click.option(
    "--year",
    "-y",
    help="Only list albums of a certain year.",
    type=int,
    # callback=_test_year,
)
@click.option(
    "--title",
    "-t",
    help="Filter title by string.",
    # callback=_test_year,
)
@click.argument("config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def list(config_file=None, year=None, title=None, *args, **kwargs):
    Config(config_file)
    albums = Album.select()
    if year is not None:
        albums = albums.where(
            Album.start_date > datetime.datetime(year, 1, 1), Album.start_date < datetime.datetime(year + 1, 1, 1)
        )
    if title is not None:
        albums = albums.where(Album.title.contains(title))
    if not albums.count():
        click.echo("No albums found.")
        return
    click.echo("┌" + (40 * "─") + "┬" + (12 * "─"), nl=False)
    click.echo("┬" + (7 * "─") + "┬" + (12 * "─") + "┬───┐")
    click.echo("│ {:<38} │ ".format("TITLE"), nl=False)
    click.echo("{:^10} │ ".format("START DATE"), nl=False)
    click.echo("{:<5} │ ".format("PICS"), nl=False)
    click.echo("{:<10} │ * │".format("KEY"))
    click.echo("├" + (40 * "─") + "┼" + (12 * "─"), nl=False)
    click.echo("┼" + (7 * "─") + "┼" + (12 * "─") + "┼───┤")
    for a in albums:
        title = a.title if len(a.title) < 39 else "%s..." % a.title[:35]
        start_date = a.start_date.strftime("%Y-%m-%d") if a.start_date else "-"
        nr = a.pictures.count() if a.from_dir else "?"
        click.echo("│ ", nl=False)
        click.echo("{:<38}".format(title), nl=False)
        click.echo(" │ ", nl=False)
        click.echo("{:^10}".format(start_date), nl=False)
        click.echo(" │ ", nl=False)
        click.echo("{:>5}".format(nr), nl=False)
        click.echo(" │ ", nl=False)
        click.echo("{:<10}".format(a.key), nl=False)
        click.echo(" │ ", nl=False)
        click.echo("-" if a.from_dir else "✓", nl=False)
        click.echo(" │")
    click.echo("└" + (40 * "─") + "┴" + (12 * "─"), nl=False)
    click.echo("┴" + (7 * "─") + "┴" + (12 * "─") + "┴───┘")
    click.echo("* Editable? Only albums based on date ranges can be edited.")
    click.echo("  Other albums should be edited through the meta file.")


album.add_command(list)


@click.command("show", help="Show all info for an Album.")
@click.argument("key", required=True)
@click.argument("config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def show(key, config_file=None, *args, **kwargs):
    Config(config_file)
    try:
        a = Album.get(key=key)
    except peewee.DoesNotExist:
        return fatal_error("No album with key: %s" % key)
    if a.start_date and a.end_date:
        date = "%s to %s" % (a.start_date.strftime("%b %d, %Y"), a.end_date.strftime("%b %d, %Y"))
    elif a.start_date:
        date = a.start_date.strftime("%b %d, %Y")
    else:
        date = "no date"
    click.echo("Key: %s" % a.key)
    click.echo("Title: %s" % a.title)
    click.echo("Date: %s" % date)
    click.echo("Nr of photos: %s" % a.pictures.count())
    click.echo("Album directory: %s" % a.album_path)
    meta = pickle.loads(a.meta.encode()) if a.meta else None
    if meta:
        click.echo("Other meta data below line.")
        click.echo(80 * "─")
        click.echo(yaml.dump(meta, default_flow_style=False))


album.add_command(show)


@click.command("add", help="Add an Album based on a date range.")
@click.option("--title", "-t", required=True, help="Title of your album")
@click.option(
    "--end-date",
    "-e",
    required=False,
    help="End date (and time) for photos in this album " "(YYYY-MM-DD or YYYY-MM-DD-hh-mm)",
    callback=_validate_date,
)
@click.option(
    "--start-date",
    "-s",
    required=True,
    help="Start date (and time) for photos in this album " "(YYYY-MM-DD or YYYY-MM-DD-hh-mm)",
    callback=_validate_date,
)
@click.argument("config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def add(config_file=None, *args, **kwargs):
    Config(config_file)
    a = Album.create(
        from_dir=False,
        album_path=alphanum_hash(length=32),
        start_date=kwargs["start_date"],
        end_date=kwargs.get("end_date", None),
        title=kwargs["title"],
    )
    click.echo("Album was saved with key: %s" % a.key)


album.add_command(add)


@click.command("edit", help="Edit an Album based on a date range.")
@click.option("--title", "-t", required=False, help="New title for the selected album")
@click.option(
    "--end-date",
    "-e",
    required=False,
    help="New end date (and time) for photos in the selected album " "(YYYY-MM-DD or YYYY-MM-DD-hh-mm)",
    callback=_validate_date,
)
@click.option(
    "--start-date",
    "-s",
    required=False,
    help="New start date (and time) for photos in the selected album " "(YYYY-MM-DD or YYYY-MM-DD-hh-mm)",
    callback=_validate_date,
)
@click.argument("key", required=True)
@click.argument("config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def edit(key, config_file=None, *args, **kwargs):
    Config(config_file)
    try:
        a = Album.get(key=key, from_dir=False)
    except peewee.DoesNotExist:
        return fatal_error("No editable album with key: %s" % key)
    click.echo("%s" % kwargs)
    if kwargs.get("title", None):
        a.title = kwargs["title"]
    if kwargs.get("end_date", None):
        a.end_date = kwargs["end_date"]
    if kwargs.get("start_date", None):
        click.echo("Updating start_date")
        a.start_date = kwargs["start_date"]
    a.save()
    click.echo("Album was updated.")


album.add_command(edit)


@click.command(
    "delete",
    help="Delete an Album. Note that albums based on a meta file in or "
    "directory will be added again after you scan the directory.",
)
@click.argument("key", required=True)
@click.argument("config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def delete(key, config_file=None, *args, **kwargs):
    Config(config_file)
    try:
        a = Album.get(key=key)
    except peewee.DoesNotExist:
        return fatal_error("No album with key: %s" % key)
    if click.confirm("Are you sure you want to delete the album with title: \n%s" % a.title):
        a.delete_instance(recursive=True)
        click.echo("Album deleted.")
    else:
        click.echo("Aborted.")


album.add_command(delete)
