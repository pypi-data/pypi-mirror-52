import click
import datetime
import os
import yaml

from .. import APP_VERBOSE_NAME
from ..defaults import DEFAULT_CONFIG, DEFAULT_ADVANCED
from ..models import init_database
from ..models import Size
from ..utils import fatal_error
from ..utils import slugify

COMPULSORY_NOT_NONE = ["resized_photos_dir", "resized_photos_url", "json_data_dir", "json_data_url"]


class HTGConfigError(Exception):
    def __init__(self, msg):
        self.msg = msg


class Config(object):

    errors = []

    def __init__(self, config_file=None, create=False, apply_changes=True):
        self.file = config_file
        if self.file is None:
            self.file = self._default_config_file
        if create:
            return self.create()
        if not os.path.exists(self.file):
            return fatal_error("Config file does not exist.")
        return self.read(apply_changes)

    @property
    def _default_config_file(self):
        return os.path.join(click.get_app_dir(APP_VERBOSE_NAME), "config.yaml")

    def _check_sizes(self, apply_changes=True):
        sizes = {}
        self.sizes_in_json = []
        for size_name in self.sizes:
            size_dict = {
                "name": slugify(size_name),
                "width": self.sizes[size_name].get("width", None),
                "height": self.sizes[size_name].get("height", None),
                "crop": self.sizes[size_name].get("crop", False),
                "include_in_json": self.sizes[size_name].get("include_resized_size_in_json", False),
            }
            if size_dict["height"] is None:
                size_dict["height"] = size_dict["width"]
            try:
                size_dict["width"] = int(size_dict["width"])
            except (ValueError, TypeError):
                raise HTGConfigError("Size with name %s does not have a valid width value." % self.file)
            try:
                size_dict["height"] = int(size_dict["height"])
            except ValueError:
                raise HTGConfigError("Size with name %s does not have a valid height value." % self.file)

            size = Size.get_size_by_name(size_dict["name"])
            if size is None:
                size = Size(
                    name=size_dict["name"],
                    width=size_dict["width"],
                    height=size_dict["height"],
                    crop=size_dict["crop"],
                    include_in_json=size_dict["include_in_json"],
                )
            else:
                changed = False
                for key in size_dict.keys():
                    if not getattr(size, key) == size_dict[key]:
                        setattr(size, key, size_dict[key])
                        changed = True
                if changed:
                    size.change_date = datetime.datetime.now()
            if apply_changes:
                size.save()
            sizes[size.name] = size
            if apply_changes and size.include_in_json:
                self.sizes_in_json.append(size.id)

        self.sizes = sizes

    def _update_config(self, config):
        for param in config:
            # if isinstance(config[param], dict):
            #     config[param] = Struct(config[param])
            setattr(self, param, config[param])

    def create(self):
        if self.file == self._default_config_file and not os.path.exists(os.path.dirname(self.file)):
            try:
                os.makedirs(os.path.dirname(self.file), 0o775)
            except OSError:
                return fatal_error("Could not create the config directory")
        if not os.path.exists(self.file) or click.confirm("The config file already exists. Overwrite?"):
            fp = open(self.file, "w")
            fp.write(DEFAULT_CONFIG)
            fp.close()
            click.echo("Your config file was saved at: %s" % self.file)
        else:
            click.echo("Your config file could not be saved.")

    def read(self, apply_changes=True):
        base_config = yaml.safe_load(DEFAULT_CONFIG + DEFAULT_ADVANCED)
        self._update_config(base_config)
        stream = open(self.file, "r")
        try:
            user_config = yaml.safe_load(stream)
        except Exception:
            raise HTGConfigError(
                "Your config file could not be parsed. Perhaps it is not "
                "a valid YAML file. You can check your YAML at: "
                "http://www.yamllint.com/"
            )
        self._update_config(user_config)

        # Set the database file if it isn't set.
        if not self.database_file:
            self.database_file = os.path.join(os.path.dirname(self.file), "db.sqlite")

        def _check_dir(dir_path, name, writable=True):
            if not isinstance(dir_path, str):
                self.errors.append(("The value for %s is not a valid string.") % name)
            elif os.path.isdir(dir_path) and not os.access(dir_path, os.W_OK):
                self.errors.append(
                    ("The %s cannot be created because the " "the directory %s is not writable.") % (name, dir_path)
                )
            elif not os.path.isdir(dir_path):
                self.errors.append(
                    ("The %s cannot be created because the " "the directory %s is not a directory.") % (name, dir_path)
                )

        # Check if the database is writable or can be created.
        if os.path.exists(self.database_file) and not os.access(self.database_file, os.W_OK):
            self.errors.append("The database_file already exists but it is " "not writable.")
        elif not os.path.exists(self.database_file):
            _check_dir(os.path.dirname(self.database_file), "database_file")

        _check_dir(self.resized_photos_dir, "resized_photos_dir")
        _check_dir(self.json_data_dir, "json_data_dir")

        if self.errors:
            raise HTGConfigError("There were errors with one or more of your paths: \n- %s" % "\n- ".join(self.errors))

        # Filter out paths that do not exist.
        self.original_photos_dirs = [p for p in self.original_photos_dirs if isinstance(p, str) and os.path.isdir(p)]

        # Initialize the database
        init_database(self.database_file)

        # check_file
        for attr in COMPULSORY_NOT_NONE:
            if getattr(self, attr) is None:
                raise HTGConfigError("The value for %s is not set." % attr)

        self._check_sizes(apply_changes)
