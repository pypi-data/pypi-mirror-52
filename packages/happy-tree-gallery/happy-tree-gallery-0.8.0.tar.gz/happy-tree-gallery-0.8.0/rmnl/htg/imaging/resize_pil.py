# coding: utf-8

import math
from decimal import Decimal

try:
    from PIL import Image
except ImportError:
    import Image


def resize_and_cache(org_file, new_file, new_width, new_height, crop=False, rotation=0):
    """ Creates a resized image of the original file and saves it
        to a new location
        If crop is true the image will be cropped to fit the exact sizes
        otherwise the image will fit within the sizes.
    """
    try:
        im = Image.open(org_file)
    except IOError:
        return False, "Could not open orignal file."

    if rotation:
        im = im.rotate(rotation)

    arorg = Decimal(im.size[0]) / Decimal(im.size[1])
    arnew = Decimal(new_width) / Decimal(new_height)

    if crop:
        # The orginal image is wider
        if arorg > arnew:
            width = im.size[1] * arnew
            left = int(math.fabs((im.size[0] - width) / 2))
            box = (left, 0, im.size[0] - left, im.size[1])
        # The original image is taller
        elif arorg < arnew:
            height = im.size[0] / arnew
            top = int(math.fabs((im.size[1] - height) / 2))
            box = (0, top, im.size[0], im.size[1] - top)
        # The original picture has the same aspect ration
        else:
            box = (0, 0, im.size[0], im.size[1])
        new = im.crop(box)
        new.thumbnail((new_width, new_height), Image.ANTIALIAS)

    else:
        # check if the image is larger or not then the image we want to
        # resize to.
        if im.size[0] > new_height or im.size[1] > new_height:
            # default
            width = Decimal(new_width)
            height = Decimal(new_height)
            # The orginal image is wider
            if arorg > arnew:
                height = Decimal(new_height) / arorg
            # The original image is taller
            elif arorg < arnew:
                width = Decimal(new_width) / arorg
            new = im.crop((0, 0, im.size[0], im.size[1]))
            new.thumbnail((width, height), Image.ANTIALIAS)
        else:
            new = im

    try:
        new.save(new_file, "JPEG", quality=95)
    except IOError:
        return False, "Could not save resized image file."

    width, height = new.size[0], new.size[1]
    del (im, new)
    return (width, height), False
