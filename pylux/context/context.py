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
import os


class Context:
    """A context defines a set of commands that the user can access.

    When a user enters a context, all commands that the user enters 
    are processed by the context using the process function. This 
    base context class provides a globals piping infrastructure, a 
    processing function and some commands that should be available 
    in all contexts.

    Attributes:
        commands: a dictionary of tuples defining commands the user 
            can invoke.
        plot_file: the PlotFile object containing the plot file.
        config: the parsed configuration file.
        log_level: the logging level defined on launch.
        interface: the Interface object being used.
    """

    def init_commands(self):
        """Add the universal commands to the commands dictionary."""
        self.commands = {}
        self.register('c', self.utility_clear, 0)
        self.register('Q', self.utility_kill, 0)

    def process(self, inputs):
        """From input, perform the required function call.

        Given the user input, search in the commands dictionary for 
        a command with the correct mnemonic. Then parse the input 
        using clihelper given the number of arguments required by 
        the function.

        Args:
            inputs: the user input, split by <space>.
        """
        function_definition = self.commands[inputs[0]]
        parsed_input = resolve_input(inputs, function_definition[1])
        function_definition[0](parsed_input)

    def set_globals(self, globals_dict):
        """Set globals from a dictionary.

        Set the attributes that are considered 'globals' from the 
        contents of globals_dict.

        Args:
            globals_dict: a dictionary containing the values of the 
                predefined globals.
        """
        self.plot_file = globals_dict['PLOT_FILE']
        self.config = globals_dict['CONFIG']
        self.log_level = globals_dict['LOG_LEVEL']
        self.interface = Interface()

    def get_globals(self):
        """Get the current globals dictionary.

        Returns a dictionary containing the globals in their current 
        state, ready to be passed into another context using the 
        set_globals command.

        Returns:
            A dictionary containing the 'global' attributes.
        """
        globals_dict = {
            'PLOT_FILE': self.plot_file,
            'CONFIG': self.config,
            'LOG_LEVEL': self.log_level}
        return globals_dict

    def register(self, mnemonic, function, nargs):
        """Register a command in the command dictionary.

        Add a command to the list of commands the user can invoke.

        Args:
            mnemonic: the mnemonic the user should type to invoke 
                this command. In general should be only two 
                characters long.
            function: a reference to the function that this command 
                calls.
            nargs: the number of arguments this command takes.
        """
        self.commands[mnemonic] = (function, nargs)

    def utility_clear(self, parsed_input):
        """Utility to clear the screen using system call."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def utility_kill(self, parsed_input):
        """Utility to exit the program without warning."""
        print('Ignoring changes and exiting...')
        sys.exit()

