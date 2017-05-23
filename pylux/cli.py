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

from importlib import import_module


def get_context(context_name):
    module_name = 'context.'+context_name
    context_module = import_module(module_name)
    context_class = context_module.get_context()
    return context_class


def main(init_globals):
    globals = init_globals
    context = get_context(globals['CONFIG']['cli']['default-context'])
    context.set_globals(globals)
    print('Welcome to Pylux! Type \'h\' to view a list of commands.')
    while True:
        user_input = input('(pylux:'+context.name+') ')
        inputs = user_input.split(' ')

        if len(user_input) > 0:
            if inputs[0] == '::':
                globals_dict = context.get_globals()
                context = get_context(globals['CONFIG']['cli']['default-context'])
                context.set_globals(globals_dict)
            elif inputs[0][0] == ':':
                globals_dict = context.get_globals()
                context = get_context(inputs[0].split(':')[1])
                context.set_globals(globals_dict)
            elif inputs[0] in context.commands:
                context.process(inputs)
            else:
                print('Command does not exist')
