# -*- coding: utf-8 -*-
"""Utility module
"""
from os import path


def read_pkg_version() -> str:
    """Read the version of this package.
    """
    pkg_root = path.join(path.dirname(path.abspath(__file__)))
    with open(path.join(pkg_root, 'VERSION'), mode='r') as fp:
        return fp.read().strip()
