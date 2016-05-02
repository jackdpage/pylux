# editor.py is part of Pylux
#
# Pylux is a program for the management of lighting documentation
# Copyright 2015 Jack Page
#
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

"""Edit the content of Pylux plot files.

editor is a CLI implementation of the Pylux plot editor, allowing 
for the reading and editing of Pylux plot files.
"""

import os
import pylux.clihelper as clihelper
from pylux.context.context import Context, Command
from pylux import get_data
import libxpx.xpx as xpx
import xml.etree.ElementTree as ET


class EditorContext(Context):

    def __init__(self):
        """Registers commands and globals for this context."""
        super().__init__()
        self.name = 'editor'

        self.register(Command('fo', self.file_open, [
            ('path', True, 'Path of the file to load.')])) 
        self.register(Command('fw', self.file_write, []))
        self.register(Command('fW', self.file_writeas, [
            ('path', True, 'Path to save the buffer to.')]))
        self.register(Command('fg', self.file_get, []))
        self.register(Command('fs', self.file_set, [
            ('path', True, 'Path to set as default save location.')]))

        self.register(Command('ml', self.metadata_list, []))
        self.register(Command('ms', self.metadata_set, [
            ('meta', True, 'The metadata to set the value of.'),
            ('value', True, 'Value for the metadata to take.')]))
        self.register(Command('mr', self.metadata_remove, [
            ('name', True, 'Name of the metadata to remove.')]))
        self.register(Command('mg', self.metadata_get, [
            ('name', True, 'Name of the metadata to print the value of.')]))

        self.register(Command('xn', self.fixture_new, [
            ('name', True, 'Human-readable name of the new fixture.')]))
        self.register(Command('xN', self.fixture_from_template, [
            ('template', True, 'Name of the fixture file to load data from.')]))
        self.register(Command('xc', self.fixture_clone, [
            ('fixture', True, 'The fixture to make a copy of.')]))
        self.register(Command('xl', self.fixture_list, []))
        self.register(Command('xf', self.fixture_filter, [
            ('tag', True, 'The tag to filter by.'),
            ('value', True, 'The value the tag must be to be displayed.')]))
        self.register(Command('xr', self.fixture_remove, [
            ('fixture', True, 'The fixture to remove.')]))
        self.register(Command('xg', self.fixture_get, [
            ('fixture', True, 'The fixture to get a tag from.'),
            ('tag', True, 'The name of the tag to print the vAlue of.')]))
        self.register(Command('xG', self.fixture_getall, [
            ('fixture', True, 'The fixture to print the tags of.')]))
        self.register(Command('xs', self.fixture_set, [
            ('fixture', True, 'The fixture to set a tag of.'), 
            ('tag', True, 'The name of the tag to set.'), 
            ('value', True, 'The value to set the tag to.')]))
        self.register(Command('xa', self.fixture_address, [
            ('fixture', True, 'The fixture to assign addresses to.'), 
            ('universe', True, 'The universe to assign addresses in.'), 
            ('address', True, 'The addresses to begin addressing at.')]))
        self.register(Command('xA', self.fixture_unaddress, [
            ('fixture', True, 'The fixture to unassign addresses for.')]))

        self.register(Command('rl', self.registry_list, []))
        self.register(Command('rL', self.registry_query, [
            ('registry', True, 'The registry to list used channels of.')]))
        self.register(Command('rn', self.registry_new, [
            ('name', True, 'The name of the new registry.')]))
        self.register(Command('rp', self.registry_probe, [
            ('registry', True, 'The registry to probe the used channels of.')]))
