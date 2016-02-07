"""Pylux is a suite for the management of lighting documentation"""

import os

__version__ = '0.1.4'


_ROOT = os.path.abspath(os.path.dirname(__file__))
_HOME = os.path.expanduser('~/.pylux')

def get_data(path, location='auto'):
    if location == 'auto':
        if os.path.isfile(os.path.join(_HOME, path)):
            return os.path.join(_HOME, path)
        else:
            return os.path.join(_ROOT, path)
    elif location == 'root':
        return os.path.join(_ROOT, path)
    elif location == 'home':
        return os.path.join(_HOME, path)
