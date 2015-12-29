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

import xml.etree.ElementTree as ET
import uuid
import argparse
import os
import configparser
import os.path
import sys
import gplotter
from __init__ import __version__


def init():
    """Initialise the argument and config parsers."""
    # Initiate the argument parser
    parser = argparse.ArgumentParser(prog='pylux',
       description='Create and modify OpenLighting Plot files')
    parser.add_argument('-v', '--version', action='version', 
        version='%(prog)s '+__version__)
    parser.add_argument('-f', '--file', dest='file', 
        help='load this project file on launch')
    parser.add_argument('-i', '--interface', dest='interface', 
        choices=['cli','gui'], default='cli', help='user interface to use')
    global LAUNCH_ARGS
    LAUNCH_ARGS = parser.parse_args()

    # Initiate the config parser
    global config_file
    config_file = os.path.expanduser('~/.pylux/pylux.conf')
    config = configparser.ConfigParser()
    config.read(config_file)

    global OL_FIXTURES_DIR
    OL_FIXTURES_DIR = os.path.expanduser(config['Fixtures']['dir'])

    global PROMPT
    PROMPT = config['Settings']['prompt']+' '


class FileManager:
    """Manage the Pylux plot project file.

    Attributes:
        file: the path of the project file.
        tree: the parsed XML tree.
        root: the root element of the XML tree.
    """

    def load(self, path):
        """Load a project file.

        Args:
            path: the location of the file to load.
        """
        self.file = path
        try:
            self.tree = ET.parse(self.file)
        except FileNotFoundError:
            print('The file you are trying to load doesn\'t exist!')
        self.root = self.tree.getroot()
        global META_MANAGER
        META_MANAGER = MetaManager(self)

    def save(self):
        """Save the project file to its original location."""
        self.tree.write(self.file, encoding='UTF-8', xml_declaration=True)

    def saveas(self, path):
        """Save the project file to a new location.

        Args:
            path: the location to save the file to.
        """
        self.tree.write(path, encoding='UTF-8', xml_declaration=True)

    
