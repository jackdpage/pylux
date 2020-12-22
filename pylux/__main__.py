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

from ast import literal_eval
import argparse
import configparser
import importlib
import os.path
import pkg_resources
from pylux import document, interpreter
from pylux.lib import data, exception


def main():

    try:
        print('This is Pylux, version '+pkg_resources.require('pylux')[0].version)
    except pkg_resources.DistributionNotFound:
        print('This is Pylux. Running in local development mode')
    
    config = configparser.ConfigParser()
    # Set optionxform to str to maintain capitalisations in the config file, otherwise
    # everything is converted to lowercase. We need to retain capitals for some
    # cases such as the keys of the autocomplete options
    config.optionxform = str
    config.read([os.path.join(data.LOCATIONS[i], 'config.ini') for i in reversed(data.PRIORITY)])
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file', default=config['main']['default-file'])
    arg_parser.add_argument('-i', '--interface', default=config['main']['default-interface'])
    args = arg_parser.parse_args()

    # If the specified file or autosave file doesn't exist, create a blank
    # document there
    if not os.path.isfile(args.file):
        print('Creating new file at '+args.file)
        with open(args.file, 'w') as f:
            f.write('[]')
    config['main']['load_file'] = args.file
    print('Opening document at '+args.file)
    file = document.Document(load_path=args.file)
    print('Initialising command interpreter')
    server = interpreter.Interpreter(file, config)
    for extension in literal_eval(config['interpreter']['default-extensions']):
        try:
            server.register_extension(extension)
            print('Enabled {0} extension'.format(extension))
        except (exception.DependencyError, ModuleNotFoundError):
            print('Could not enable {0} extension due to missing ' 
                  'dependencies'.format(extension))
    try:
        interface_module = importlib.import_module('.'+args.interface, package='pylux.interface')
        print('Launching {0} interface'.format(args.interface))
    except ModuleNotFoundError:
        print('Could not load {0} interface. Reverting to fallback'.format(args.interface))
        interface_module = importlib.import_module('.fallback', package='pylux.interface')
    interface_module.main(server)


if __name__ == '__main__':
    __package__ = 'pylux'
    main()
