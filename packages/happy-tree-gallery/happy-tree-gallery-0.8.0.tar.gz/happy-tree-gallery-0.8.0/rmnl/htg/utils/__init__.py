# coding: utf-8

""" Collection of helper functions that can be used
    in various modules of this program.
"""

import calendar
import click
import datetime
import errno
import hashlib
import json
import markdown2
import os
import random
import re
import string
import subprocess
import sys
import unicodedata
import yaml

from tkinter.filedialog import askdirectory
from tkinter import Tk


def abort(msg="Process was aborted"):
    click.echo("\nPLEASE NOTE: %s" % msg)


def alphanum_hash(length=10):
    """ Generate a random alphanumeric string.
    """
    length = max(0, length)
    population = (string.ascii_letters + string.digits) * length
    return ("".join(random.sample(population, length))).lower()


def ask_for_dir(msg="Pick your directory."):
    """ Asks the user to input the path.
        The user can choose to open a file dialog.
    """
    directory = user_input("%s\n# " % msg, case_sensitive=True)
    if directory:
        return directory
    return pick_directory()


def check_and_create_dir(path, create=False):
    """ Check if a directory exists and if not
        it can create the directory.
    """
    if os.path.isdir(path):
        return True
    if create:
        try:
            os.makedirs(path, 0o775)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
        return True
    return False


def execute(command_list):
    """ Executes commands on the command line.
        Returns tuple with the result True|False and
        the output that the command generated.
    """
    try:
        command = [c if isinstance(c, str) else str(c) for c in command_list]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = proc.communicate()
        if proc.returncode:
            return False, err.decode("utf-8") if err else None
        return True, out.decode("utf-8") if out else None
    except OSError as e:
        if isinstance(e, FileNotFoundError):  # No such file or directory
            return False, '"%s" is not available on your system.' % command[0]
        else:
            raise e


def fatal_error(message):
    """ Return a fatal error message with description and exit
        the program.
    """
    click.echo("\nFATAL ERROR:")
    sys.exit("%s\n" % message)
    return False


def file_name_date(file_path, date_formats, use_creation_date):
    bn = os.path.basename(file_path)
    date_formats = [(df, len(datetime.datetime.now().strftime(df))) for df in date_formats]
    for df in date_formats:
        try:
            dt = datetime.datetime.strptime(bn[: df[1]], df[0])
            return dt
        except ValueError:
            pass
    if use_creation_date:
        print(file_path)
        return os.path.getctime(file_path)
    return None


def filter_image_files(config, files):
    images = []
    for f in files:
        name, ext = os.path.splitext(f)
        if ext.lower() in config.image_extensions:
            images.append(f)
    return images


def checksum(file_path, digest="md5", block_size=512):
    digest = getattr(hashlib, digest)()
    f = open(file_path)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(128 * block_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_json(json_string):
    try:
        return json.loads(json_string)
    except ValueError:
        return False


def parse_meta_file(meta_file, raw=False):
    data, description, meta = None, None, {}

    fp = open(meta_file, "r")
    raw_meta = fp.read()
    fp.close()

    raw_meta = re.split(r"^(--+)|(\+\++)$", raw_meta, maxsplit=2, flags=re.M)

    if not raw_meta[0].strip():
        del (raw_meta[0])

    # Parse yaml
    data = yaml.safe_load(raw_meta[0])

    if len(raw_meta) > 1:
        description = raw_meta[1]

    if raw:
        return data, description

    if description is not None:
        extras = []
        if data.get("markdown_extras", []):
            extras = data["markdown_extras"]
            del (data["markdown_extras"])
        description = markdown2.markdown(description, extras=extras)
        meta["description"] = description
    if data is not None:
        for p in ["title", "start_date", "end_date", "include", "album"]:
            if data.get(p, None) is not None:
                meta[p] = data[p]
                del (data[p])
        if len(data):
            meta["meta"] = data
    return meta


def pick_directory():
    """ Present a UI dialog to easily pick a directory.
    """
    # we don't want a full GUI, so keep the root window from appearing
    Tk().withdraw()
    directory = askdirectory(mustexist=True)
    return directory


def read_json(path):
    """ Read json from a file and return a python dictionary
        Returns None if the file cannot be found/opened
        Returns False if the file does not contain valid json
    """
    try:
        fp = open(path, "r")
    except IOError:
        return None
    try:
        dictionary = json.load(fp)
    except ValueError:
        return False
    fp.close()
    return dictionary


def slugify(name):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    # Create unicode sequences instead of characters
    name = unicodedata.normalize("NFKD", name)
    # Replace non letter and space characters
    slug = re.sub(r"[^\w\s-]", "", name).strip().lower()
    # Replace spaces with -
    slug = re.sub(r"[-\s]+", "-", slug)
    # Encode and decode to ascii to remove all none ascii characters
    return slug.encode("ascii", "ignore").decode()


def source_warning(file):
    if os.path.exists(os.path.join(os.path.dirname(file), "..", "README.md")):
        click.echo("\n" + (27 * ">") + " RUNNING FROM SOURCE FILE " + (27 * "<") + "\n")


def title_and_date_from_dir_name(path, pattern):
    title, start_date = None, None
    dir_pattern = re.compile(pattern)
    dir_name = os.path.basename(path)
    match = re.match(dir_pattern, dir_name)
    if match:
        try:
            start_date = datetime.datetime(
                int(match.group("year")), int(match.group("month")), int(match.group("day"))
            )
        except (IndexError, ValueError):
            # No valid date info could be found or the info was invalid.
            start_date = None
        try:
            title = match.group("title")
        except IndexError:
            title = None
    return title, start_date


def to_utc_timestamp(dt):
    if dt is None:
        return None
    return calendar.timegm(dt.timetuple())


def user_input(msg, case_sensitive=False):
    """ Ask user for input on the command line.
        Returns stripped string of input.
    """
    confirm = (input(u"%s" % msg)).strip()
    if case_sensitive:
        return confirm
    return confirm.lower()


def write_json(path, dictionary):
    """ Transform a python dictionary to JSON.
        Returns True if write is completed successfully
        Returns False if object could not be serialized
        Returns None if file could not be opened

        Writes to a temporary file first and moves the
        file to final location.
    """
    tmp_path = path + ".tmp"
    try:
        fp = open(tmp_path, "w")
    except IOError:
        return None
    try:
        json.dump(dictionary, fp, indent=2)
    except TypeError:
        fp.close()
        return False
    fp.close()
    os.rename(tmp_path, path)
    return True
