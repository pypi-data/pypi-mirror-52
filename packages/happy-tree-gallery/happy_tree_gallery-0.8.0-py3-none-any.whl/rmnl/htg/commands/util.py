# coding: utf-8

import click
import os
import yaml

from ..classes import Clean
from ..classes import Config
from ..classes import Index
from ..classes import Serve

from ..meta_example import META_EXAMPLE

# from ..migrate import migrate
from ..models import Album

from ..utils import abort
from ..utils import fatal_error
from ..utils.aliased_group import AliasedGroup


@click.group(
    "utils",
    cls=AliasedGroup,
    help="Various utilities",
    epilog='Use "htg utils COMMAND --help" for help with subcommands.',
)
def util(*args, **kwargs):
    pass


@click.command(
    "clean",
    help="Clean database and remove all references to pictures that no "
    "longer exist on your file system. Also deletes all resized pictures "
    "based on the pictures that are removed.",
)
@click.option(
    "--keep-resized",
    help="By default all resized versions of originals that can no longer be "
    "found on your file system are removed from the database and deleted "
    "from your file system. Set this flag to keep these resized pictures "
    "anyway",
    is_flag=True,
)
@click.option(
    "--resize-dir",
    help="Directory in which to look for resized images that are no longer in "
    "the database. Found resized images will be deleted. Defaults to "
    "resized_photos_dir setting from your config file.",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
)
@click.argument("config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def clean(config_file, keep_resized=False, resize_dir=None, *args, **kwargs):
    try:
        clean = Clean(Config(config_file))
        clean.clean(keep_resized=keep_resized, resize_dir=resize_dir)
    except KeyboardInterrupt:
        return abort()


util.add_command(clean)


@click.command(
    "meta",
    help="Tests the METAFILE if the file exists or attempts to create a meta "
    "file with example data if the file does not exist.",
)
@click.argument(
    "meta-file", required=True, metavar="METAFILE", type=click.Path(exists=False, dir_okay=False, resolve_path=True)
)
def meta(meta_file):
    if os.path.isfile(meta_file):
        index = Index()
        meta_data = index.test_meta(meta_file)
        if meta_data is None:
            click.echo("File could not be parsed.")
        else:
            click.echo("%s" % meta_data)
            if meta_data.get("description"):
                click.echo("Description:\n".upper())
                click.echo("%s" % meta_data["description"])
                del (meta_data["description"])
            click.echo("\nParsed and reformatted data:\n".upper())
            click.echo("%s" % yaml.dump(meta_data, default_flow_style=False))
            click.echo("\nFile is ok.".upper())
    else:
        if not os.path.isdir(os.path.dirname(meta_file)):
            return fatal_error("The directory %s does not exist." % os.path.dirname(meta_file))
        try:
            fp = open(meta_file, "w")
        except IOError:
            return fatal_error("The file %s is not writable." % meta_file)
        fp.write(META_EXAMPLE)
        fp.close()
        click.echo("Created example meta file at: %s" % meta_file)


util.add_command(meta)


@click.command("move", help="Moved changes file paths in the db after you moved files on your " "file system.")
@click.option(
    "--from-dir",
    "-f",
    required=True,
    type=click.Path(exists=False, file_okay=False, resolve_path=True),
    help="The old directory",
)
@click.option(
    "--to-dir",
    "-t",
    required=True,
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    help="The new directory (needs to exist).",
)
@click.argument("config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def move(config_file=None, from_dir=None, to_dir=None, *args, **kwargs):
    try:
        clean = Clean(Config(config_file))
        clean.move(from_dir=from_dir, to_dir=to_dir)
    except KeyboardInterrupt:
        return abort()


util.add_command(move)


@click.command("reset", help="Delete albums or the entire database. Beware!")
@click.option(
    "--db",
    help="Resets everything by deleting the database file. Otherwise only the " "albums will be deleted.",
    is_flag=True,
)
@click.argument("config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def reset(config_file, db=False, *args, **kwargs):
    config = Config(config_file)
    if db and click.confirm("Are you sure you want to delete your " "database file?"):
        os.unlink(config.database_file)
    else:
        Album.delete().execute()


util.add_command(reset)


@click.command("serve", help="Simple webserver to test your gallery.")
@click.option("--host", help="Select the hostname for your local server.", default="localhost")
@click.option("--port", help="Select the port.", default=8000, type=int)
@click.argument("document-root", required=False, type=click.Path(exists=True, file_okay=False, resolve_path=True))
def serve(document_root=None, host="localhost", port=8000, *args, **kwargs):
    Serve.serve(document_root, host=host, port=port, *args, **kwargs)


util.add_command(serve)


# util.add_command(migrate)
