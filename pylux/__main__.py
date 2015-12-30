#!/usr/bin/python3

# __main__.py is part of Pylux
#
# Pylux is a program for the management of lighting documentation
# Copyright 2015 Jack Page
# Pylux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pylux is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The __main__ module takes options and does stuff."""

import argparse
import os
import configparser
import sys
import gplotter
import plotter

from __init__ import __version__


def init():
    """Initialise the argument and config parsers."""
    # Initiate the argument parser
    parser = argparse.ArgumentParser(prog='pylux',
       description='Create and modify OpenLighting Plot files')
    parser.add_argument('-v', '--version', action='version', 
        version='%(prog)s '+__version__)
    parser.add_argument('-f', '--file', dest='file', 
        help='load this project file on launch')
    parser.add_argument('-i', '--interface', dest='interface', 
        choices=['cli','gui'], default='cli', help='user interface to use')
    global LAUNCH_ARGS
    LAUNCH_ARGS = parser.parse_args()

    # Initiate the config parser
    config_file = os.path.expanduser('~/.pylux/pylux.conf')
    global CONFIG
    CONFIG = configparser.ConfigParser()
    CONFIG.read(config_file)

    global OL_FIXTURES_DIR
    OL_FIXTURES_DIR = os.path.expanduser(CONFIG['Fixtures']['dir'])

    global PROMPT
    PROMPT = CONFIG['Settings']['prompt']+' '


def main():
    init()
    if LAUNCH_ARGS.interface == 'cli':
        plotter.main()
    elif LAUNCH_ARGS.interface == 'gui':
        gplotter.main()


if __name__ == '__main__':
    main()
