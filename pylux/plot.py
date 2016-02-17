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

"""Interact with Pylux plot files without an XML parser.

Manipulate Pylux plot files without having to use an XML parser, 
instead use the series of objects defined by plot which allow 
for quicker editing of plots, and management of the XML tree.
Also provides some utility functions to make writing extensions 
for Pylux quicker and easier.
"""

import xml.etree.ElementTree as ET
import uuid
import math
import pylux.reference as reference
from pylux.exception import *


class PlotFile:
    """Manage the Pylux plot project file.

    Attributes:
        path: the path of the project file.
        tree: the parsed XML tree.
        root: the root element of the XML tree.
    """

    def __init__(self, path=None):
        """Initialise the PlotFile instance.

        Prepares the instance of PlotFile for a file to be loaded 
        into it. If the path argument is given, loads the plot file 
        at that location on the filesystem and parses its XML tree 
        into an accessible element.

        Args:
            path: the full system path of the file to load.

        Raises:
            FileNotFoundError: if the file does not exist on the 
                               filesystem.
            FileFormatError: if the  XML parser raises a ParseError.
        """
        self.path = path
        if self.path is None:
            self.new()
        else:
            self.load(self.path)

    def load(self, path):
        """Load a project file.

        Args:
            path: the location of the file to load.

        Raeses:
            FileNotFoundError: if the file can not be found in the 
                               directory hierarchy.
            FileFormatError: if the XML parser raises a ParseError.
        """
        try:
            self.tree = ET.parse(path)
        except ET.ParseError:
            raise FileFormatError
        else:
            self.root = self.tree.getroot()
            self.path = path

    def write(self):
        """Save the project file to its original location."""
        self.tree.write(self.path, encoding='UTF-8', xml_declaration=True)

    def write_to(self, path):
        """Save the project file to a new location.

        Args:
            path: the location to save the file to.
        """
        self.path = path
        self.write()

    def new(self):
        """Create a new plot file in the buffer.

        Overwrite the current file buffer with a new empty plot file. 
        Create a new ElementTree in tree and set the root to be a 
        plot element.
        """
        self.root = ET.Element('plot')
        self.tree = ET.ElementTree(self.root)
        self.path = None

class DmxRegistry:
    """Manage DMX registries.
    
    Now with multiple functions per channel! Exclusive!!
    """

    def __init__(self, plot_file, universe):
        self.registry = {}
        self.universe = universe
        self._xml_registry = None
        # Find the corresponding XML registry
        for xml_registry in plot_file.root.findall('registry'):
            if xml_registry.get('universe') == self.universe:
                self._xml_registry = xml_registry
                break
        # If there isn't one make a new one
        if self._xml_registry is None:
            self._xml_registry = ET.Element('registry')
            self._xml_registry.set('universe', self.universe)
            plot_file.root.append(self._xml_registry)
        # Otherwise populate the Python registry
        else:
            for xml_channel in self._xml_registry.findall('channel'):
                address = int(xml_channel.get('address'))
                self.registry[address] = []
                for xml_function in xml_channel.findall('function'):
                    fixture_uuid = xml_function.get('uuid')
                    function = xml_function.text
                    self.registry[address].append((fixture_uuid, function))

    def _save(self):
        """Saves the Python registry to the XML tree.

        Saves the contents of the Python DMX registry to the registry in 
        XML and deletes any XML channels that no longer exist in the 
        Python registry.
        """
        # Search a channel with address in XML
        def get_xml_channel(self, address):
            for channel in self._xml_registry.findall('channel'):
                found_address = channel.get('address')
                if found_address == str(address):
                    return channel

        # Add an empty channel object
        def add_xml_channel(self, address):
            new_channel = ET.SubElement(self._xml_registry, 'channel')
            new_channel.set('address', str(address))

        # Iterate over the Python registry
        for address in self.registry:
            if self.registry[address] != None:
                xml_channel = get_xml_channel(self, address)
                # If there is no channel with this address, make one
                if xml_channel == None:
                    add_xml_channel(self, address)
                    xml_channel = get_xml_channel(self, address)
                # Clear the channel if it does exist
                else:
                    for function in xml_channel.findall('function'):
                        xml_channel.remove(function)
                # Iterate over functions and add to XML
                for function in self.registry[address]:
                    fixture_uuid = function[0]
                    fixture_function = function[1]
                    xml_function = ET.SubElement(xml_channel, 'function')
                    xml_function.set('uuid', fixture_uuid)
                    xml_function.text = fixture_function
            else:
                self._xml_registry.remove(get_xml_channel(self, address))

    def get_occupied(self):
        """Returns a list of occupied DMX channels.

        Returns:
            A list containing the addresses of the occupied channels 
            in the Python registry.
        """
        occupied = []
        for address in self.registry:
            if self.registry[address] != None:
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


    def add_function(self, address, fixture_uuid, function):
        if address in self.registry:
            self.registry[address].append((fixture_uuid, function))
        else:
            self.registry[address] = [(fixture_uuid, function)]
        self._save()

    def remove_function(self, address, uuid):
        """Remove a function from an address.

        Remove the function from the channel that has the given 
        fixture UUID.
        """
        for function in self.registry[address]:
            if function[0] == uuid:
                self.registry[address].remove(function)
        self._save()

    def get_functions(self, address):
        if address in self.registry:
            return self.registry[address]
        else:
            return None
        

