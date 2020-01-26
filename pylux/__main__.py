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

import argparse
import configparser

from pylux import cli


def main():

    print('This is Pylux, version 0.4.0')
    
    config = configparser.ConfigParser()
    config.read(['pylux.conf'])
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file')
    args = arg_parser.parse_args()

    init_globals = {'FILE': args.file, 'CONFIG': config, 'LOAD_LOC': ''}

    print('Launching command line interface')
    cli.main(init_globals)


if __name__ == '__main__':
    __package__ = 'pylux'
    main()
