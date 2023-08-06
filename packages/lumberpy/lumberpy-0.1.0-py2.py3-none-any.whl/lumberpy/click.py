from typing import Callable, Optional

import click


def options(fn: Optional[Callable] = None) -> Callable:
    """decorator to add click options."""

    # allow for two ways to decorate:
    # @lumberpy.click.options
    # @lubermpy.click.options()
    if fn is None:
        return options

    click.option("--lumberpy-config-path", type=click.Path())(fn)
    click.option("-v", "--verbose", count=True)(fn)
    return fn