class RegistryList:

    def __init__(self, plot_file):
        xml_registries = plot_file.root.findall('registry')
        self.registries = []
        for xml_registry in xml_registries:
            registry = DmxRegistry(plot_file, xml_registry.get('universe'))
            self.registries.append(registry)


class FixtureList:
    """Manage all the fixtures in a plot."""
    def __init__(self, plot_file):
        """Creates fixture objects for all the fixtures in the plot."""
        self._root = plot_file.root
        self.fixtures = []
        for xml_fixture in self._root.findall('fixture'):
            fixture = Fixture(plot_file, uuid=xml_fixture.get('uuid'))
            self.fixtures.append(fixture)

    def remove(self, fixture):
        """Remove a fixture from the plot."""
        self._root.remove(fixture._xml_fixture)

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

    def assign_usitt_numbers(self):
        count = 1
        hung = []
        for fixture in self.fixtures:
            if 'posY' in fixture.data:
                hung.append(fixture)
        for fixture in sorted(hung, key=lambda fixture: fixture.data['posY']):
            fixture.set_data('usitt_key', str(count))
            count = count+1
        for fixture in self.fixtures:
            if fixture not in hung:
                fixture.set_data('usitt_key', str(None))

    def get_fixtures_for_dimmer(self, dimmer):
        """Get a list of fixtures controlled by this fixture.

        If this is a dimmer fixture, get a list of fixture objects 
        that the dimmer controls.
        """
        if 'is_dimmer' not in dimmer.data:
            return []
        if dimmer.data['is_dimmer'] != 'True':
            return []
        controlled = []
        for fixture in self.fixtures:
            if 'dimmer_uuid' in fixture.data:
                if fixture.data['dimmer_uuid'] == dimmer.uuid:
                    controlled.append(fixture)
        return controlled


