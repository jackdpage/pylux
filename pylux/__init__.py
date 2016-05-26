"""Pylux is a suite for the management of lighting documentation"""

import os
import pkg_resources

__version__ = pkg_resources.get_distribution('pylux').version


_ROOT = os.path.abspath(os.path.dirname(__file__))
_HOME = os.path.expanduser('~/.pylux')
_USRD = os.path.abspath('/usr/share/pylux')

# Priority of data locations, high to low
PRIORITY = [_ROOT, _USRD, _HOME]

def get_data(path, location='auto'):
    if location == 'auto':
        for loc in PRIORITY:
            if os.path.isfile(os.path.join(loc, path)):
                return os.path.join(loc, path)
        return False
    elif location == 'root':
        if os.path.isfile(os.path.join(_ROOT, path)):
            return os.path.join(_ROOT, path)
        else:
            return False
    elif location == 'home':
        if os.path.isfile(os.path.join(_HOME, path)):
            return os.path.join(_HOME, path)
        else:
            return False
    elif location == 'usr':
        if os.path.isfile(os.path.join(_USRD, path)):
            return os.path.join(_USRD, path)
        else:
            return False
