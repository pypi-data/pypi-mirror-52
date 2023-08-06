# coding: utf-8

import datetime
import json
import sys

from ..utils import execute
from ..utils import fatal_error
from .resize_im import resize_and_cache as resize_with_im
from .resize_sips import resize_and_cache as resize_with_sips

try:
    from resize_pil import resize_and_cache as resize_with_pil
except ImportError:
    resize_with_pil = False

EXIFTOOL_AVAILABLE, output = execute(["which", "exiftool"])

EXIF_TITLE_TAGS = ["ImageDescription", "UserComment", "Caption-Abstract", "Headline"]

EXIF_ROTATION_MAP = {
    1: 0,  # Horizontal (normal)
    2: 0,  # Mirrored horizontal
    3: 180,  # Rotated 180
    4: 0,  # Mirrored vertical
    5: 270,  # Mirrored horizontal then rotated 90 CCW
    6: 90,  # Rotated 90 CCW
    7: 90,  # Mirrored horizontal then rotated 90 CW
    8: 270,  # Rotated 90 C
}


def resize_and_cache(resize_with, *args, **kwargs):
    if not resize_with:
        # Based on performance. IM should only be set specifically
        # success, msg = execute(['convert', '--version'])
        # if success and 'ImageMagick' in msg:
        #     preference = 'im'
        if "darwin" in sys.platform:
            resize_with = "sips"
        else:
            resize_with = "pil"

    if resize_with == "im":
        return resize_with_im(*args, **kwargs)
    elif resize_with == "sips":
        return resize_with_sips(*args, **kwargs)
    else:
        if resize_with_pil:
            return resize_with_pil(*args, **kwargs)
        else:
            fatal_error("The Python Imaging Library cannot be found.")


def image_caption(raw_data, title_tag=False):
    if title_tag and raw_data.get(title_tag, False):
        return raw_data[title_tag].strip()
    for tag in EXIF_TITLE_TAGS:
        if raw_data.get(tag, False):
            return raw_data[tag].strip()
    return None


def image_date(raw_data):
    tstr = raw_data.get("DateTimeOriginal", None)
    if tstr is None:
        return None
    try:
        return datetime.datetime.strptime(tstr, "%Y:%m:%d %H:%M:%S")
    except ValueError:  # Somehow the format is wrong or all zero's
        return None


def image_geolocation(raw_data):
    if raw_data.get("GPSLongitude", False) and raw_data.get("GPSLatitude", False):
        return [raw_data["GPSLatitude"], raw_data["GPSLongitude"]]
    return (None, None)


def image_rotation(raw_data):
    orientation = raw_data.get("Orientation", 1)
    return EXIF_ROTATION_MAP.get(orientation, 0)


def image_exif_data(img_path):
    exif_data = {}
    if EXIFTOOL_AVAILABLE:
        success, raw_json = execute(["exiftool", "-j", "-n", img_path])
        if success:
            try:
                return json.loads(raw_json)[0]
            except ValueError:
                # Invalid json input. Let's pass for now
                pass
    return exif_data


def image_metadata(img_path, title_tag=False):
    raw_data = image_exif_data(img_path)
    return {
        "caption": image_caption(raw_data, title_tag),
        "rotation": image_rotation(raw_data),
        "raw_data": raw_data,
        "gps": image_geolocation(raw_data),
        "date": image_date(raw_data),
    }
