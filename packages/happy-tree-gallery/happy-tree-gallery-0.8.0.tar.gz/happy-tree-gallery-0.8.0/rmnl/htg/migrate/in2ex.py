import click
import os
import yaml

from ..utils import parse_meta_file


def in2ex(config, dirs):
    skip_dirs = []
    click.echo("Updating meta files")
    for root_dir in dirs:
        for path, dirs, files in os.walk(root_dir):
            if path == root_dir:
                continue
            if list(filter(lambda d: path.startswith(d), skip_dirs)):
                continue
            exclude_file = os.path.join(path, config.exclude_file_name)
            meta_file = os.path.join(path, config.meta_file_name)
            if os.path.exists(exclude_file):
                skip_dirs.append(path)
                continue
            if not os.path.exists(meta_file):
                continue
            skip_dirs.append(path)
            meta, description = parse_meta_file(meta_file, raw=True)
            include = meta.get("include", None)
            if include:
                del (meta["include"])
            if not isinstance(include, list):
                include = []
            exclude = exclude_subdirs(path, include)
            if not exclude:
                continue
            meta["exclude"] = exclude
            if meta.get("meta", None) is not None:
                for m in meta["meta"]:
                    meta[m] = meta["meta"][m]
                del (meta["meta"])
            meta_yaml = yaml.dump(meta, default_flow_style=False)
            meta_yaml = meta_yaml.replace("\n-", "\n  -")
            if description is not None:
                meta_yaml = "%s\n---\n%s" % (meta_yaml, description)
            try:
                fp = open(meta_file, "w")
                fp.write(meta_yaml)
                fp.close()
                click.echo("Updated: %s" % meta_file)
            except OSError:
                click.echo("ERROR: %s" % meta_file)
                click.echo("       Meta file not updated, because it could " "not be overwritten.")
    click.echo("Done.")


def exclude_subdirs(album_path, include=[]):
    exclude = []
    for path, dirs, files in os.walk(album_path):
        if path == album_path:
            continue
        dir_name = path.replace(album_path + "/", "")
        if dir_name not in include:
            exclude.append(dir_name)
    exclude.sort()
    return exclude

    click.echo("Done")
