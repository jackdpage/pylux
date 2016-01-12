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
import math
import pylux.reference as reference


class PlotFile:
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

    def save(self):
        """Save the project file to its original location."""
        self.tree.write(self.file, encoding='UTF-8', xml_declaration=True)

    def saveas(self, path):
        """Save the project file to a new location.

        Args:
            path: the location to save the file to.
        """
        self.tree.write(path, encoding='UTF-8', xml_declaration=True)

    def generate(self, path):
        """Generate a blank project file.

        Generate a file containing the olplot root element, the 
        metadata element and the fixtures element.
        """
        with open(path, 'w') as new_file:
            new_file.write('<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
                           '<olplot>\n<metadata>\n</metadata>\n'
                           '<fixtures>\n</fixtures>\n</olplot>')


class DmxRegistry:
    """Manages DMX registries.

    Attributes:
        registry: the registry as a Python dictionary.
        universe: the universe id of the registry.
        xml_registry: the XML tree of the registry. Is False if the 
            registry doesn't exist in XML.
    """

    def __init__(self, plot_file, universe):
        """Create a new Python registry.

        Creates a new Python registry with the id universe. Then 
        searches the project file for a registry with the same id. If 
        one is found, loads that data into the Python registry, if 
        the registry doesn't exist in XML, creates one and adds it to 
        the tree.

        Args:
            universe: the universe id of the registry to be created.
        """
        self.plot_file = plot_file
        self.registry = {}
        self.universe = universe
        self.xml_registry = False
        # Search for this universe in the XML file
        xml_registries = self.plot_file.root.findall('dmx_registry')
        for xml_registry in xml_registries: 
            testing_universe = xml_registry.get('universe')
            if testing_universe == self.universe:
                self.xml_registry = xml_registry
                break # Return XML registry if it exists
        # Create a new XML registry if one doesn't exist
        if self.xml_registry == False:
            self.xml_registry = ET.Element('dmx_registry')
            self.xml_registry.set('universe', self.universe)
            self.plot_file.root.append(self.xml_registry)
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
                print('Found free channels in the range '+
                    str(free_from)+':'+str(free_until))
            if free_until-free_from+1 >= n:
                print('Automatically chose start address '+
                    str(free_from))
                return free_from

    def address(self, fixture, start_address):
        """Address a fixture."""
        required_channels = int(fixture.data['dmx_channels'])
        if start_address == 'auto':
            address = self.get_start_address(required_channels)
        else:
            address = int(start_address)
        try:
            fixture.data['universe']
        except KeyError:
            pass
        else:
            old_start_addr = int(fixture.data['dmx_start_address'])
            i = old_start_addr
            while i < old_start_addr+required_channels:
                self.registry[i] = None
                i = i+1
        fixture.data['dmx_start_address'] = str(address)
        fixture.data['universe'] = self.universe
        for function in fixture.dmx_functions:
            self.registry[address] = (fixture.uuid, function)
            address = int(address)+1
        fixture.save()
        self.save()

    def unaddress(self, fixture):
        """Remove a fixture from the registry"""
        start_address = int(fixture.data['dmx_start_address'])
        i = start_address
        while i < start_address+int(fixture.data['dmx_channels']):
            self.registry[i] = None
            i = i+1
        self.save()


class FixtureList:
    """Manage all the fixtures in a plot."""
    def __init__(self, plot_file):
        """Creates fixture objects for all the fixtures in the plot."""
        self.xml_fixture_list = plot_file.root.find('fixtures')
        self.fixtures = []
        for i in self.xml_fixture_list:
            fixture = Fixture(plot_file)
            fixture.load(i)
            self.fixtures.append(fixture)

    def remove(self, fixture):
        """Remove a fixture from the plot."""
        self.xml_fixture_list.remove(fixture.xml_fixture)

    def get_data_values(self, data_type):
        """Returns a list containing the values of data...etc""" 
        data_values = []
        for fixture in self.fixtures:
            try:
                data_values.append(fixture.data[data_type])
            except KeyError:
                pass
        data_values = list(set(data_values))
        data_values.sort()
        return data_values