class Fixture:
    """Manage individual fixtures.

    Attributes:
        uuid: the UUID of the fixture.
        data: a dictionary containing all other data for the fixture.
        dmx: a list of the functions of the DMX channels used by this 
            fixture.
        dmx_num: the number of DMX channels required by this fixture.
    """

    def __init__(self, plot_file, uuid=None, template=None, src_fixture=None):
        """Create a new fixture in Python.

        If uuid is given, load data from the plot file from the fixture 
        with the corresponding UUID. If template is given, create a new 
        fixture based on the template file. If src_fixture is given, 
        copy the contents of an existing fixture into this one.

        Args:
            plot_file: the PlotFile object containing the plot.
            uuid: the UUID of the fixture to load from XML.
            src_fixture: the Fixture object to copy into this one.
        """
        self.data = {}
        if uuid != None:
            self.uuid = uuid
            xml_fixtures = plot_file.root.findall('fixture')
            for xml_fixture in plot_file.root.findall('fixture'):
                if uuid == xml_fixture.get('uuid'):
                    self._xml_fixture = xml_fixture
                    for data_item in self._xml_fixture:
                        self.data[data_item.tag] = data_item.text
                    self._save()
        elif template != None:
            self._new_from_template(template)
            self._xml_fixture = ET.Element('fixture')
            self._xml_fixture.set('uuid', self.uuid)
            plot_file.root.append(self._xml_fixture)
            self._save()
        elif src_fixture != None:
            self._new_from_fixture(src_fixture)
            self._xml_fixture = ET.Element('fixture')
            self._xml_fixture.set('uuid', self.uuid)
            plot_file.root.append(self._xml_fixture)
            self._save()

    def _new_from_template(self, template_file):
        """Load information from a template into this fixture.

        Args:
            template: the name of the template the new fixture should copy.
        """
        self.uuid = str(uuid.uuid4()) 
        src_tree = ET.parse(template_file)
        src_root = src_tree.getroot()
        for xml_data in src_root:
            self.data[xml_data.tag] = xml_data.text

    def _new_from_fixture(self, src_fixture):
        """Copy the contents of another fixture into this one.

        Make a verbatim copy of an existing fixture, except create 
        a new UUID for this fixture.

        Args:
            src_fixture: the source Fixture to be copied. 
        """
        self.uuid = str(uuid.uuid4())
        for data_item in src_fixture.data:
            self.data[data_item] = src_fixture.data[data_item]

    def _save(self):
        """Save the Python fixture object to XML."""
        # Add a new data item
        def add_xml_data(self, tag, value):
            new_data_item = ET.SubElement(self._xml_fixture, tag)    
            new_data_item.text = value

        # Edit an existing data item
        def edit_xml_data(self, tag, new_value):
            self._xml_fixture.find(tag).text = new_value

        # Search for data in XML
        def get_xml_data(self, tag):
            try:
                return self._xml_fixture.find(tag)
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
        for data_item in self._xml_fixture:
            data_name = data_item.tag
            if self.data[data_name] == '':
                self._xml_fixture.remove(data_item)

    def set_data(self, name, value):
        """Set the value of a piece of data."""
        self.data[name] = value
        self._save()

    def get_data(self, name):
        """Get the value of a piece of data."""
        if name in self.data:
            return self.data[name]
        else:
            return None

    def address(self, registry, start_address):
        address = start_address
        for function in self.data['dmx_functions'].split(','):
            registry.add_function(address, self.uuid, function)
            address = address+1

    def unaddress(self, registries):
        for registry in registries.registries:
            for address in registry.registry:
                registry.remove_function(address, self.uuid)

    def get_rotation(self):
        if ('posX' not in self.data or 'posY' not in self.data
            or 'focusX' not in self.data or 'focusY' not in self.data):
            return None
        else:
            posX = float(self.data['posX'])
            posY = float(self.data['posY'])
            focusX = float(self.data['focusX'])
            focusY = float(self.data['focusY'])
            return math.degrees(math.atan2((focusY-posY), (focusX-posX)))

    def get_colour(self):
        if 'gel' not in self.data:
            return None
        elif self.data['gel'] in reference.gel_colours:
            return reference.gel_colours[self.data['gel']]
        else:
            return None


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
        self._root = plot_file.root
        self.meta = {}
        for metaitem in self._root.findall('metadata'):
            self.meta[metaitem.get('name')] = metaitem.text

    def set_data(self, name, value):
        self.meta[name] = value
        self._save()

    def _save(self):
        """Save the metadata dictionary to XML."""
        # Add a new meta item
        def add_xml_meta(self, name, value):
            new_metadata = ET.Element('metadata')    
            new_metadata.set('name', name)
            new_metadata.text = value
            self._root.append(new_metadata)

        # Edit an existing meta item
        def edit_xml_meta(self, xml_meta, new_value):
            xml_meta.text = new_value

        # Search for meta in XML
        def get_xml_meta(self, name):
            try:
                for metaitem in self._root.findall('metadata'):
                    if metaitem.get('name') == metaitem:
                        return metaitem
                else:
                    return None
            except AttributeError:
                return None

        # Iterate over the meta values dictionary
        for metaitem in self.meta:
            xml_meta = get_xml_meta(self, metaitem)
            if xml_meta == None:
                add_xml_meta(self, metaitem, self.meta[metaitem])
            else:
                edit_xml_meta(self, xml_meta, self.meta[metaitem])
        # Iterate over XML meta object to remove empty values
        for metaitem in self._root.findall('metadata'):
            name = metaitem.get('name')
            if self.meta[name] == None:
                self._root.remove(metaitem)

