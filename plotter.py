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

# Initiate the argument parser
Parser = argparse.ArgumentParser(prog='OLPlotter',
    description='Create and modify OpenLighting Plot files')
Parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
Parser.add_argument('file')
launch_args = Parser.parse_args()

PROJECT_FILE = launch_args.file


# Parse the file to extract the root object
def get_file_root(file):
    file_tree = ET.parse(file)
    file_root = file_tree.getroot()
    return(file_root)

class DmxRegistry:
    # Create an empty DMX registry
    def create():
        dmx_registry = {}
        for i in range(1,513):
            dmx_registry[i] = ()
        return dmx_registry
    
    # Populate registry with the contents of universe_id
    def populate(registry, universe_id):
        xml_registries = file_root.findall('dmx_registry')
        for xml_registry in xml_registries:
            universe = xml_registry.get('universe')
            if universe == universe_id:
                using_registry = xml_registry
        for channel in using_registry:
            address = int(channel.get('address'))
            function = channel.find('function').text
            uuid = channel.find('fixture_uuid').text
            registry[address] = (uuid, function)

    # Get a list of all the used DMX channels
    def get_populated_list(registry):
        dmx_registry_populated = []
        for channel in registry:
            address = int(channel.get('address'))
            dmx_registry_populated.append(address)
            dmx_registry_populated.sort()
        return dmx_registry_populated
   
    # Get a list of the fixtures associated with each channel
    def get_uuid_registry(registry):
        dmx_registry_uuid = {}
        for channel in registry:
            address = int(channel.get('address'))
            dmx_registry_uuid[address] = channel.find('fixture_uuid').text
        return dmx_registry_uuid

    # Get a list of the functions of each DMX channel
    def get_function_registry(registry):
        dmx_registry_function = {}
        for channel in registry:
            address = int(channel.get('address'))
            dmx_registry_function[address] = channel.find('function').text
        return dmx_registry_function
    
    # Get a list of free DMX channels
    def get_free_channels(registry):
        occupied = DmxRegistry.get_populated_list(registry)
        free = DmxRegistry.get_all_dmx()
        for i in occupied:
            free.remove(i)
        return(free)
        
    # Get the next free run of n DMX channels
#    def get_n_free_channels(registry, n)
#        free = DmxRegistry.get_free_channels(registry)
