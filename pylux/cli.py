# cli.py is part of Pylux
#
# Pylux is a program for the management of lighting documentation
# Copyright 2015 Jack Page
#
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


import logging
from importlib import import_module


def get_context(context_name):
    module_name = 'pylux.context.'+context_name
    try:
        context_module = import_module(module_name)
    except ImportError:
        print('Error: Context does not exist')
        return None
    else:
        context_class = context_module.get_context()
        return context_class


def main():
    context = get_context(CONFIG['cli']['default-context'])
    globals_dict = {
        'PLOT_FILE': PLOT_FILE,
        'CONFIG': CONFIG,
        'LOG_LEVEL': LOG_LEVEL}
    context.set_globals(globals_dict)
    logging.basicConfig(level=LOG_LEVEL)
    print('Welcome to Pylux! Type \'h\' to view a list of commands.')
    while True:
        user_input = input('(pylux:'+context.name+') ')
        inputs = user_input.split(' ')

        if len(user_input) > 0:
            if inputs[0] == '::':
                globals_dict = context.get_globals()
                context = get_context('editor')
                context.set_globals(globals_dict)

            elif inputs[0][0] == ':':
                globals_dict = context.get_globals()
                if get_context(inputs[0].split(':')[1]) is not None:
                    context = get_context(inputs[0].split(':')[1])
                    context.set_globals(globals_dict)

            elif inputs[0] in context.commands:
                context.process(inputs)

            else:
                print('Error: Command doesn\'t exist.') 


if __name__ == 'pylux_root':
    main()
