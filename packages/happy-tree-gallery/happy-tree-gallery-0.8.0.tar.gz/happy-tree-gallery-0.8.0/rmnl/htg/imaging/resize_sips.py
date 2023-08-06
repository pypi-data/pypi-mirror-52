# coding: utf-8

import os
import re
import shutil
from decimal import Decimal, ROUND_UP

from ..utils import execute

SIPS = "/usr/bin/sips"
HAS_JPEGTRAN, msg = execute(["which", "jpegtran"])


def _get_dimensions(path):
    def _get_wh(keyword):
        m = re.search(r"%s: (\d+)" % keyword, output)
        if m:
            return int(m.group(1))
        return 0

    success, output = execute([SIPS, "-g", "pixelWidth", "-g", "pixelHeight", path])
    if success:
        return _get_wh("pixelWidth"), _get_wh("pixelHeight")
    return 0, 0


def resize_and_cache(org_file, new_file, width, height, crop=False, rotation=0):
    def _failed(msg):
        os.unlink(new_file)
        return False, msg

    try:
        shutil.copy(org_file, new_file)
    except IOError:
        return _failed("Could not copy the original file to the new location.")

    # if the image has to fix within a square bounding box, it's easy with sips
    if width == height and not crop:
        if rotation:
            success, output = execute([SIPS, "-Z", width, "-r", rotation, new_file])
        success, output = execute([SIPS, "-Z", width, new_file])
        if not success:
            return _failed("Something went wrong while executing SIPS.")
        return _get_dimensions(new_file), False

    # Rotate first
    if rotation:
        # We prefer jpegtran, because it's rotations are lossless.
        if rotation in [90, 180, 270] and HAS_JPEGTRAN:
            success, output = execute(["jpegtran", "-rotate", rotation, "-outfile", new_file, new_file])
        elif rotation:
            success, output = execute([SIPS, "-r", rotation, new_file])
        if not success:
            return _failed("Could not rotate the image.")

    # Retreive the orignal dimensions
    orgW, orgH = _get_dimensions(new_file)
    if not orgW or not orgH:
        return _failed("Could not get original dimensions of the image file.")

    # Calculate the transformations
    arorg = Decimal(orgW) / Decimal(orgH)
    arnew = Decimal(width) / Decimal(height)

    new_w, new_h = False, False

    if crop:
        # the original is taller
        if arorg < arnew:
            # first resize to width
            new_w = width
            new_h = int((Decimal(width) / arorg).quantize(Decimal("1"), rounding=ROUND_UP))
        # The orginal image is wider
        elif arorg > arnew:
            new_h = height
            new_w = int((Decimal(height) * arorg).quantize(Decimal("1"), rounding=ROUND_UP))
        # Do nothing if the original picture has the same aspect ratio

    # check if the image is larger or not then the image we want to resize to.
    elif orgW > width or orgH > height:
        # The original image is taller
        if arorg < arnew:
            new_w = int((Decimal(height) * arorg).quantize(Decimal("1"), rounding=ROUND_UP))
            new_h = height
        # The orginal image is wider
        elif arorg > arnew:
            new_w = width
            new_h = int((Decimal(width) / arorg).quantize(Decimal("1"), rounding=ROUND_UP))

    if new_w and new_h:
        success, output = execute([SIPS, "-z", new_h, new_w, new_file])
        if not success:
            return _failed("Could not resize image.")

    if crop:
        success, output = execute([SIPS, "-c", height, width, new_file])
        if not success:
            return _failed("Could not crop the image.")

    return _get_dimensions(new_file), False