class Cue:
    """Manages cues something something bored of docstrings."""

    def __init__(self, plot_file, UUID=None):
        """Create an empty cue."""
        self.data = {}
        if UUID is None:
            self.uuid = str(uuid.uuid4())
            self.key = len(CueList(plot_file).cues)+1
            self._xml_cue = ET.Element('cue')
            self._xml_cue.set('uuid', self.uuid)
            plot_file.root.append(self._xml_cue)
        else:
            self.uuid = UUID
            for xml_cue in plot_file.root.findall('cue'):
                if xml_cue.get('uuid') == self.uuid:
                    self._xml_cue = xml_cue
                    self.key = int(xml_cue.get('key'))
                    for cue_data in xml_cue:
                        self.data[cue_data.tag] = cue_data.text

    def set_data(self, name, value):
        """Set the value of name to value and save to XML."""
        self.data[name] = value
        self._save()

    def get_data(self, name):
        """Get the value of name."""
        if name in self.data:
            return self.data[name]
        else:
            return None

    def _save(self):
        """Save the cue to XML."""
        # Find data tags already in XML
        data_in_xml = []
        for data_item_xml in self._xml_cue:
            data_in_xml.append(data_item_xml.tag)
        # Set the sorting key
        self._xml_cue.set('key', str(self.key))
        # Iterate through data in dict
        for data_item in self.data:
            # If data not in XML, make a new sub element
            if data_item not in data_in_xml:
                new_data_item = ET.SubElement(self._xml_cue, data_item)
                new_data_item.text = self.data[data_item]
            # Otherwise edit existing data
            else:
                for data_item_xml in self._xml_cue:
                    if data_item_xml.tag == data_item:
                        data_item_xml.text = self.data[data_item]
        # Iterate through data in XML and remove empty
        for data_item_xml in self._xml_cue:
            if self.data[data_item_xml.tag] is None:
                self._xml_cue.remove(data_item_xml)