class DmxRegistry:
    """Manages DMX registries.

    Attributes:
        registry: the registry as a Python dictionary.
        universe: the universe id of the registry.
        xml_registry: the XML tree of the registry. Is False if the 
            registry doesn't exist in XML.
    """

    def __init__(self, universe):
        """Create a new Python registry.

        Creates a new Python registry with the id universe. Then 
        searches the project file for a registry with the same id. If 
        one is found, loads that data into the Python registry, if 
        the registry doesn't exist in XML, creates one and adds it to 
        the tree.

        Args:
            universe: the universe id of the registry to be created.
        """
        self.registry = {}
        self.universe = universe
        self.xml_registry = False
        # Search for this universe in the XML file
        xml_registries = PROJECT_FILE.root.findall('dmx_registry')
        for xml_registry in xml_registries: 
            testing_universe = xml_registry.get('universe')
            if testing_universe == self.universe:
                self.xml_registry = xml_registry
                break # Return XML registry if it exists
        # Create a new XML registry if one doesn't exist
        if self.xml_registry == False:
            self.xml_registry = ET.Element('dmx_registry')
            self.xml_registry.set('universe', self.universe)
            PROJECT_FILE.root.append(self.xml_registry)
        # Populate the Python registry if an XML registry was found
        else:            
            for channel in xml_registry:
                address = int(channel.get('address'))
                uuid = channel.find('fixture_uuid').text
                function = channel.find('function').text
                self.registry[address] = (uuid, function)

    def save(self):
        """Saves the Python registry to the XML tree.

        Saves the contents of the Python DMX registry to the registry in 
        XML and deletes any XML channels that no longer exist in the 
        Python registry.
        """
        # Add a new XML entry
        def add_xml_entry(self, address, uuid, function):
            self.registry[address] = (uuid, function)
            new_channel = ET.Element('channel')
            new_channel.set('address', str(address))
            new_uuid = ET.SubElement(new_channel, 'fixture_uuid')
            new_uuid.text = uuid
            new_function = ET.SubElement(new_channel, 'function')
            new_function.text = function
            self.xml_registry.append(new_channel)
    
        # Edit an existing XML entry
        def edit_xml_entry(self, xml_channel, new_uuid, new_function):
            xml_channel.find('fixture_uuid').text = new_uuid
            xml_channel.find('function').text = function

        # Search a channel with address in XML
        def get_xml_channel(self, address):
            for channel in self.xml_registry:
                found_address = channel.get('address')
                if found_address == str(address):
                    return channel
                    break

        # Iterate over the Python registry
        for address in self.registry:
            if self.registry[address] != None:
                uuid = self.registry[address][0]
                function = self.registry[address][1]
                xml_channel = get_xml_channel(self, address)
                if xml_channel == None:
                    add_xml_entry(self, address, uuid, function)
                else:
                    edit_xml_entry(self, xml_channel, uuid, function)
            else:
                self.xml_registry.remove(get_xml_channel(self, address))

    def get_occupied(self):
        """Returns a list of occupied DMX channels.

        Returns:
            A list containing the addresses of the occupied channels 
            in the Python registry.
        """
        occupied = []
        for address in self.registry:
            occupied.append(address)
        occupied.sort()
        return occupied

    def get_start_address(self, n):
        """Returns a recommended start address for a new fixture.

        Finds the next run of n free DMX channels in the Python 
        registry or returns 1 if no channels are occupied.

        Args:
            n: the number of DMX channels required by the new fixture.

        Returns:
            An integer giving the ideal DMX start address.
        """
        occupied = self.get_occupied()
        if occupied == []:
            print('All channels are free so choosing start address 1')
            return 1
        for i in occupied:
            free_from = i+1
            if occupied[-1] == i:
                next_test = 513
            else:
                next_test = occupied[occupied.index(i)+1]
            free_until = next_test-1
            if free_until-free_from >= 0:
                print('Found free channels in the range '+str(free_from)+':'
                    +str(free_until))
            if free_until-free_from+1 >= n:
                print('Automatically chose start address '+str(free_from))
                return free_from

    def list(self):
        """Print a list of the used channels in the registry.

        Print a list of the used channels in the registry, along with 
        the UUID of the fixture they control and their function.
        """
        for channel in self.registry:
            print(str(format(channel, '03d'))+' uuid: '+
                self.registry[channel][0]+', func: '+self.registry[channel][1])


