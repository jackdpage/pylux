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
from tabulate import tabulate
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

    def __init__(self):
        """Add the universal commands to the commands dictionary."""
        self.commands = {}
        self.register(Command('c', self.utility_clear, [], 
                      synopsis='Clear the screen.'))
        self.register(Command('h', self.utility_help, ['command'], 
                      synopsis='Get information about a command.'))
        self.register(Command('Q', self.utility_kill, [], 
                      synopsis='Exit the program without saving any changes.'))

    def post_init(self):
        """Initialisation phase run once globals are loaded."""
        return None

    def process(self, inputs):
        """From input, perform the required function call.

        Given the user input, search in the commands dictionary for 
        a command with the correct mnemonic. Then parse the input 
        using clihelper given the number of arguments required by 
        the function.

        Args:
            inputs: the user input, split by <space>.
        """
        command = self.commands[inputs[0]]
        parsed_input = resolve_input(inputs, command.nargs)
        command.function(parsed_input)

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
        self.post_init()

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

    def register(self, command):
        """Register a command in the command dictionary.

        Add a command to the list of commands the user can invoke.
        """
        self.commands[command.mnemonic] = command

    def log(self, level, message):
        level_name = self.config['advanced']['log-'+str(level)]
        if level >= self.log_level:
            print(''.join([level_name,':',self.name,':',message]))

    def utility_clear(self, parsed_input):
        """Utility to clear the screen using system call."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def utility_kill(self, parsed_input):
        """Utility to exit the program without warning."""
        sys.exit()

    def utility_help(self, parsed_input):
        """Print a list of all available commands."""
        if len(parsed_input) > 0:
            if parsed_input[0] not in self.commands:
                print('Error: Command does not exist')
            else:
                command = self.commands[parsed_input[0]]
                print('Usage:')
                usage = '    '+command.mnemonic
                for arg in command.arguments:
                    usage = usage+' '+arg
                print(usage)
                print('Description:')
                print('    '+str(command.synopsis))
        else:
            command_table = []
            for mnemonic in self.commands:
                table_row = []
                command = self.commands[mnemonic]
                usage = mnemonic
                for arg in command.arguments:
                    usage = usage+' '+arg
                table_row.append(usage)
                table_row.append(command.function.__name__)
                command_table.append(table_row)
            command_table.sort(key=lambda command: command[1])
            print(tabulate(command_table, 
                           headers=['Usage', 'Function'],
                           tablefmt=self.config['cli']['help-table-format']))


class Command:

    def __init__(self, mnemonic, function, arguments, synopsis=None):
        self.mnemonic = mnemonic
        self.function = function
        self.arguments = arguments
        self.nargs = len(self.arguments)
        self.synopsis = synopsis