class Fixture:
    """Manage individual fixtures.

    Attributes:
        uuid: the UUID of the fixture.
        data: a dictionary containing all other data for the fixture.
        dmx: a list of the functions of the DMX channels used by this 
            fixture.
        dmx_num: the number of DMX channels required by this fixture.
    """

    def __init__(self, plot_file, uuid=None):
        """Create a new fixture in Python and load data based on UUID."""
        self.plot_file = plot_file
        self.data = {}
        self.dmx_functions = []
        if uuid != None:
            xml_fixtures_list = plot_file.root.find('fixtures')
            for xml_fixture in xml_fixtures_list:
                if uuid == xml_fixture.get('uuid'):
                    self.load(xml_fixture)

    def new(self, template, fixtures_dir):
        """Make this fixture as a brand new fixture.

        Given template name, assign a UUID and load the constants from the 
        OLF file into the data dictionary.

        Args:
            template: the name of the template the new fixture should copy.
        """
        self.uuid = str(uuid.uuid4()) # Random UUID assigned
        src_tree = ET.parse(fixtures_dir+template+'.xml')
        self.src_root = src_tree.getroot()
        dmx_xml = self.src_root.find('dmx_functions')
        for channel in dmx_xml:
            self.dmx_functions.append(channel.tag)
        dmx_num = len(self.dmx_functions)
        # Add constants from OLF file
        for xml_data in self.src_root:
            if xml_data.tag != 'dmx_functions':
                self.data[xml_data.tag] = xml_data.text
        self.data['dmx_channels'] = str(dmx_num)

    def add(self):
        """Create an XML object for the fixture and add to the tree.

        Generate a fixture XML object and populate it with the 
        contents of the data dictionary, then add the newly created 
        fixture to the XML tree.
        """
        fixture_list = self.plot_file.root.find('fixtures')
        new_fixture = ET.Element('fixture')
        new_fixture.set('uuid', self.uuid)
        # Iterate over data 
        for data_item in self.data:
            new_detail = ET.SubElement(new_fixture, data_item)
            new_detail.text = self.data[data_item]
        xml_dmx_functions = ET.SubElement(new_fixture, 'dmx_functions')
        for dmx_function in self.dmx_functions:
            new_dmx_function = ET.SubElement(xml_dmx_functions, dmx_function)
        fixture_list.append(new_fixture)
        self.xml_fixture = new_fixture

    def load(self, xml_fixture):
        """Make this fixture as an existing fixture in the XML tree.

        Load the contents of an existing fixture in the XML document 
        into this Python fixture object.

        Args:
            fixture: the XML fixture object to load.
        """
        self.xml_fixture = xml_fixture
        self.uuid = xml_fixture.get('uuid')
        for data_item in xml_fixture:
            if data_item.tag != 'dmx_functions':
                self.data[data_item.tag] = data_item.text
        xml_dmx_functions = xml_fixture.find('dmx_functions')
        for dmx_function in xml_dmx_functions:
            self.dmx_functions.append(dmx_function.tag)
        self.dmx_num = len(self.dmx_functions)

    def clone(self, src_fixture):
        """Clone a fixture.

         an exact copy of a fixture in XML, but assign a new 
        UUID.

        Args:
            src_fixture: source Python fixture object to copy.
        """
        self.uuid = str(uuid.uuid4())
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
            if data_name != 'dmx_functions' and self.data[data_name] == "" :
                self.xml_fixture.remove(data_item)

    def generate_rotation(self):
        posX = float(self.data['posX'])
        posY = float(self.data['posY'])
        focusX = float(self.data['focusX'])
        focusY = float(self.data['focusY'])
        return math.degrees(math.atan2((focusY-posY), (focusX-posX)))

    def generate_colour(self):
        if self.data['gel'] in reference.gel_colours:
            return reference.gel_colours[self.data['gel']]
        else:
            return False


class Metadata:
    """Manages the metadata section of the XML file.

    Attributes:
        xml_meta: the XML object containing a the metadata.
        meta: a dictionary containing the metadata.
    """

    def __init__(self, plot_file):
        """Find the metadata in XML and add to the attribute.

        Args:
            plot_file: the FileManager object of the project file.
        """
        self.xml_meta = plot_file.root.find('metadata')
        self.meta = {}
        for metaitem in self.xml_meta:
            self.meta[metaitem.tag] = metaitem.text

    def save(self):
        """Save the metadata dictionary to XML."""
        # Add a new meta item
        def add_xml_meta(self, name, value):
            new_metadata = ET.Element(name)    
            new_metadata.text = value
            self.xml_meta.append(new_metadata)

        # Edit an existing meta item
        def edit_xml_meta(self, name, new_value):
            self.xml_meta.find(name).text = new_value

        # Search for meta in XML
        def get_xml_meta(self, name):
            try:
                return self.xml_meta.find(name)
            except AttributeError:
                return None

        # Iterate over the meta values dictionary
        for metaitem in self.meta:
            xml_meta = get_xml_meta(self, metaitem)
            if xml_meta == None:
                add_xml_meta(self, metaitem, self.meta[metaitem])
            else:
                edit_xml_meta(self, metaitem, self.meta[metaitem])
        # Iterate over XML meta object to remove empty values
        for metaitem in self.xml_meta:
            name = metaitem.tag
            if self.meta[name] == None:
                self.xml_meta.remove(metaitem)


class FixtureSymbol:
    """Manages the SVG symbols for fixtures."""

    def __init__(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        self.ns = {'ns0': 'http://www.w3.org/2000/svg'}
        self.image_group = root.find('ns0:g', self.ns)

    def prepare(self, posX, posY, rotation, colour):
        posX = str(float(posX)*1000)
        posY = str(float(posY)*1000)
        rotation = str(rotation)
        self.image_group.set('transform', 'translate('+
            posX+' '+posY+') rotate('+rotation+')')
        for path in self.image_group:
            if path.get('class') == 'outer':
                path.set('fill', colour)
