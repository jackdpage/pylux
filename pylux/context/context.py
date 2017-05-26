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

import clihelper
from clihelper import resolve_input, Interface
import document
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
        self.register(Command('c', self.utility_clear, []))
        self.register(Command('h', self.utility_help, [
            ('command', False, 'The command to access information about')]))
        self.register(Command('q', self.utility_exit, []))
        self.register(Command('Q', self.utility_kill, []))

        self.register(Command('fo', self.file_open, [
            ('path', True, 'Path of the file to load.')]))
        self.register(Command('fw', self.file_write, []))
        self.register(Command('fg', self.file_get, []))
        self.register(Command('fs', self.file_set, [
            ('path', True, 'Path to set load location to.')]))

        self.register(Command('l', self.generic_list, []))
        self.register(Command('s', self.generic_set, [
            ('type', True, 'The type of object to alter'),
            ('ref', True, 'The reference of the object to alter'),
            ('k', True, 'Key of the data to set'),
            ('v', True, 'Value to set the data to')]))
        self.register(Command('r', self.generic_remove, [
            ('type', True, 'The type of object to remove'),
            ('ref', True, 'The reference of the object to remove')]))


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
        if len(inputs) < command.nargs:
            self.log(30, 'Not enough arguments, type \'h '+
                         command.mnemoic+'\' for usage.')
        elif len(inputs) >= command.maxargs:
            parsed_input = resolve_input(inputs, command.maxargs)
            command.function(parsed_input)
        else:
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
        self.interface = Interface()
        self.load_location = globals_dict['LOAD_LOC']
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
            'LOAD_LOC': self.load_location}
        return globals_dict

    def register(self, command):
        """Register a command in the command dictionary.

        Add a command to the list of commands the user can invoke.
        """
        self.commands[command.mnemonic] = command

    def utility_clear(self, parsed_input):
        '''Clear the screen.'''
        os.system('cls' if os.name == 'nt' else 'clear')

    def utility_exit(self, parsed_input):
        '''Quit the program and save the plot file to disk.'''
        self.file_write(parsed_input)
        self.utility_kill(parsed_input)

    def utility_kill(self, parsed_input):
        '''Quit the program without saving any changes.'''
        sys.exit()

    def utility_help(self, parsed_input):
        '''Access information about a command or list all commands.'''
        if len(parsed_input) > 0:
            if parsed_input[0] not in self.commands:
                self.log(30, 'Command does not exist')
            else:
                command = self.commands[parsed_input[0]]
                print('Usage:')
                usage = '    '+command.mnemonic
                for arg in command.arguments:
                    usage = usage+' '+arg[0]
                print(usage)
                print('Description:')
                print('    '+str(command.function.__doc__))
                print('Arguments:')
                for arg in command.arguments:
                    if arg[1]:
                        req = '(Required)'
                    else:
                        req = '(Optional)'
                    print(''.join(['    ', arg[0], ' ', req, ': ', arg[2]]))
        else:
            command_table = []
            for mnemonic in self.commands:
                table_row = []
                command = self.commands[mnemonic]
                usage = mnemonic
                for arg in command.arguments:
                    usage = usage+' '+arg[0]
                table_row.append(usage)
                table_row.append(command.function.__name__)
                command_table.append(table_row)
            command_table.sort(key=lambda command: command[1])
            print(tabulate(command_table, 
                           headers=['Usage', 'Function'],
                           tablefmt=self.config['cli']['help-table-format']))

    def generic_list(self, parsed_input):
        """List all objects in the plot file."""
        for obj in self.plot_file:
            clihelper.print_object(obj)

    def generic_set(self, parsed_input):
        """Set an arbitrary tag to a value."""
        all_of_type = document.get_by_type(self.plot_file, parsed_input[0])
        refs = clihelper.resolve_references(parsed_input[1])
        for obj in all_of_type:
            if obj['ref'] in refs:
                obj[parsed_input[2]] = parsed_input[3]

    def generic_remove(self, parsed_input):
        """Remove an object from the document."""
        all_of_type = document.get_by_type(self.plot_file, parsed_input[0])
        refs = clihelper.resolve_references(parsed_input[1])
        for obj in all_of_type:
            if obj['ref'] in refs:
                document.remove_by_uuid(self.plot_file, obj['uuid'])

    def file_open(self, parsed_input):
        '''Open a new plot file, discarding any present buffer.'''
        self.load_location = parsed_input[0]
        s = document.get_string_from_file(parsed_input[0])
        self.plot_file = document.get_deserialised_document_from_string(s)

    def file_write(self, parsed_input):
        '''Write the contents of the file buffer to the original path.'''
        document.write_to_file(self.plot_file, self.load_location)

    def file_get(self, parsed_input):
        '''Print the current load location.'''
        print(self.load_location)

    def file_set(self, parsed_input):
        '''Set the load location to something else.'''
        self.load_location = parsed_input[0]

class Command:

    def __init__(self, mnemonic, function, arguments):
        self.mnemonic = mnemonic
        self.function = function
        self.synopsis = self.function.__doc__
        self.arguments = arguments
        self.maxargs = len(self.arguments)
        self.nargs = 0
        for arg in self.arguments:
            if arg[1]:
                self.nargs += 1
