# pylux is a program for the management of lighting documentation
# Copyright 2015 Jack Page
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
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

# Initiate the argument parser
parser = argparse.ArgumentParser(prog='pylux',
    description='Create and modify OpenLighting Plot files')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
parser.add_argument('-f', '--file', dest='file', 
    help='load this project file on launch')
LAUNCH_ARGS = parser.parse_args()

# Initiate the config parser
config_file = os.path.expanduser('~/.config/pylux.conf')
config = configparser.ConfigParser()
config.read(config_file)

OL_FIXTURES_DIR = os.path.expanduser(config['Fixtures']['dir'])

PROMPT = '(pylux) '

class FileManager:

    def load(self, path):
        self.file = path
        try:
            self.tree = ET.parse(self.file)
        except FileNotFoundError:
            print('The file you are trying to load doesn\'t exist!')
        self.root = self.tree.getroot()

    def save(self):
        self.tree.write(self.file, encoding='UTF-8', 
            xml_declaration=True)


class ConfigHelper:
    
    def __init__(self):
        self = self

    
class DmxRegistry:
    
    # Create a new registry and populate it from the XML file, if it doesn't
    # exist in the XML file, create an empty XML registry with id universe
    def __init__(self, universe):
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
            uuid = self.registry[address][0]
            function = self.registry[address][1]
            xml_channel = get_xml_channel(self, address)
            if xml_channel == None:
                add_xml_entry(self, address, uuid, function)
            else:
                edit_xml_entry(self, xml_channel, uuid, function)
        # Iterate over the XML registry to remove any now empty channels
        for channel in self.xml_registry:
            address = int(channel.get('address'))
            if address not in self.registry:
                self.xml_registry.remove(channel)

    # Get a list of the occupied channels
    def get_occupied(self):
        occupied = []
        for address in self.registry:
            occupied.append(address)
        occupied.sort()
        return occupied

    # Get a start address for a run of n free DMX channels
    def get_start_address(self, n):
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

    # Print a nice list of the used channels
    def print(self):
        for channel in self.registry:
            print(str(format(channel, '03d'))+' uuid: '+
                self.registry[channel][0]+', func: '+self.registry[channel][1])

class Fixture:
    
    # Initialise the fixture from the OLF file
    def __init__(self, olid):
        tree = ET.parse(OL_FIXTURES_DIR+olid+'.olf')
        root = tree.getroot()
        self.olid = olid # OLID was specified on creation
        self.uuid = str(uuid.uuid4()) # Random UUID assigned
        # Add variables from OLF file
        variables_xml = root.find('variables')
        self.variables = {}
        for variable in variables_xml:
            self.variables[variable.tag] = None
        # Add constants from OLF file
        constants_xml = root.find('constants')
        self.constants = {}
        for constant in constants_xml:
            self.constants[constant.tag] = constant.text
        # Add DMX channels from OLF file
        dmx_xml = root.find('dmx_channels')
        self.dmx = []
        for channel in dmx_xml:
            self.dmx.append(channel.tag)
        self.dmx_num = len(self.dmx)

    # Create an XML object from the information in this fixture and add it to
    # the tree
    def add(self):
        fixture_list = PROJECT_FILE.root.find('fixtures')
        new_fixture = ET.Element('fixture')
        new_fixture.set('olid', self.olid)
        new_fixture.set('uuid', self.uuid)
        # Iterate over variables
        for variable in self.variables:
            new_detail = ET.SubElement(new_fixture, variable)
            new_detail.text = self.variables[variable]
        # Iterate over constants
        for constant in self.constants:
            new_detail = ET.SubElement(new_fixture, constant)
            new_detail.text = self.constants[constant]
        fixture_list.append(new_fixture)

    # Edit the data associated with this fixture
    def edit(self):
        for variable in self.variables:
            parser = argparse.ArgumentParser()
            parser.add_argument('variable')
            value = input('Value for '+variable+': ')
            args = parser.parse_args(value.split())
            self.variables[variable] = value
    

# Return a list of the OLF files in the directory
def get_olf_library():
    library = os.listdir(OL_FIXTURES_DIR)
    for olf in library:
        olid = olf.split('.')[0]
        library[library.index(olf)] = olid
    return library

# Display the help page
def get_command_list():
    text = ""
    with open('help.txt') as man:
        for line in man:
            text = text+line
    print(text)

# Clear the console
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Add a new fixture to the plot
def add_fixture():
    parser = argparse.ArgumentParser()
    parser.add_argument('fixture')
    print('The following fixture types were found: '+str(get_olf_library()))
    fixture_type = input('OLID of fixture to add: ')
    new_fixture = Fixture(fixture_type)
    new_fixture.edit()
    new_fixture.add()
    parser = argparse.ArgumentParser()
    parser.add_argument('universe')
    universe = input('DMX universe to use: ')
    registry = DmxRegistry(universe)
    print('Need '+str(new_fixture.dmx_num)+' DMX channels')
    print('Occupied channels: '+str(registry.get_occupied()))
    parser.add_argument('address')
    address = input('DMX start address or auto: ')
    if address == 'auto':
        address = registry.get_start_address(new_fixture.dmx_num)
    else:
        address = int(address)
    for function in new_fixture.dmx: 
        registry.registry[address] = (new_fixture.uuid, function)
        address = int(address)+1
    registry.save()

# Get a list of all the fixtures
def list_fixtures():
    fixture_list = PROJECT_FILE.root.find('fixtures')
    for fixture in fixture_list:
        olid = fixture.get('olid')
        uuid = fixture.get('uuid')
        print(olid+', id: '+uuid)

# The program itself
def main():
    global PROJECT_FILE
    PROJECT_FILE = FileManager()
    print('Pylux 0.1')
    print('Using configuration file '+config_file)
    # If a project file was given at launch, load it
    if LAUNCH_ARGS.file != None:
        PROJECT_FILE.load(os.path.expanduser(LAUNCH_ARGS.file))
        print('Using project file '+PROJECT_FILE.file) 
    print('Welcome to Pylux! Type \'help\' to view a list of commands.')
    while True:
        parser = argparse.ArgumentParser()
        parser.add_argument('action')
        user_input = input(PROMPT)
        if user_input.find(' ') != -1:
            action = user_input.split(' ')[0]
            parameter = user_input.split(' ')[1]
        else:
            action = user_input
        # File actions
        if action == 'load' or action == 'fl':
            try:
                PROJECT_FILE.load(parameter)
            except UnboundLocalError:
                print('You need to specify a file path to load')
        elif action == 'save' or action == 'fs':
            PROJECT_FILE.save()
        # Fixture actions
        elif action == 'add' or action == 'xa':
            add_fixture()
        elif action == 'fixlist' or action == 'xl':
            list_fixtures()
        # DMX registry actions
        elif action == 'reglist' or action == 'rl':
            dmx_registry = DmxRegistry(parameter)
            dmx_registry.print()
        # Utility actions
        elif action == 'help' or action == 'h':
            get_command_list()
        elif action == 'clear' or action == 'c':
            clear()
        elif action == 'quit' or action == 'q':
            sys.exit()
        else:
            print('The command you typed doesn\'t exist.') 
            print('Type \'help\' for a list of available commands.')

# Check that the program isn't imported, then run main
if __name__ == '__main__':
    main()
