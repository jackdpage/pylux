# context.py is part of Pylux
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


from pylux.clihelper import resolve_input, Interface 
from importlib import import_module
import sys


class Context:
    """A context defines a set of commands that the user can access."""

    def init_commands(self):
        """Initialise the commands dictionary."""
        self.commands = {}
        self.register('c', self.utility_clear, 0)
        self.register('Q', self.utility_kill, 0)

    def process(self, inputs):
        function_definition = self.commands[inputs[0]]
        parsed_input = resolve_input(inputs, function_definition[1])
        function_definition[0](parsed_input)

    def set_globals(self, globals_dict):
        self.plot_file = globals_dict['PLOT_FILE']
        self.config = globals_dict['CONFIG']
        self.log_level = globals_dict['LOG_LEVEL']
        self.interface = Interface()

    def get_globals(self):
        globals_dict = {
            'PLOT_FILE': self.plot_file,
            'CONFIG': self.config,
            'LOG_LEVEL': self.log_level}
        return globals_dict

    def register(self, mnemonic, function, nargs):
        self.commands[mnemonic] = (function, nargs)

    def utility_clear(self, parsed_input):
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.exit()

    def utility_kill(self, parsed_input):
        print('Ignoring changes and exiting...')
        sys.exit()