class Fixture:
    """Manage the addition of fixtures to the plot file.

    Attributes:
        olid: the OLID of the fixture.
        uuid: the UUID of the fixture.
        data: a dictionary containing all other data for the fixture.
        dmx: a list of the functions of the DMX channels used by this 
            fixture.
        dmx_num: the number of DMX channels required by this fixture.
    """

    def __init__(self):
        """Create a new fixture in Python."""
        self.data = {}
        self.dmx = []

    def new(self, olid):
        """Make this fixture as a new fixture.

        Given an OLID, create a new fixture, assign a UUID and load 
        the constants from the OLF file into the data dictionary.

        Args:
            olid: the OLID of the new fixture.
        """
        olf_tree = ET.parse(OL_FIXTURES_DIR+olid+'.olf')
        olf_root = olf_tree.getroot()
        self.olid = olid # OLID was specified on creation
        self.uuid = str(uuid.uuid4()) # Random UUID assigned
        constants_xml = olf_root.find('constants')
        dmx_xml = olf_root.find('dmx_channels')
        dmx_chans = []
        for channel in dmx_xml:
            dmx_chans.append(channel.tag)
        dmx_num = len(dmx_chans)
        # Add constants from OLF file
        for constant in constants_xml:
            self.data[constant.tag] = constant.text
        self.data['dmx_channels'] = str(dmx_num)

    def add(self):
        """Create an XML object for the fixture and add to the tree.

        Generate a fixture XML object and populate it with the 
        contents of the data dictionary, then add the newly created 
        fixture to the XML tree.
        """
        fixture_list = PROJECT_FILE.root.find('fixtures')
        new_fixture = ET.Element('fixture')
        new_fixture.set('olid', self.olid)
        new_fixture.set('uuid', self.uuid)
        # Iterate over data 
        for data_item in self.data:
            new_detail = ET.SubElement(new_fixture, data_item)
            new_detail.text = self.data[data_item]
        fixture_list.append(new_fixture)
        self.xml_fixture = new_fixture

    def load(self, fixture):
        """Load existing fixture data from XML.

        Load the contents of an existing fixture in the XML document 
        into this Python fixture object.

        Args:
            fixture: the XML fixture object to load.
        """
        self.xml_fixture = fixture
        self.olid = fixture.get('olid')
        self.uuid = fixture.get('uuid')
        for data_item in fixture:
            self.data[data_item.tag] = data_item.text
        # Load DMX info from OLF file
        olf_tree = ET.parse(OL_FIXTURES_DIR+self.olid+'.olf')
        olf_root = olf_tree.getroot()
        dmx_xml = olf_root.find('dmx_channels')
        for channel in dmx_xml:
            self.dmx.append(channel.tag)
        self.dmx_num = len(self.dmx)

    def edit(self, tag, value):
        """Edit a piece of data in the fixture.

        Args:
            tag: the data value to edit.
            value: the new value to set.
        """
        self.data[tag] = value

    def clone(self, src_fixture):
        """Clone a fixture.

         an exact copy of a fixture in XML, but assign a new 
        UUID.

        Args:
            src_fixture: source Python fixture object to copy.
        """
        self.uuid = str(uuid.uuid4())
        self.olid = src_fixture.olid
        for data_item in src_fixture.data:
            self.data[data_item] = src_fixture.data[data_item]

    def save(self):
        """Save the Python fixture object to XML."""
        # Add a new data item
        def add_xml_data(self, tag, value):
            new_data_item = ET.Element(tag)    
            new_data_item.text = value
            self.xml_fixture.append(new_data_item)

        # Edit an existing data item
        def edit_xml_data(self, tag, new_value):
            self.xml_fixture.find(tag).text = new_value

        # Search for data in XML
        def get_xml_data(self, tag):
            try:
                return self.xml_fixture.find(tag)
            except AttributeError:
                return None

        # Iterate over the data dictionary
        for data_item in self.data:
            xml_data = get_xml_data(self, data_item)
            if xml_data == None:
                add_xml_data(self, data_item, self.data[data_item])
            else:
                edit_xml_data(self, data_item, self.data[data_item])
        # Iterate over XML fixture to remove empty data
        for data_item in self.xml_fixture:
            data_name = data_item.tag
            if data_name not in self.data:
                self.xml_fixture.remove(data_item)

class MetaManager:
    """Manages the metadata section of the XML file.

    Attributes:
        meta_values: the XML object containing a the metadata.
    """

    def __init__(self, project_file):
        """Find the metadata in XML and add to the attribute.

        Args:
            project_file: the FileManager object of the project file.
        """
        self.meta_values = project_file.root.find('metadata')

    def list_meta(self):
        """Print the values of all metadata."""
        for metaitem in self.meta_values:
            print(metaitem.tag+': '+metaitem.text)

    def add_meta(self, tag, value):
        """Add a new piece of metadata.

        Args:
            tag: the XML tag of the new metadata.
            value: the value of the new metadata.
        """
        new_meta = ET.Element(tag)
        new_meta.text = value
        self.meta_values.append(new_meta)

    def remove_meta(self, tag):
        """Remove a piece of metadata from XML.

        Args:
            tag: the XML tag of the metadata to remove.
        """
        for metaitem in self.meta_values:
            test_tag = metaitem.tag
            if test_tag == tag:
                self.meta_values.remove(metaitem)

    def get(self, tag):
        """Return the value of a piece of metadata.

        Args:
            tag: the XML tag of the metadata to return.

        Returns:
            A string containing the XML text of the metadata.
        """
        for metaitem in self.meta_values:
            test_tag = metaitem.tag
            if test_tag == tag:
                return metaitem.text
                break

