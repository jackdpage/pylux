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

# Initiate the argument parser
Parser = argparse.ArgumentParser(prog='OLPlotter',
    description='Create and modify OpenLighting Plot files')
Parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
Parser.add_argument('file')
Parser.add_argument('fixturesDir')
Parser.add_argument('action', choices=['add'])
launch_args = Parser.parse_args()

PROJECT_FILE = launch_args.file
PROJECT_FILE_TREE = ET.parse(PROJECT_FILE)
PROJECT_FILE_ROOT = PROJECT_FILE_TREE.getroot()
OL_FIXTURES_DIR = launch_args.fixturesDir
PROGRAM_ACTION = launch_args.action

class DmxRegistry:
    
    # Create a new registry and populate it from the XML file
    def __init__(self, universe):
        self.registry = {}
        for i in range(1,513):
            self.registry[i] = ()
        DmxRegistry.populate(self, universe)

    # Get XML registry from universe_id returns False if no registry with that
    # universe id exists
    def get(universe_id):
        xml_registries = PROJECT_FILE_ROOT.findall('dmx_registry')
        got_match = False
        for xml_registry in xml_registries:
            universe = xml_registry.get('universe')
            if universe == universe_id:
                got_match = True
                return_registry = xml_registry
        if got_match == True:
            return return_registry
        else:
            return False

    # Search in universe_id for a channel with address
    def find(universe_id, address):
        xml_registry = DmxRegistry.get(universe_id)
        got_match = False
        for channel in xml_registry:
            found_address = channel.get('address')
            if found_address == str(address):
                got_match = True
                return_channel = channel
        if got_match == True:
            return return_channel
        else:
            return False

    # Populate registry with the contents of universe_id
    def populate(self, universe_id):
        using_registry = DmxRegistry.get(universe_id)
        for channel in using_registry:
            address = int(channel.get('address'))
            function = channel.find('function').text
            uuid = channel.find('fixture_uuid').text
            self.registry[address] = (uuid, function)
    
    # Save the contents of registry to universe_id
    def save(self, universe_id):

        # Edit an existing XML entry
        def edit_channel(address, info):
            channel = DmxRegistry.find(universe_id, address)
            channel.find('fixture_uuid').text = info[0]
            channel.find('function').text = info[1]            

        # Create an XML entry for a new DMX channel
        def create_channel(address, info):
            new_channel = ET.Element('channel')
            new_channel.set('address', str(address))
            new_uuid = ET.SubElement(new_channel, 'fixture_uuid')
            new_uuid.text = info[0]
            new_function = ET.SubElement(new_channel, 'function')
            new_function.text = info[1]
            return new_channel

        # If the universe doesn't exist in XML, create it
        if DmxRegistry.get(universe_id) == False:
            xml_registry = ET.Element('dmx_registry')
            xml_registry.set('universe', universe_id)
            PROJECT_FILE_ROOT.append(xml_registry)
        # Otherwise just fetch it
        else:
            xml_registry = DmxRegistry.get(universe_id)
    
        # Fill the XML registry with the Python registry contents
        for address in self.registry:
            info = self.registry[address]
            # If the Python channel is not blank, add it
            if info is not ():
                # If the doesn't already exist, make a new one
                if DmxRegistry.find(universe_id, address) == False:
                    new_channel = create_channel(address, info)
                    xml_registry.append(new_channel)
                # Otherwise just edit the existing one
                else:
                    edit_channel(address, info)

    # Get a list of all the used DMX channels
   
    # Get a list of the fixtures associated with each channel

    # Get a list of the functions of each DMX channel
    
    # Get a list of free DMX channels
    def get_free_channels(self):
        free_channels = []
        for address in self.registry:
            if self.registry[address] == ():
                free_channels.append(address)
        return free_channels
        

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

    def edit(self):
        for variable in self.variables:
            parser = argparse.ArgumentParser()
            parser.add_argument('variable')
            value = input('Value for '+variable+': ')
            args = parser.parse_args(value.split())
            self.variables[variable] = value

def get_olf_library():
    library = os.listdir(OL_FIXTURES_DIR)
    for olf in library:
        olid = olf.split('.')[0]
        library[library.index(olf)] = olid
    return library

def add_fixture():
    parser = argparse.ArgumentParser()
    parser.add_argument('fixture', choices=get_olf_library())
    print('The following fixture types were found: '+str(get_olf_library()))
    fixture_type = input('OLID of fixture to add: ')
    new_fixture = Fixture(fixture_type)
    new_fixture.edit()
    new_fixture.add()

PROJECT_FILE_TREE.write(PROJECT_FILE, encoding='UTF-8', xml_declaration=True)
