#!/usr/bin/python3

# plotter.py is part of Pylux
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

import os
import sys
from __init__ import __version__
import plot
import importlib
    

class CliManager:
    """Manage some CLI interactivity and other functionality.

    Manage the interactive CLI lists, whereby a unique key which is 
    presented to the user on the CLI returns an object, without the 
    user having to specify the object itself. Also parse user input
    containing multi-word arguments.

    Attributes:
        option_list: a dictionary of the options presented to the 
            user on the CLI.
    """

    def __init__(self):
        """Create a dictionary for the options.

        Create a dictionary ready to populate with options, and add 
        an entry for the special 'this' with the value None.
        """
        self.option_list = {'this': None}

    def append(self, ref, object):
        """Add an object to the option list.

        Args:
            ref: the unique CLI identifier of the option being added.
            object: the object that should be returned if the user 
                selects this option.
        """
        self.option_list[ref] = object

    def get(self, ref):
        """Return the object of a user selection.

        Args:
            ref: the unique CLI identifier that the user selected.

        Returns:
            The object (which could be of any form) that is 
            associated with the reference in the option list.
        """
        try:
            ref = int(ref)
        finally:
            return self.option_list[ref]

    def clear(self):
        """Clear the option list."""
        self.option_list.clear()
        self.option_list['this'] = None

    def resolve_input(self, inputs_list, number_args):
        """Parse user input that contains a multi-word argument.

        From a list of user arguments which have already been split, 
        return a new list containing a set number of arguments, where 
        the last argument is a multi-word argument is a multi-word
        argument.

        Args:
            inputs_list: a list containing strings which have been 
                split from the user input using split(' ').
            number_args: the number of arguments the input should 
                contain, excluding the action itself. For example, 
                the add metadata action takes two arguments: the tag 
                and value.

        Returns:
            A list containing a list of the arguments, where the last 
            argument is a concatenation of any arguments that were 
            left after processing the rest of the inputs list. For 
            example, the metadata example above would return 
            ['ma', 'tag', 'value which can be many words long'].
        """
        i = 0
        parsed_input = []
        multiword_input = ""
        while i < number_args:
            parsed_input.append(inputs_list[i])
            i = i+1
        while number_args <= i <= len(inputs_list)-1:
            if multiword_input == "":
                multiword_input = multiword_input+inputs_list[i]
            else:
                multiword_input = multiword_input+' '+inputs_list[i]
            i = i+1
        parsed_input.append(multiword_input)
        return parsed_input

def get_olf_library():
    """Return a list of the installed OLF files."""
    library = os.listdir(OL_FIXTURES_DIR)
    for olf in library:
        olid = olf.split('.')[0]
        library[library.index(olf)] = olid
    return library


def get_command_list():
    """Display the help page."""
    text = ""
    with open('help.txt') as man:
        for line in man:
            text = text+line
    print(text)


def clear():
    """Clear the console."""


def purge_fixture(fixture):
    """Remove a fixture and all its DMX channels.

    Args:
        fixture: the XML object of the fixture to be purged.
    """
    registry = DmxRegistry(fixture.find('universe').text)
    start_addr = int(fixture.find('dmx_start_address').text)
    i = start_addr
    while i < start_addr+int(fixture.find('dmx_channels').text):
        registry.registry[i] = None
        i=i+1
    registry.save()
    remove_fixture(fixture)


def get_data_list(project_file, data_name):
    """Search through the fixtures list and return every value of data_name.

    Args:
        project_file: the Pylux plot file to search.
        data_name: the XML tag of the data.

    Returns:
        A list containing every value present for this XML tag.
    """
    fixture_list = project_file.root.find('fixtures')
    data_values = []

