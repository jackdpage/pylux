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
import runpy
import logging
import libxpx.xpx as xpx

from pylux import __version__, get_data


def main():
    """Initialise the argument and config parsers."""
    print('This is Pylux, version '+__version__)
    # Initiate the argument parser and get launch arguments
    parser = argparse.ArgumentParser(prog='pylux',
       description='Create and modify OpenLighting Plot files')
    parser.add_argument('-v', '--version', action='version', 
        version='%(prog`)s '+__version__)
    parser.add_argument('-f', '--file', dest='file', 
        help='load this project file on launch')
    parser.add_argument('-g', '--gui', action='store_true', 
        help='launch Pylux with a GUI')
    parser.add_argument('-V', '--verbose', dest='verbose', action='count',
        help='set the verbosity of output')
    launch_args = parser.parse_args()
    # Load configuration
    config = configparser.ConfigParser()
    config.read([get_data('settings.conf', location='root'),
                 get_data('settings.conf', location='home')])
    # Handle verbosity
    verbosity_dict = {
        None: 30, 
        1: 20,
        2: 10,
        3: 1}
    print('Logging level is '+config['advanced']['log-'+str(verbosity_dict[launch_args.verbose])])
    # Load XPX file
    xpx_file = xpx.Document()
    if launch_args.file != None:
        xpx_file.load(launch_args.file)
        print('Using XPX file '+launch_args.file)
    else:
        print('No XPX file loaded')
    # Prepare globals for launch
    init_globals = {
        'PLOT_FILE': xpx_file,
        'CONFIG': config,
        'LOG_LEVEL': verbosity_dict[launch_args.verbose]}
    if launch_args.gui == True:
        print('Running in GUI mode\n')
        runpy.run_module('pylux.gui', init_globals=init_globals, 
                         run_name='pylux_root')
    else:
        print('Running in CLI mode\n')
        runpy.run_module('pylux.cli', init_globals=init_globals, 
                         run_name='pylux_root')


if __name__ == '__main__':
    main()
