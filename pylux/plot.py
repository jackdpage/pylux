# plot.py is part of Pylux
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
import sys
from __init__ import __version__
import __main__


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

        Given an OLID, assign a UUID and load the constants from the 
        OLF file into the data dictionary.

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


class Metadata:
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