class CueList:
    """Manage all the cues in the document.

    Create a list contaning cue objects for every cue in the document. 
    Also manage the keys of cues by moving cues relative to one 
    another and remove cues entirely.

    Attributes:
        cues: a list of all the cue objects in the document.
    """

    def __init__(self, plot_file):
        """Generate a list of all the cues present.

        Search through the plot file for any cue tags, create a Cue
        object for them, then add to a list.

        Args:
            plot_file: the PlotFile object containing the document.
        """
        self._root = plot_file.root
        self.cues = []
        for xml_cue in self._root.findall('cue'):
            cue_uuid = xml_cue.get('uuid')
            cue = Cue(plot_file, UUID=cue_uuid)
            self.cues.append(cue)

    def remove(self, cue):
        """Remove a cue from the plot entirely.

        Args:
            plot_file: the PlotFile object containing the document.
            UUID: the UUID of the cue to be deleted.
        """
        self._root.remove(cue._xml_cue)

    def move_after(self, origin, dest):
        """Move a cue after another in the list.

        Manipulate the key attributes of any necessary cues to 
        rearrange the list such that origin is placed immediately 
        after dest.

        Args:
            plot_file: the PlotFile object containing the document.
            origin: the key of the cue to be moved.
            dest: the key of the cue after which this cue should be 
                  immediately located.
        """
        if dest > origin:
            for cue in self.cues:
                if cue.key == origin:
                    cue.key = dest
                elif origin < cue.key <= dest:
                    cue.key = cue.key-1
                cue._save()
        if dest < origin:
            for cue in self.cues:
                if dest < cue.key < origin:
                    cue.key = cue.key+1
                elif cue.key == origin:
                    cue.key = dest+1
                cue._save()

    def move_before(self, origin, dest):
        """Move a cue before another in the list.

        Manipulate the key attributes of any necessary cues to 
        rearrange the list such that origin is placed immediately
        before dest.

        Args:
            plot_file: the PlotFile object containing the document.
            origin: the key of the cue to be moved.
            dest: the key of the cue before which this cue should be 
                  immediately located.
        """
        if dest > origin:
            for cue in self.cues:
                if cue.key == origin:
                    cue.key = dest
                elif dest >= cue.key > origin:
                    cue.key = cue.key-1
                cue._save()
        if dest < origin:
            for cue in self.cues:
                if origin > cue.key >= dest:
                    cue.key = cue.key+1
                elif cue.key == origin:
                    cue.key = dest
                cue._save()

    def assign_identifiers(self):
        count = {'LX': 1, 'SX': 1, 'VX': 1}
        for cue in sorted(self.cues, key=lambda cue: cue.key):
            cue_type = cue.data['type']
            cue.set_data('identifier', cue_type+str(count[cue_type]))
            count[cue_type] = count[cue_type]+1


class Scene:
    """Scenes store DMX output states."""

    def __init__(self, plot_file, UUID=None):
        """Create an empty scene."""
        self.dmx_data = {}
        if UUID is None:
            self.uuid = str(uuid.uuid4())
            xml_cue = ET.Element('scene')
            xml_cue.set('uuid', self.uuid)
            plot_file.root.append(xml_cue)
        else:
            self.uuid = UUID
            for xml_scene in plot_file.root.findall('scene'):
                if xml_scene.get('uuid') == self.uuid:
                    for dmx_info_xml in xml_scene.findall('dmx'):
                        address = dmx_info_xml.get('address')
                        output = int(dmx_info_xml.text)
                        self.dmx_data[address] = output

    def save(self, plot_file):
        """Save the scene to XML."""
        for xml_scene_test in plot_file.root.findall('scene'):
            if xml_scene_test.get('uuid') == self.uuid:
                xml_scene = xml_scene_test
        # Find DMX info already in XML
        dmx_in_xml = []
        for dmx_info_xml in xml_scene.findall('dmx'):
            dmx_in_xml.append(dmx_info_xml.get('address'))
        # Iterate through data in DMX dict
        for dmx_info in self.dmx_data:
            # If DMX not in XML, make a new sub element
            if dmx_info not in dmx_in_xml:
                new_dmx_info = ET.SubElement(xml_scene, 'dmx')
                new_dmx_info.text = self.dmx_data[dmx_info]
                new_dmx_info.set('address', dmx_info)
            # Otherwise edit existing data
            else:
                for dmx_info_xml in xml_scene:
                    if dmx_info_xml.tag == dmx_info:
                        dmx_info_xml.text = self.dmx_data[dmx_info]
        # Iterate through data in XML and remove empty
        for dmx_info_xml in xml_scene:
            if self.dmx_data[dmx_info_xml.tag] is None:
                xml_scene.remove(dmx_info_xml)
