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
import importlib
import os.path

from pylux import document


def main():

    print('This is Pylux, version 0.4.0')
    
    config = configparser.ConfigParser()
    config.read(['pylux.conf'])
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file', default=config['main']['default-file'])
    arg_parser.add_argument('-i', '--interface', default=config['main']['default-interface'])
    args = arg_parser.parse_args()

    # If the specified file or autosave file doesn't exist, create a blank json document there
    if not os.path.isfile(args.file):
        document.write_to_file([], args.file)

    config['main']['load_file'] = args.file
    init_globals = {'FILE': args.file, 'CONFIG': config}

    try:
        print('Launching {0} interface'.format(args.interface))
        try:
            interface_module = importlib.import_module('.'+args.interface, package='pylux.interface')
        except ModuleNotFoundError:
            print('One or more dependencies for {0} were missing. Reverting to fallback interface...'.format(args.interface))
            interface_module = importlib.import_module('.fallback', package='pylux.interface')
    except ModuleNotFoundError:
        print('Couldn\'t source {0} interface. Reverting to fallback interface...'.format(args.interface))
        interface_module = importlib.import_module('.fallback', package='pylux.interface')
    interface_module.main(init_globals)


if __name__ == '__main__':
    __package__ = 'pylux'
    main()
