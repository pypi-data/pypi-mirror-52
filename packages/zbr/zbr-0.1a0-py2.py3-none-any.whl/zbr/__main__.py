#!/usr/bin/env python
# -*- coding: utf-8 -*-
from blessings import Terminal
import click
import logging
import sys

term = Terminal()

LOG = logging.getLogger(__name__)


def link(url, name):
    return "\033]8;;{}\033\\{}\033]8;;\033\\".format(url, name)


@click.command()
@click.option("--debug", "-d", default=False, help="Debug mode", is_flag=True)
def main(debug):
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    LOG.addHandler(handler)

    if sys.version_info.major < 3:
        reload(sys)  # noqa
        sys.setdefaultencoding("utf8")

    if debug:
        LOG.setLevel(level=logging.DEBUG)


if __name__ == "__main__":

    main()
