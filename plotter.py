# OLDoc is a suite for the management of lighting documentation
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
import logging
import os
import configparser
import os.path
import itertools
import operator
from itertools import groupby
from operator import itemgetter

# Initiate the argument parser
parser = argparse.ArgumentParser(prog='OLPlotter',
    description='Create and modify OpenLighting Plot files')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
parser.add_argument('file')
parser.add_argument('action', choices=['add'])
launch_args = parser.parse_args()

# Initiate the config parser
config_file = os.path.expanduser('~/.config/oldoc/OLDoc.conf')
config = configparser.ConfigParser()
config.read(config_file)
print('Using config file '+config_file)

PROJECT_FILE = launch_args.file
PROJECT_FILE_TREE = ET.parse(PROJECT_FILE)
PROJECT_FILE_ROOT = PROJECT_FILE_TREE.getroot()
OL_FIXTURES_DIR = os.path.expanduser(config['Fixtures']['dir'])
PROGRAM_ACTION = launch_args.action


class DmxRegistry:
    
    # Create a new registry and populate it from the XML file, if it doesn't
    # exist in the XML file, create an empty XML registry with id universe
    def __init__(self, universe):
        self.registry = {}
        self.universe = universe
        # Search for this universe in the XML file
        xml_registries = PROJECT_FILE_ROOT.findall('dmx_registry')
        for xml_registry in xml_registries: 
            testing_universe = xml_registry.get('universe')
            if testing_universe == self.universe:
                self.xml_registry = xml_registry
                break # Return XML registry if it exists
            else:
                xml_registry = False # Return false if no XML registry exists
        # Create a new XML registry if one doesn't exist
        if xml_registry == False:
            xml_registry = ET.Element('dmx_registry')
            xml_registry.set('universe', self.universe)
            PROJECT_FILE_ROOT.append(xml_registry)
            self.xml_registry = xml_registry
        # Populate the Python registry if an XML registry was found
        else:            
            for channel in xml_registry:
                address = int(channel.get('address'))
                uuid = channel.find('fixture_uuid').text
                function = channel.find('function').text
                self.registry[address] = (uuid, function)

    # Add a channel to the registry
    def add(self, address, uuid, function):
        self.registry[address] = (uuid, function)
        new_channel = ET.Element('channel')
        new_channel.set('address', str(address))
        new_uuid = ET.SubElement(new_channel, 'fixture_uuid')
        new_uuid.text = uuid
        new_function = ET.SubElement(new_channel, 'function')
        new_function.text = function
        self.xml_registry.append(new_channel)
    
    # Edit an existing DMX channel
    def edit(self, address, new_uuid, new_function):
        self.registry[address] = (new_uuid, new_function)
        channel = self.get_xml_channel(address)
        channel.find('fixture_uuid').text = new_uuid
        channel.find('function').text = function

    # Search a channel with address in XML
    def get_xml_channel(self, address):
        for channel in self.xml_registry:
            found_address = channel.get('address')
            if found_address == str(address):
                break
                return channel
        else:
            return False

    # Get a list of free DMX channels
    def get_free_channels(self):
        free = []
        for i in range(1, 512):
            free.append(i)
        for address in self.registry:
            free.remove(address) 
        groups = []
        keys = []
        free.sort()
       # for k, g in groupby(enumerate(data), lambda(i, x): i-x):
       #     print(map(itemgetter(1), g))
        

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

    # Create an XML object from the information in this fixture and add it to
    # the tree
    def add(self):
        fixture_list = PROJECT_FILE_ROOT.find('fixtures')
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

# Add a new fixture to the plot
def add_fixture():
    parser = argparse.ArgumentParser()
    parser.add_argument('fixture', choices=get_olf_library())
    print('The following fixture types were found: '+str(get_olf_library()))
    fixture_type = input('OLID of fixture to add: ')
    new_fixture = Fixture(fixture_type)
    new_fixture.edit()
    new_fixture.add()
    parser = argparse.ArgumentParser()
    parser.add_argument('universe')
    universe = input('DMX universe to use: ')
    parser.add_argument('start_address')
    address = input('DMX start address: ')
    registry = DmxRegistry(universe)
    print(universe)
    print(address)
    for function in new_fixture.dmx: 
        registry.add(address, new_fixture.uuid, function)
        address = int(address)+1

# Main function to allow imports
def main():
    iwb_reg = DmxRegistry('IWB')
    print(iwb_reg.registry)
    if PROGRAM_ACTION == 'add':
        add_fixture()
    print(iwb_reg.registry)
    print('doing main stuff')
    PROJECT_FILE_TREE.write(PROJECT_FILE, encoding='UTF-8', 
        xml_declaration=True)

# Check that the program isn't imported, then run main
if __name__ == '__main__':
    main()
