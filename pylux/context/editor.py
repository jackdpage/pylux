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
        # Register commands
        self.register(Command('q', self.save_quit, []))
        self.register(Command('fo', self.file_open, ['path'], 
                              synopsis='Open a plot file.'))
        self.register(Command('fw', self.file_write, [], 
                              synopsis='Write the buffer to the original '
                                       'location.'))
        self.register(Command('fW', self.file_writeas, ['path'], 
                              synopsis='Write the buffer to a different '
                                       'location.'))
        self.register(Command('fg', self.file_get, [], 
                              synopsis='Print the location of the plot file.'))
        self.register(Command('fn', self.file_new, ['path'],
                              synopsis='Create a new plot file.'))
        self.register(Command('ml', self.metadata_list, [], 
                              synopsis='List all metadata values.'))
        self.register(Command('ms', self.metadata_set, ['name', 'value'], 
                              synopsis='Set the value of one piece of '
                                       'metadata.'))
        self.register(Command('mr', self.metadata_remove, ['name'], 
                              synopsis='Remove a piece of metadata'))
        self.register(Command('mg', self.metadata_get, ['name'],
                              synopsis='Print the value of a piece of '
                                       'metadata.'))
        self.register(Command('xn', self.fixture_new, ['template'], 
                              synopsis='Create a new fixture from a '
                                       'template.'))
        self.register(Command('xc', self.fixture_clone, ['fixture'], 
                              synopsis='Create a new fixture from an existing '
                                       'fixture.'))
        self.register(Command('xl', self.fixture_list, [], 
                              synopsis='List all fixtures.'))
        self.register(Command('xf', self.fixture_filter, ['tag', 'value'], 
                              synopsis='List all fixtures that match certain ' 
                                       'criteria.'))
        self.register(Command('xr', self.fixture_remove, ['fixture'], 
                              synopsis='Remove a fixture.'))
        self.register(Command('xg', self.fixture_get, ['fixture', 'tag'], 
                              synopsis='Print the value of a fixture\'s tag.'))
        self.register(Command('xG', self.fixture_getall, ['fixture'], 
                              synopsis='Print the values of all of a '
                                       'fixture\'s tags.'))
        self.register(Command('xs', self.fixture_set, 
                              ['fixture', 'tag', 'value'], 
                              synopsis='Set the value of a fixture\'s tag.'))
        self.register(Command('xa', self.fixture_address,
                              ['fixture', 'universe', 'address'], 
                              synopsis='Assign DMX addresses to a fixture.'))
        self.register(Command('xA', self.fixture_unaddress, ['fixture'], 
                              synopsis='Remove the DMX addresses assigned '
                                       'to a fixture.'))
        self.register(Command('rl', self.registry_list, ['universe'], 
                              synopsis='List the functions of the DMX '
                                       'channels in a universe.'))
        self.register(Command('rL', self.registry_probe, ['universe'], 
                              synopsis='List the functions of the DMX '
                                       'channels in a universe and, if there '
                                       'are any dimmers, list the fixtures '
                                       'that they control.'))
        self.register(Command('ql', self.cue_list, [], 
                              synopsis='List all the cues.'))
        self.register(Command('qn', self.cue_new, ['type', 'location'], 
                              synopsis='Add a new cue.'))
        self.register(Command('qr', self.cue_remove, ['cue'], 
                              synopsis='Remove a cue.'))
        self.register(Command('qs', self.cue_set, ['cue', 'tag', 'value'], 
                              synopsis='Set the value of a cue\'s tag.'))
        self.register(Command('qg', self.cue_get, ['cue', 'tag'], 
                              synopsis='Print the value of a cue\'s tag.'))
        self.register(Command('qG', self.cue_getall, ['cue'], 
                              synopsis='Print the values of all of a cue\'s '
                                       'tags.'))
        self.register(Command('qm', self.cue_moveafter, ['cue', 'dest_cue'], 
                              synopsis='Move a cue after another.'))
        self.register(Command('qM', self.cue_movebefore, ['cue', 'dest_cue'], 
                              synopsis='Move a cue before another.'))

    def save_quit(self, parsed_input):
        self.file_write(parsed_input)
        self.utility_kill(parsed_input)

    def file_open(self, parsed_input):
        try:
            self.plot_file.load(parsed_input[0])
        except FileNotFoundError:
            logging.warning('No file with that name')
        except FileFormatError:
            logging.warning('File is not valid XML')

    def file_write(self, parsed_input):
        try:
            self.plot_file.save()
        except AttributeError:
            print('Error: No file is loaded')

    def file_writeas(self, parsed_input):
        self.plot_file.saveas(parsed_input[0])

    def file_get(self, parsed_input):
        print('Using plot file '+self.plot_file.file)

    def file_new(self, parsed_input):
        self.plot_file.generate(os.path.expanduser(parsed_input[0]))
        self.plot_file.load(os.path.expanduser(parsed_input[0]))
        self.file_get(parsed_input)

    def metadata_list(self, parsed_input):
        metadata = plot.Metadata(self.plot_file)
        for i in metadata.meta:
            print(i+': '+metadata.meta[i])

    def metadata_set(self, parsed_input):
        metadata = plot.Metadata(self.plot_file)
        metadata.meta[parsed_input[0]] = parsed_input[1]
        metadata.save(self.plot_file)

    def metadata_remove(self, parsed_input):
        metadata = plot.Metadata(self.plot_file)
        metadata.meta[parsed_input[0]] = None
        metadata.save(self.plot_file)

    def metadata_get(self, parsed_input):
        metadata = plot.Metadata(self.plot_file)
        print(parsed_input[0]+': '+metadata.meta[parsed_input[0]])

    def fixture_new(self, parsed_input):
        fixture = plot.Fixture(self.plot_file)
        template_file = get_data('fixture/'+parsed_input[0]+'.xml')
        try:
            fixture.new(template_file)
        except FileNotFoundError:
            print('Error: Couldn\'t find a fixture file with this name')
        else:
            fixture.add(self.plot_file)
            fixture.save()

    def fixture_clone(self, parsed_input):
        src_fixture = self.interface.get(parsed_input[0])
        if len(src_fixture) > 1:
            print('Error: You can only clone one fixture!')
        else:
            new_fixture = plot.Fixture(self.plot_file, FIXTURES_DIR)
            new_fixture.clone(src_fixture[0])
            new_fixture.add()
            new_fixture.save()

    def fixture_list(self, parsed_input):
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
        fixture_list = plot.FixtureList(self.plot_file)
        fixtures = self.interface.get(parsed_input[0])
        for fixture in fixtures:
            fixture.unaddress(self.plot_file)
            fixture_list.remove(fixture)

    def fixture_get(self, parsed_input):
        fixtures = self.interface.get(parsed_input[0])
        for fixture in fixtures:
            if parsed_input[1] in fixture.data:
                print(fixture.data[parsed_input[1]])
            else:
                print(None)
        self.interface.update_this(parsed_input[0])

    def fixture_getall(self, parsed_input):
        fixtures = self.interface.get(parsed_input[0])
        for fixture in fixtures:
            for data_item in fixture.data:
                print(data_item+': '+str(fixture.data[data_item]))
        self.interface.update_this(parsed_input[0])

    def fixture_set(self, parsed_input):
        fixtures = self.interface.get(parsed_input[0])
        tag = parsed_input[1]
        value = parsed_input[2]
        for fixture in fixtures:
            # See if it can be automatically generated
            if value == 'auto':
                if tag == 'rotation':
                    fixture.data['rotation'] = str(fixture.generate_rotation())
                elif tag == 'colour':
                    fixture.data['colour'] = fixture.generate_colour()
                else:
                    print('Error: No automatic generation is available for '
                          'this tag')
            # See if it is a special pseudo tag
            elif tag == 'position':
                fixture.data['posX'] = value.split(',')[0]
                fixture.data['posY'] = value.split(',')[1]
            elif tag == 'focus':
                fixture.data['focusX'] = value.split(',')[0]
                fixture.data['focusY'] = value.split(',')[1]
            elif tag == 'dimmer':
                fixture.data['dimmer_uuid'] = self.interface.get(value.split(',')[0])[0].uuid
                fixture.data['dimmer_channel'] = value.split(',')[1]
            # Otherwise just set it
            else:
                fixture.data[tag] = value
            fixture.save()
        self.interface.update_this(parsed_input[0])

    def fixture_address(self, parsed_input):
        fixtures = self.interface.get(parsed_input[0])
        if len(fixtures) > 1 :
            print('Error: You cannot specify more than one fixture. \n'
                  'Using the first fixture in the list.')
        registry = plot.DmxRegistry(self.plot_file, parsed_input[1])
        required_channels = fixtures[0].data['dmx_channels']
        if parsed_input[2] == 'auto':
            start_address = registry.get_start_address(required_channels)
        else:
            start_address = int(parsed_input[2])
        fixtures[0].address(registry, start_address) 
        self.interface.update_this(parsed_input[0])

    def fixture_unaddress(self, parsed_input):
        fixtures = self.interface.get(parsed_input[0])
        for fixture in fixtures:
            fixture.unaddress(self.plot_file)

    def registry_list(self, parsed_input):
        registry = plot.DmxRegistry(self.plot_file, parsed_input[0])
        for channel in registry.registry:
            functions = registry.get_functions(channel)
            for function in functions:
                fixture = plot.Fixture(self.plot_file, uuid=function[0])
                print_name = clihelper.get_fixture_print(fixture)
                print(str(format(channel, '03d'))+' '+print_name+' ('+
                      function[1]+')')

    def registry_probe(self, parsed_input):
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
        cues = plot.CueList(self.plot_file)
        self.interface.clear()
        for cue in cues.cues:
            cue_type = cue.data['type']
            cue_location = cue.data['location']
            print('\033[4m'+str(cue.key)+'\033[0m ('+cue_type+') at '+
                  cue_location)
            self.interface.append(cue.key, cue)

    def cue_new(self, parsed_input):
        cue = plot.Cue(self.plot_file)
        cue.data['type'] = parsed_input[0]
        cue.data['location'] = parsed_input[1]
        cue.save(self.plot_file)

    def cue_remove(self, parsed_input):
        cues = plot.CueList(self.plot_file)
        removal_candidates = self.interface.get(parsed_input[0])
        for rc in removal_candidates:
            cues.remove(self.plot_file, rc.uuid)

    def cue_set(self, parsed_input):
        cues_to_change = self.interface.get(parsed_input[0])
        for cue in cues_to_change:
            cue.data[parsed_input[1]] = parsed_input[2]
            cue.save(self.plot_file)

    def cue_get(self, parsed_input):
        cues_to_get = self.interface.get(parsed_input[0])
        for cue in cues_to_get:
            if parsed_input[1] in cue.data:
                print(cue.data[parsed_input[1]])
            else:
                print(None)

    def cue_getall(self, parsed_input):
        cues_to_get = self.interface.get(parsed_input[0])
        for cue in cues_to_get:
            for data_item in cue.data:
                print(data_item+': '+cue.data[data_item])

    def cue_moveafter(self, parsed_input):
        cues = plot.CueList(self.plot_file)
        cues.move_after(self.plot_file, int(parsed_input[0]), 
                        int(parsed_input[1]))

    def cue_movebefore(self, parsed_input):
        cues = plot.CueList(self.plot_file)
        cues.move_before(self.plot_file, int(parsed_input[0]), 
                         int(parsed_input[1]))


def get_context():
    return EditorContext()