class PositionManager:
    """NYI"""
    def get_fixture(uuid):
        fixture_list = PROJECT_FILE.root.find('fixtures')
        for fixture in fixture_list:
            test_uuid = fixture.get('uuid')
            if test_uuid == uuid:
                return fixture
                break

    def position(uuid, position):
        fixture_list = PROJECT_FILE.root.find('fixtures')
        fixture = PositionManager.get_fixture(uuid)
        posX = ET.SubElement(fixture, 'posX')
        posX.text = position[0]
        posY = ET.SubElement(fixture, 'posY')
        posY.text = position[1]
        posZ = ET.SubElement(fixture, 'posZ')
        posZ.text = position[2]


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
        """Create an empty dictionary for the options."""
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

    def resolve_input(inputs_list, number_args):
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
    os.system('cls' if os.name == 'nt' else 'clear')


def remove_fixture(fixture):
    """Remove a fixture from the plot.

    Args:
        fixture: the XML object of the fixture to be removed.
    """
    fixture_list = PROJECT_FILE.root.find('fixtures')
    fixture_list.remove(fixture)
    return fixture


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


def list_fixture_info(fixture):
    """Print the user-defined values of a fixture.

    Args:
        fixture: the XML object of the fixture.
    """
    for variable in fixture:
        print(variable.tag+': '+variable.text)

def list_fixtures():
    """Print a list of all fixtures.

    Print a list of all the fixtures in the plot and assign a unique 
    CLI identifier to each one, so that the user can pass them into 
    further commands.
    """
    fixture_list = PROJECT_FILE.root.find('fixtures')
    INTERFACE_MANAGER.clear()
    i=1
    for fixture in fixture_list:
        olid = fixture.get('olid')
        uuid = fixture.get('uuid')
        print('['+str(i)+'] '+olid+', id: '+uuid)
        INTERFACE_MANAGER.append(i, fixture)
        i = i+1


def filter_fixtures(key, value):
    """Display a list of fixtures with a certain property.

    Print a list of fixtures which have a certain value for a key 
    and assign a unique CLI identifier to each one, so that the user 
    can pass them into further commands.

    Args:
        key: the XML tag to test.
        value: the XML value of the fixtures that should be returned.
    """
    fixture_list = PROJECT_FILE.root.find('fixtures')
    INTERFACE_MANAGER.clear()
    i=1
    for fixture in fixture_list:
        if key == 'olid':
            test_value = fixture.get('olid')
            if test_value == value:
                uuid = fixture.get('uuid')
                print('['+str(i)+'] '+test_value+', id: '+uuid)
                INTERFACE_MANAGER.append(i, fixture)
                i = i+1
        else:        
            try:
                test_value = fixture.find(key).text
                if test_value == value:
                    olid = fixture.get('olid')
                    uuid = fixture.get('uuid')
                    print('['+str(i)+'] '+olid+', id: '+uuid+', '+key+': '+
                        value)
                    INTERFACE_MANAGER.append(i, fixture)
                    i = i+1
            except AttributeError:
                continue


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
    for fixture in fixture_list:
        try:
            data_values.append(fixture.find(data_name).text)
        except AttributeError:
            continue
    data_values = list(set(data_values))
    data_values.sort()
    return data_values

