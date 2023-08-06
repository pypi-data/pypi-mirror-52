# coding: utf-8

import click

from ..models import Size


def validate_resize_size(ctx, param, name):
    def _validate(name):
        if Size.get_size_by_name(name):
            return name
        raise click.BadParameter(
            "%s is not a valid size name. Please choose from: \n  - %s" % (name, "\n  - ".join(Size.all_names()))
        )

    if hasattr(name, "__iter__"):
        return [_validate(n) for n in name]
    else:
        return _validate(name)