def main(plot_file, config):
    """The main user loop."""
    interface = CliManager()
    prompt = config['Settings']['prompt']+' '
    fixtures_dir = os.path.expanduser(config['Fixtures']['dir'])
    print('Welcome to Pylux! Type \'h\' to view a list of commands.')
    # Begin the main loop
    while True:
        user_input = input(config['Settings']['prompt']+' ')
        inputs = []
        for i in user_input.split(' '):
            inputs.append(i)

        # File actions
        if inputs[0] == 'fl':
            try:
                plot_file.load(inputs[1])
            except UnboundLocalError:
                print('Error: You need to specify a file path to load')

        elif inputs[0] == 'fs':
            plot_file.save()

        elif inputs[0] == 'fS':
            try:
                plot_file.saveas(inputs[1])
            except IndexError:
                print('Error: You need to specify a destination path!')

        elif inputs[0] == 'fg':
            print('Using plot file '+plot_file.file)

        # Metadata actions
        elif inputs[0] == 'ml':
            metadata = plot.Metadata(plot_file)
            for i in metadata.meta:
                print(i+': '+metadata.meta[i])

        elif inputs[0] == 'ma':
            metadata = plot.Metadata(plot_file)
            metadata.meta[inputs[1]] = interface.resolve_input(inputs, 2)[-1]
            metadata.save()

        elif inputs[0] == 'mr':
            metadata = plot.Metadata(plot_file)
            metadata.meta[inputs[1]] = None
            metadata.save()

        elif inputs[0] == 'mg':
            metadata = plot.Metadata(plot_file)
            print(inputs[1]+': '+metadata.meta[inputs[1]])

        # Fixture actions
        elif inputs[0] == 'xa':
            fixture = plot.Fixture(plot_file)
            try:
                fixture.new(inputs[1], fixtures_dir)
            except FileNotFoundError:
                print('Error: Couldn\'t find an OLF file with OLID '+inputs[1])
            else:
                fixture.add()
                fixture.save()
                interface.option_list['this'] = fixture

        elif inputs[0] == 'xc':
            src_fixture = interface.get(inputs[1])
            new_fixture = plot.Fixture(plot_file, fixtures_dir)
            new_fixture.clone(src_fixture)
            new_fixture.add()
            new_fixture.save()

        elif inputs[0] == 'xl':
            fixtures = plot.FixtureList(plot_file)
            i = 1
            interface.clear()
            for fixture in fixtures.fixtures:
                print('\033[4m'+str(i)+'\033[0m '+fixture.olid+', id: '+
                    fixture.uuid)
                interface.append(i, fixture)
                i = i+1

        elif inputs[0] == 'xf':
            try:
                key = inputs[1]
                value = interface.resolve_input(inputs, 2)[-1]
                fixtures = plot.FixtureList(plot_file, fixtures_dir)
                interface.clear()
                i = 1
                for fixture in fixtures.fixtures:
                    if key == 'olid':
                        test_value = fixture.olid
                    else:
                        try:
                            test_value = fixture.data[key]
                        except IndexError:
                            pass
                    if test_value == value:
                        print('\033[4m'+str(i)+'\033[0m '+fixture.olid+
                            ', id: '+fixture.uuid+', '+key+': '+value)
                        interface.append(i, fixture)
                        i = i+1
                        
            except IndexError:
                print('Error: You need to specify a key and value!')

        elif inputs[0] == 'xr':
            try:
                fixtures = plot.FixtureList(plot_file, fixtures_dir)
                fixtures.remove(interface.get(inputs[1]))
            except IndexError:
                print('Error: You need to run either xl or xf then specify the'
                      ' interface id of the fixture you wish to remove')

        elif inputs[0] == 'xi':
            fixture = interface.get(inputs[1])
            for data_item in fixture.data:
                print(data_item+': '+fixture.data[data_item])
            interface.option_list['this'] = fixture

        elif inputs[0] == 'xs':
            fixture = interface.get(inputs[1])
            fixture.data[inputs[2]] = interface.resolve_input(inputs, 3)[-1]
            fixture.save()
            interface.option_list['this'] = fixture

        elif inputs[0] == 'xA':
            fixture = interface.get(inputs[1])
            registry = plot.DmxRegistry(plot_file, inputs[2])
            registry.address(fixture, inputs[3])
            interface.option_list['this'] = fixture

        elif inputs[0] == 'xp':
            fixture = interface.get(inputs[1])
            registry = plot.DmxRegistry(plot_file, fixture.data['universe'])
            registry.unaddress(fixture)
            fixtures = plot.FixtureList(plot_file, fixtures_dir)
            fixtures.remove(fixture)

        # DMX registry actions
        elif inputs[0] == 'rl':
            try:
                registry = plot.DmxRegistry(plot_file, inputs[1])
                interface.clear()
                for channel in registry.registry:
                    uuid = registry.registry[channel][0]
                    func = registry.registry[channel][1]
                    print('\033[4m'+str(format(channel, '03d'))+
                        '\033[0m uuid: '+uuid+', func: '+func)
                    interface.append(channel, plot.Fixture(plot_file, uuid))
            except IndexError:
                print('You need to specify a DMX registry!')

        # Extension actions
        elif inputs[0][0] == ':':
            try:
                ext_module = importlib.import_module(inputs[0].split(':')[1])
            except ImportError:
                print('No extension with this name!')
            else:
                try:
                    ext_module.main(plot_file, interface)
                except AttributeError:
                    print('This extension is not configured correctly!')

        # Utility actions
        elif inputs[0] == 'h':
            get_command_list()

        elif inputs[0] == 'c':
            os.system('cls' if os.name == 'nt' else 'clear')

        elif inputs[0] == 'q':
            print('Autosaving changes...')
            plot_file.save()
            sys.exit()

        elif inputs[0] == 'Q':
            print('Ignoring changes and exiting...')
            sys.exit()

        else:
            print('Error: Command doesn\'t exist.') 
            print('Type \'h\' for a list of available commands.')


# Check that the program isn't imported, then run main
if __name__ == '__main__':
    main()
