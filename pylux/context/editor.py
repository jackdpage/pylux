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
import pylux.plot as plot
import pylux.clihelper as clihelper
import logging
from pylux.context.context import Context, Command
from pylux import get_data
from pylux.exception import *


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
        self.register(Command('fn', self.file_new, []))
        self.register(Command('ml', self.metadata_list, []))
        self.register(Command('ms', self.metadata_set, [
            ('name', True, 'Name of the metadata to set.'),
            ('value', True, 'Value for the metadata to take.')]))
        self.register(Command('mr', self.metadata_remove, [
            ('name', True, 'Name of the metadata to remove.')]))
        self.register(Command('mg', self.metadata_get, [
            ('name', True, 'Name of the metadata to print the value of.')]))
        self.register(Command('xn', self.fixture_new, [
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
            ('tag', True, 'The name of the tag to print the value of.')]))
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
        self.register(Command('rl', self.registry_list, [
            ('universe', True, 'The universe to list the used addresses of.')]))
        self.register(Command('rL', self.registry_probe, [
            ('universe', True, 'The universe to list the used addresses of.')]))
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

    def file_open(self, parsed_input):
        '''Open a new plot file, discarding any present buffer.'''
        try:
            self.plot_file.load(parsed_input[0])
        except FileNotFoundError:
            logging.warning('No file with that name')
        except FileFormatError:
            logging.warning('File is not valid XML')

    def file_write(self, parsed_input):
        '''Write the contents of the file buffer to its original path.'''
        try:
            self.plot_file.write()
        except AttributeError:
            print('Error: No file is loaded')

    def file_writeas(self, parsed_input):
        '''Write the contents of the file buffer to an alternative location.'''
        self.plot_file.write_to(parsed_input[0])

    def file_get(self, parsed_input):
        '''Print the path from which the current file was loaded.'''
        if self.plot_file.path is None:
            print('Using temporary plot file')
        else:
            print('Using plot file '+self.plot_file.path)

    def file_new(self, parsed_input):
        '''Create a new file in the buffer.'''
        self.plot_file.new()

    def metadata_list(self, parsed_input):
        '''List the values of all metadata in the plot file.'''
        metadata = plot.Metadata(self.plot_file)
        for meta_item in sorted(metadata.meta):
            print(meta_item+': '+metadata.meta[meta_item])

    def metadata_set(self, parsed_input):
        '''Set the value of a piece of metadata.'''
        metadata = plot.Metadata(self.plot_file)
        metadata.set_data(parsed_input[0], parsed_input[1])

    def metadata_remove(self, parsed_input):
        '''Remove a piece of metadata from the file.'''
        metadata = plot.Metadata(self.plot_file)
        metadata.set_data(parsed_input[0], None)

    def metadata_get(self, parsed_input):
        '''Print the value of a piece of metadata.'''
        metadata = plot.Metadata(self.plot_file)
        print(parsed_input[0]+': '+metadata.get_data(parsed_input[0]))

    def fixture_new(self, parsed_input):
        '''Create a new fixture from a template file.'''
        template_file = get_data('fixture/'+parsed_input[0]+'.xml')
        try:
            fixture = plot.Fixture(self.plot_file, template=template_file)
        except FileNotFoundError:
            print('Error: No template with this name')

    def fixture_clone(self, parsed_input):
        '''Create a new fixture by copying an existing fixture.'''
        src_fixtures = self.interface.get(parsed_input[0])
        for src in src_fixtures:
            new_fixture = plot.Fixture(self.plot_file, src_fixture=src)

    def fixture_list(self, parsed_input):
        '''List all fixtures in the plot file.'''
        fixtures = plot.FixtureList(self.plot_file)
        i = 1
        self.interface.clear()
        for fixture in fixtures.fixtures:
            if 'name' in fixture.data:
                name = fixture.data['name']
            else:
                name = fixture.data['type']
            if self.config['cli']['show-uuids'] == 'True':
                print('\033[4m'+str(i)+'\033[0m '+name+', id: '+fixture.uuid)
            else:
                print('\033[4m'+str(i)+'\033[0m '+name)
            self.interface.append(i, fixture)
            i = i+1

    def fixture_filter(self, parsed_input):
        '''List all fixtures that meet a certain criterion.'''
        key = parsed_input[0]
        value = parsed_input[1]
        fixtures = plot.FixtureList(self.plot_file)
        self.interface.clear()
        i = 1
        for fixture in fixtures.fixtures:
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
        '''Print the value of a fixture's tag.'''
        fixtures = self.interface.get(parsed_input[0])
        for fixture in fixtures:
            print(fixture.get_data(parsed_input[1]))
        self.interface.update_this(parsed_input[0])

    def fixture_getall(self, parsed_input):
        '''Print the value of every tag associated with a fixture.'''
        fixtures = self.interface.get(parsed_input[0])
        for fixture in fixtures:
            for data_item in fixture.data:
                print(data_item+': '+str(fixture.data[data_item]))
        self.interface.update_this(parsed_input[0])

    def fixture_set(self, parsed_input):
        '''Set the value of one of a fixture's tags.'''
        fixtures = self.interface.get(parsed_input[0])
        tag = parsed_input[1]
        value = parsed_input[2]
        for fixture in fixtures:
            # See if it is a special pseudo tag
            if tag == 'position':
                fixture.set_data('posX', value.split(',')[0])
                fixture.set_data('posY', value.split(',')[1])
            elif tag == 'focus':
                fixture.set_data('focusX', value.split(',')[0])
                fixture.set_data('focusY', value.split(',')[1])
            elif tag == 'dimmer':
                fixture.set_data('dimmer_uuid', self.interface.get(value.split(',')[0])[0].uuid)
                fixture.set_data('dimmer_channel', value.split(',')[1])
            # Otherwise just set it
            else:
                fixture.set_data(tag, value)
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

    def registry_list(self, parsed_input):
        '''List the functions of all used channels in a registry.'''
        registry = plot.DmxRegistry(self.plot_file, parsed_input[0])
        for channel in registry.registry:
            functions = registry.get_functions(channel)
            for function in functions:
                fixture = plot.Fixture(self.plot_file, uuid=function[0])
                print_name = clihelper.get_fixture_print(fixture)
                print(str(format(channel, '03d'))+' '+print_name+' ('+
                      function[1]+')')

    def registry_probe(self, parsed_input):
        '''List the functions of all used channels in a registry and also \n
        list any fixtures which are controlled by dimmers.'''
        registry = plot.DmxRegistry(self.plot_file, parsed_input[0])
        for channel in registry.registry:
            functions = registry.get_functions(channel)
            for function in functions:
                fixture = plot.Fixture(self.plot_file, uuid=function[0])
                print_name = clihelper.get_fixture_print(fixture)
                print(str(format(channel, '03d'))+' '+print_name+' ('+
                      function[1]+')')
                if ('is_dimmer' in fixture.data and 
                    fixture.data['is_dimmer'] == 'True'):
                    dimmer_chan = function[1].replace('channel_', '')
                    fixtures = plot.FixtureList(self.plot_file)
                    for lantern in fixtures.fixtures:
                        if ('dimmer_uuid' in lantern.data and 
                            lantern.data['dimmer_uuid'] == function[0] and 
                            lantern.data['dimmer_channel'] == dimmer_chan):
                            print_name = clihelper.get_fixture_print(lantern)
                            print('    ⤷ '+print_name)

    def cue_list(self, parsed_input):
        '''List all cues in the plot file.'''
        cues = plot.CueList(self.plot_file)
        self.interface.clear()
        for cue in cues.cues:
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
