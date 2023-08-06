# coding: utf-8

from ..utils import execute


def _get_dimensions(path):
    success, output = execute(["convert", path, "-ping", "-format", "%wx%h", "info:"])
    if not success:
        return 0, 0
    return [int(i) for i in output.split("x")]


def resize_and_cache(org_file, new_file, width, height, crop=False, rotation=0):
    command = ["convert", org_file]
    geometry = "%sx%s" % (width, height)
    if rotation:
        command += ["-rotate", rotation]
    if crop:
        command += ["-resize", geometry + "^", "-gravity", "center", "-extent", geometry]
    else:
        command += ["-resize", geometry + ">"]
    command.append(new_file)
    success, msg = execute(command)
    if success:
        return _get_dimensions(new_file), False
    else:
        return False, "Could not convert image."
