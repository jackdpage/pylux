"""Pylux is a suite for the management of lighting documentation"""

import os

__version__ = '0.1-alpha2'


_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, path)
