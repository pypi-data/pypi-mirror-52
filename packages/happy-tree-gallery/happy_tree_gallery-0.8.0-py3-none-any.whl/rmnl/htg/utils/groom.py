import click
import datetime
import os
import sys

from ..meta_example import META_EXAMPLE_SHORT
from ..meta_example import META_EXAMPLE_NO_ALBUM
from ..utils import filter_image_files
from ..utils import title_and_date_from_dir_name
from ..utils import user_input


def groom_subdirs(config, album_path):
    exclude, sub_dirs = [], []
    click.echo("  Grooming subdirectories of the album:")
    for path, dirs, files in os.walk(album_path):
        path = "" if path == album_path else path.replace(album_path + "/", "")
        if filter_image_files(config, files):
            sub_dirs.append(path)
        else:
            exclude.append(path)
    # Reversing so we start with the deepest directories first. This makes
    # more sense when grooming.
    sub_dirs.reverse()
    for d in sub_dirs:
        text = "Album root" if "" == d else d
        click.echo("  - %s:" % text, nl=False)
        if not click.confirm(" Include contents in album?"):
            exclude.append(d)
    if exclude:
        exclude.sort()
        return "exclude:\n  - %s" % "\n  - ".join(exclude)
    return ""


def groom(config, dirs, include_all=False):
    click.echo(
        "Groom is going to loop through all your directories and for each "
        "directory you will get 4 choices: \n"
        "\n"
        "- i: Ignore the directory\n"
        "- x: Exclude the directory (1)\n"
        "- a: Include the directory and consider its contents as an album (2)\n"
        "- n: Include the media in the directory, but it's not an album (2)\n"
        "\n"
        "(1): An exclusion file will be added to the directory. The name of "
        'this file can be set with the "exclude_file_name" '
        "setting in your config file.\n"
        "(2): A meta file will be added to the directory. The name of this "
        'meta file is set in the "meta_file_name" setting inside the config '
        "file.\n"
    )
    if not click.confirm("All clear?"):
        click.echo("Ok, aborting..")
        sys.exit()
    skip_dirs = []
    for root_dir in dirs:
        click.echo("Grooming directory: %s" % root_dir)
        for path, dirs, files in os.walk(root_dir):
            if path == root_dir:
                continue
            if list(filter(lambda d: path.startswith(d), skip_dirs)):
                continue
            click.echo("- %s" % path.replace(root_dir, ""))
            exclude, meta = False, False
            exclude_file = os.path.join(path, config.exclude_file_name)
            meta_file = os.path.join(path, config.meta_file_name)
            if os.path.exists(exclude_file):
                exclude = exclude_file
            if os.path.exists(meta_file):
                meta = meta_file
            if exclude and not include_all:
                skip_dirs.append(path)
                click.echo("  Skipped: Already excluded.")
                continue
            if meta and not include_all:
                skip_dirs.append(path)
                click.echo("  Skipped: Already has a meta file.")
                continue
            if not os.access(path, os.W_OK):
                click.echo(" Skipped: Directory is not writable.")
                continue
            answer = None
            while answer not in ["i", "x", "a", "n"]:
                answer = user_input(
                    # 'Ignore, eXclude, Album, or Not an album? '
                    "  [i|x|a|n]: "
                )
            if answer == "x":
                if exclude:
                    # click.echo('  Already excluded, nothing changed')
                    continue
                if meta and not click.confirm(
                    "  This directory currently has a meta file.\n" "  Are you sure you want to delete this file?"
                ):
                    click.echo("  Skipped")
                    continue
                if meta:
                    try:
                        os.unlink(meta)
                    except OSError:
                        click.echo("  ERROR: could not delete the meta file.")
                        continue
                fp = open(exclude_file, "w")
                fp.close()
                skip_dirs.append(path)
                continue

            if answer == "a" or answer == "n":
                if exclude:
                    try:
                        os.unlink(exclude)
                    except OSError:
                        click.echo("  ERROR: could not delete the exclusion file.")
                        continue
                if meta and not click.confirm(
                    "  This directory already has a meta file.\n" "  Are you sure you want to overwrite this file?"
                ):
                    click.echo("  Skipped")
                    continue
                if answer == "a":
                    title, start_date = title_and_date_from_dir_name(path, config.album_dir_pattern)
                    if title is None:
                        title = "Title of your Album"
                    if start_date is None:
                        start_date = datetime.datetime.now()
                    extra = groom_subdirs(config, path) if dirs else ""
                    content = META_EXAMPLE_SHORT % {
                        "title": title,
                        "start_date": start_date.strftime("%Y-%m-%d"),
                        "extra": extra,
                    }
                else:
                    content = META_EXAMPLE_NO_ALBUM
                fp = open(meta_file, "w")
                fp.write(content)
                fp.close()
                skip_dirs.append(path)
                continue

            # ignoring
            if exclude:
                try:
                    os.unlink(exclude)
                except OSError:
                    click.echo("  ERROR: could not delete the exclusion file.")
                    continue
            if meta and not click.confirm(
                "  This directory currently has a meta file.\n" "  Are you sure you want to delete this file?"
            ):
                click.echo("  Skipped")
                continue
            if meta:
                try:
                    os.unlink(meta)
                except OSError:
                    click.echo("  ERROR: could not delete the meta file.")
                    continue
    click.echo("Done")