def cli_loop():
    """The main user loop."""
    init()
    global PROJECT_FILE
    PROJECT_FILE = FileManager()
    global INTERFACE_MANAGER
    INTERFACE_MANAGER = CliManager()
    print('Pylux 0.1')
    print('Using configuration file '+config_file)
    # If a project file was given at launch, load it
    if LAUNCH_ARGS.file != None:
        PROJECT_FILE.load(os.path.expanduser(LAUNCH_ARGS.file))
        print('Using project file '+PROJECT_FILE.file) 
    print('Welcome to Pylux! Type \'h\' to view a list of commands.')
    # Begin the main loop
    while True:
        parser = argparse.ArgumentParser()
        parser.add_argument('action', nargs='+')
        user_input = input(PROMPT)
        inputs = []
        for i in user_input.split(' '):
            inputs.append(i)
        # File actions
        if inputs[0] == 'fl':
            try:
                PROJECT_FILE.load(inputs[1])
            except UnboundLocalError:
                print('Error: You need to specify a file path to load')
        elif inputs[0] == 'fs':
            PROJECT_FILE.save()
        elif inputs[0] == 'fS':
            try:
                PROJECT_FILE.saveas(inputs[1])
            except IndexError:
                print('Error: You need to specify a destination path!')
        # Metadata actions
        elif inputs[0] == 'ml':
            META_MANAGER.list_meta()
        elif inputs[0] == 'ma':
            META_MANAGER.add_meta(inputs[1],
                CliManager.resolve_input(inputs, 2)[-1])
        elif inputs[0] == 'mr':
            META_MANAGER.remove_meta(inputs[1])
        elif inputs[0] == 'mg':
            print(META_MANAGER.get(inputs[1]))
        # Fixture actions
        elif inputs[0] == 'xa':
            fixture = Fixture()
            try:
                fixture.new(inputs[1])
            except FileNotFoundError:
                print('Error: Couldn\'t find an OLF file with OLID '+inputs[1])
            else:
                fixture.add()
                fixture.save()
                INTERFACE_MANAGER.option_list['this'] = fixture.xml_fixture
        elif inputs[0] == 'xc':
            src_fixture = Fixture()
            src_fixture.load(INTERFACE_MANAGER.get(inputs[1]))
            new_fixture = Fixture()
            new_fixture.clone(src_fixture)
            new_fixture.add()
            new_fixture.save()
        elif inputs[0] == 'xl':
            list_fixtures()
        elif inputs[0] == 'xf':
            try:
                filter_fixtures(inputs[1], 
                    CliManager.resolve_input(inputs, 2)[-1])
            except IndexError:
                print('Error: You need to specify a key and value!')
        elif inputs[0] == 'xr':
            try:
                remove_fixture(INTERFACE_MANAGER.get(inputs[1]))
            except IndexError:
                print('Error: You need to run either xl or xf then specify the'
                      ' interface id of the fixture you wish to remove')
        elif inputs[0] == 'xi':
            fixture = INTERFACE_MANAGER.get(inputs[1])
            list_fixture_info(fixture)
            INTERFACE_MANAGER.option_list['this'] = fixture
        elif inputs[0] == 'xs':
            fixture = Fixture()
            fixture.load(INTERFACE_MANAGER.get(inputs[1]))
            fixture.edit(inputs[2], CliManager.resolve_input(inputs, 3)[-1])
            fixture.save()
        elif inputs[0] == 'xA':
            fixture = Fixture()
            fixture.load(INTERFACE_MANAGER.get(inputs[1]))
            registry = DmxRegistry(inputs[2])
            if inputs[3] == 'auto':
                address = registry.get_start_address(fixture.dmx_num)
            else:
                address = int(inputs[3])
            try:
                fixture.data['universe']
            except KeyError:
                continue
            else:
                old_start_addr = int(fixture.data['dmx_start_address'])
                i = old_start_addr
                while i < old_start_addr+int(fixture.data['dmx_channels']):
                    registry.registry[i] = None
                    i=i+1
            finally:
                fixture.edit('dmx_start_address', str(address))
                fixture.edit('universe', inputs[2])
                for function in fixture.dmx:
                    registry.registry[address] = (fixture.uuid, function)
                    address = int(address)+1
                fixture.save()
                registry.save()
                INTERFACE_MANAGER.option_list['this'] = fixture.xml_fixture
        elif inputs[0] == 'xp':
            purge_fixture(INTERFACE_MANAGER.get(inputs[1]))
        # DMX registry actions
        elif inputs[0] == 'rl':
            try:
                dmx_registry = DmxRegistry(inputs[1])
                dmx_registry.list()
            except IndexError:
                print('You need to specify a DMX registry!')
        # Utility actions
        elif inputs[0] == 'h':
            get_command_list()
        elif inputs[0] == 'c':
            clear()
        elif inputs[0] == 'q':
            print('Autosaving changes...')
            PROJECT_FILE.save()
            sys.exit()
        elif inputs[0] == 'q!':
            print('Ignoring changes and exiting...')
            sys.exit()
        else:
            print('Error: Command doesn\'t exist.') 
            print('Type \'h\' for a list of available commands.')


def main():
    init()
    if LAUNCH_ARGS.interface == 'cli':
        cli_loop()
    elif LAUNCH_ARGS.interface == 'gui':
        gui.main()

# Check that the program isn't imported, then run main
if __name__ == '__main__':
    main()