#        self.register(Command('rr', self.registry_remove [
#            ('registry', True, 'The registry to remove.')]))

        self.register(Command('ql', self.cue_list, [])) 
        self.register(Command('qn', self.cue_new, [
            ('type', True, 'The type of the cue to add.'), 
            ('location', True, 'The cue line or visual for this cue.')]))
        self.register(Command('qr', self.cue_remove, [
            ('cue', True, 'The cue to remove.')]))
        self.register(Command('qs', self.cue_set, [
            ('cue', True, 'The cue to set a tag of.'), 
            ('tag', True, 'The name of the tag to set.'), 
            ('value', True, 'The value to set the tag to.')]))
        self.register(Command('qg', self.cue_get, [
            ('cue', True, 'The cue to get a tag from.'), 
            ('tag', True, 'The name of the tag to print the value of.')]))
        self.register(Command('qG', self.cue_getall, [
            ('cue', True, 'The cue to print the tags of.')]))
        self.register(Command('qm', self.cue_moveafter, [
            ('cue', True, 'The cue to move.'), 
            ('dest_cue', True, 'The cue after which the cue should come.')]))
        self.register(Command('qM', self.cue_movebefore, [
            ('cue', True, 'The cue to move.'),
            ('dest_cue', True, 'The cue before which the cue should come.')]))

    # File commands

    def file_open(self, parsed_input):
        '''Open a new plot file, discarding any present buffer.'''
        self.plot_file.load(parsed_input[0])

    def file_write(self, parsed_input):
        '''Write the contents of the file buffer to the original path.'''
        self.plot_file.write(self.plot_file.load_location)

    def file_writeas(self, parsed_input):
        '''Write the contents of the file buffer to a new path.'''
        try:
            self.plot_file.write(parsed_input[0])
        except AttributeError:
            print('Error: No file is loaded')

    def file_get(self, parsed_input):
        '''Print the original location of the plot file.'''
        print(self.plot_file.load_location)

    def file_set(self, parsed_input):
        '''Set the default save location for the plot file.'''
        self.plot_file.load_location = parsed_input[0]

    # Metadata commands

    def metadata_list(self, parsed_input):
        '''List the values of all metadata in the plot file.'''
        self.interface.begin_listing()
        for meta in self.plot_file.metadata:
            s = meta.name+': '+meta.value
            self.interface.add_listing(meta, s)

    def metadata_set(self, parsed_input):
        metadata = self.interface.get(parsed_input[0])
        for meta in metadata:
            meta.value = parsed_input[1]

    def metadata_remove(self, parsed_input):
        '''Remove a piece of metadata from the file.'''
        metadata = self.interface.get(parsed_input[0])
        for meta in metadata:
            self.plot_file.metadata.remove(meta)

    def metadata_get(self, parsed_input):
        '''Print the values of metadata matching a name.'''
        self.interface.begin_listing()
        for meta in self.plot_file.metadata:
            if meta.name == parsed_input[0]:
                s = meta.name+': '+meta.value
                self.interface.add_listing(meta, s)

    # Fixture commands

    def fixture_new(self, parsed_input):
        '''Create a new fixture from scratch.'''
        fixture = xpx.Fixture(name=parsed_input[0], functions=[], data={})
        self.plot_file.fixtures.append(fixture)

    def fixture_from_template(self, parsed_input):
        '''Create a new fixture from a template file.'''
        template_file = get_data('fixture/'+parsed_input[0]+'.xml')
        if not template_file:
            self.log(30, 'No fixture template with this name exists')
        else:
            xfixture = ET.parse(template_file).getroot()
            fixture = xpx.Fixture(element=xfixture)
            self.plot_file.fixtures.append(fixture)

    def fixture_clone(self, parsed_input):
        '''Create a new fixture by copying an existing fixture.'''
        src_fixtures = self.interface.get(parsed_input[0])
        for src in src_fixtures:
            new_fixture = src
            new_fixture.uuid = str(xpx.uuid4())
            self.plot_file.fixtures.append(new_fixture)

    def fixture_list(self, parsed_input):
        '''List all fixtures in the plot file.'''
        self.interface.begin_listing()
        for fixture in self.plot_file.fixtures:
            if 'type' in fixture.data:
                fixture_type = fixture.data['type']
            else:
                fixture_type = 'n/a'
            s = fixture.name+' ('+fixture_type+')'
            self.interface.add_listing(fixture, s)

    def fixture_filter(self, parsed_input):
        '''List all fixtures that meet a certain criterion.'''
        key = parsed_input[0]
        value = parsed_input[1]
        fixtures = plot.FixtureList(self.plot_file)
        fixtures.assign_usitt_numbers()
        self.interface.clear()
        for fixture in fixtures.fixtures:
            i = int(fixture.data['usitt_key'])
            if key in fixture.data:
                if fixture.data[key] == value:
                    if 'name' in fixture.data:
                        name = fixture.data['name']
                    else:
                        name = fixture.data['type']
                    if self.config['cli']['show-uuids'] == 'True':
                        print('\033[4m'+str(i)+'\033[0m '+name+
                              ', id: '+fixture.uuid)
                    else:
                        print('\033[4m'+str(i)+'\033[0m '+name)
                    self.interface.append(i, fixture)
                    i = i+1
            else:
                pass

    def fixture_remove(self, parsed_input):
        '''Remove a fixture from the plot file.'''
        fixture_list = plot.FixtureList(self.plot_file)
        fixtures = self.interface.get(parsed_input[0])
        registries = plot.RegistryList(self.plot_file)
        for fixture in fixtures:
            fixture.unaddress(registries)
            fixture_list.remove(fixture)

    def fixture_get(self, parsed_input):
        '''Print the values of a fixture's tags.'''
        fixtures = self.interface.get(parsed_input[0])
        for fixture in fixtures:
            print('\033[1mFixture Data: '+fixture.name+'\033[0m')
            for key, value in fixture.data.items():
                print(key+': '+value)

    def fixture_getall(self, parsed_input):
        '''Print the tags and functions of a fixture..'''
        fixtures = self.interface.get(parsed_input[0])
        self.interface.begin_listing()
        for fixture in fixtures:
            print('\033[1mFixture Data: '+fixture.name+'\033[0m')
            for key, value in fixture.data.items():
                print(key+': '+value)
            for function in fixture.functions:
                s = '(Function) '+function.name
                self.interface.add_listing(function, s)

    def fixture_set(self, parsed_input):
        '''Set the value of one of a fixture's tags.'''
        fixtures = self.interface.get(parsed_input[0])
        tag = parsed_input[1]
        value = parsed_input[2]
        for fixture in fixtures:
            # See if it is a special pseudo tag
            if tag == 'position':
                fixture.data['posX'] = value.split(',')[0]
                fixture.data['posY'] = value.split(',')[1]
            elif tag == 'focus':
                fixture.data['focusX'] = value.split(',')[0]
                fixture.data['focusY'] = value.split(',')[1]
            elif tag == 'dimmer':
                dimmer_function = self.interface.get(value)[0].uuid
                fixture.data['controlDimmer'] = dimmer_function
            # Otherwise just set it
            else:
                fixture.data[tag] = value
        self.interface.update_this(parsed_input[0])

    def fixture_address(self, parsed_input):
        '''Assign DMX addresses to a fixture.'''
        fixtures = self.interface.get(parsed_input[0])
        registry = plot.DmxRegistry(self.plot_file, parsed_input[1])
        required_channels = len(fixtures[0].data['dmx_functions'].split(','))
        if parsed_input[2] == 'auto':
            start_address = registry.get_start_address(required_channels)
        else:
            start_address = int(parsed_input[2])
        fixtures[0].address(registry, start_address) 
        self.interface.update_this(parsed_input[0])

    def fixture_unaddress(self, parsed_input):
        '''Unassign addresses in all universes for this fixture.'''
        fixtures = self.interface.get(parsed_input[0])
        for fixture in fixtures:
            fixture.unaddress(plot.RegistryList(self.plot_file))

    # Registry commands

    def registry_new(self, parsed_input):
        '''Create a new registry.'''
        registry = xpx.Registry(name=parsed_input[0], channels=[])
        self.plot_file.registries.append(registry)

    def registry_remove(self, parsed_input):
        '''Delete one or more registries.'''
        registries = self.interface.get(parsed_input[0])
        for registry in registries:
            self.plot_file.registries.remove(registry)

    def registry_list(self, parsed_input):
        '''List all registries.'''
        self.interface.begin_listing()
        for registry in self.plot_file.registries:
            s = (registry.name+' ('+str(len(registry.get_occupied_addresses()))
                 +' occupied)')
            self.interface.add_listing(registry, s) 

    def registry_query(self, parsed_input):
        '''List the functions of all used channels in a registry.'''
        registries = self.interface.get(parsed_input[0])
        self.interface.begin_listing()
        for registry in registries:
            print('\033[1mUniverse: '+registry.name+'\033[0m')
            for channel in registry.channels:
                address = channel.address
                func = self.plot_file.get_object_by_uuid(channel.function.uuid)
                fix = self.plot_file.get_fixture_for_function(func)
                s = ('DMX'+str(format(address, '03d'))+': '+fix.name+' ('
                     +func.name+')')
                self.interface.add_listing(channel, s)

    def registry_probe(self, parsed_input):
        '''List channels and dimmer controlled lights.'''
        registries = self.interface.get(parsed_input[0])
        self.interface.begin_listing()
        for registry in registries:
            print('\033[1mUniverse: '+registry.name+'\033[0m')
            for channel in registry.channels:
                address = channel.address
                func = self.plot_file.get_object_by_uuid(channel.function.uuid)
                fixture = self.plot_file.get_fixture_for_function(func)
                s = ('DMX'+str(format(address, '03d'))+': '+fixture.name+' ('
                     +func.name+')')
                self.interface.add_listing(channel, s)
                controlled = self.plot_file.get_fixtures_for_dimmer_function(func)
                for dimmed_fixture in controlled:
                    print('\t→ '+dimmed_fixture.name)

    # Cue commands

    def cue_list(self, parsed_input):
        '''List all cues in the plot file.'''
        cues = plot.CueList(self.plot_file)
        self.interface.clear()
        for cue in sorted(cues.cues, key=lambda cue: cue.key):
            cue_type = cue.data['type']
            cue_location = cue.data['location']
            print(''.join(['\033[4m',str(cue.key),'\033[0m (',cue_type,
                          ') at \'',cue_location,'\'']))
            self.interface.append(cue.key, cue)

    def cue_new(self, parsed_input):
        '''Create a new cue.'''
        cue = plot.Cue(self.plot_file)
        cue.set_data('type', parsed_input[0])
        cue.set_data('location', parsed_input[1])

    def cue_remove(self, parsed_input):
        '''Remove a cue from the plot.'''
        cues = plot.CueList(self.plot_file)
        removal_candidates = self.interface.get(parsed_input[0])
        for rc in removal_candidates:
            cues.remove(rc)

    def cue_set(self, parsed_input):
        '''Set the value of a cue's tag.'''
        cues_to_change = self.interface.get(parsed_input[0])
        for cue in cues_to_change:
            cue.set_data(parsed_input[1], parsed_input[2])

    def cue_get(self, parsed_input):
        '''Print the value of a cue's tag.'''
        cues_to_get = self.interface.get(parsed_input[0])
        for cue in cues_to_get:
            if parsed_input[1] in cue.data:
                print(cue.data[parsed_input[1]])
            else:
                print(None)

    def cue_getall(self, parsed_input):
        '''Print the values of all of a cue's tags.'''
        cues_to_get = self.interface.get(parsed_input[0])
        for cue in cues_to_get:
            for data_item in cue.data:
                print(data_item+': '+cue.data[data_item])

    def cue_moveafter(self, parsed_input):
        '''Move a cue directly after another in the list.'''
        cues = plot.CueList(self.plot_file)
        cues.move_after(int(parsed_input[0]), 
                        int(parsed_input[1]))

    def cue_movebefore(self, parsed_input):
        '''Move a cue directly before another in the list.'''
        cues = plot.CueList(self.plot_file)
        cues.move_before(int(parsed_input[0]), 
                         int(parsed_input[1]))


def get_context():
    return EditorContext()
