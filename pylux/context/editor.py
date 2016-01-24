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
from pylux.context.context import Context
from pylux import get_data


class EditorContext(Context):

    def __init__(self):
        """Registers commands and globals for this context."""
        self.name = 'editor'
        self.init_commands()
        # Register commands
        self.register('fo', self.file_open, 1)
        self.register('fw', self.file_write, 0)
        self.register('fW', self.file_writeas, 1)
        self.register('fg', self.file_get, 0)
        self.register('fn', self.file_new, 1)
        self.register('ml', self.metadata_list, 0)
        self.register('ms', self.metadata_set, 2)
        self.register('mr', self.metadata_remove, 1)
        self.register('mg', self.metadata_get, 1)
        self.register('xn', self.fixture_new, 1)
        self.register('xc', self.fixture_clone, 1)
        self.register('xl', self.fixture_list, 0)
        self.register('xf', self.fixture_filter, 2)
        self.register('xr', self.fixture_remove, 1)
        self.register('xg', self.fixture_get, 2)
        self.register('xG', self.fixture_getall, 1)
        self.register('xs', self.fixture_set, 3)
        self.register('xa', self.fixture_address, 3)
        self.register('xp', self.fixture_purge, 1)
        self.register('rl', self.registry_list, 1)
        self.register('ql', self.cue_list, 0)
        self.register('qn', self.cue_new, 2)
        self.register('qr', self.cue_remove, 1)
        self.register('qs', self.cue_set, 3)
        self.register('qg', self.cue_get, 2)
        self.register('qG', self.cue_getall, 1)
        self.register('qm', self.cue_moveafter, 2)
        self.register('qM', self.cue_movebefore, 2)

    def file_open(self, parsed_input):
        try:
            self.plot_file.load(parsed_input[0])
        except IndexError:
            print('Error: You need to specify a file path to load')
        except AttributeError:
            pass

    def file_write(self, parsed_input):
        try:
            self.plot_file.save()
        except AttributeError:
            print('Error: No file is loaded')

    def file_writeas(self, parsed_input):
        try:
            self.plot_file.saveas(parsed_input[0])
        except IndexError:
            print('Error: You need to specify a destination path!')

    def file_get(self, parsed_input):
        print('Using plot file '+self.plot_file.file)

    def file_new(self, parsed_input):
        self.plot_file.generate(os.path.expanduser(parsed_input[0]))
        self.plot_file.load(os.path.expanduser(parsed_input[0]))
        file_get(self, parsed_input)

    def metadata_list(self, parsed_input):
        metadata = plot.Metadata(self.plot_file)
        for i in metadata.meta:
            print(i+': '+metadata.meta[i])

    def metadata_set(self, parsed_input):
        metadata = plot.Metadata(self.plot_file)
        metadata.meta[parsed_input[0]] = parsed_input[1]
        metadata.save()

    def metadata_remove(self, parsed_input):
        metadata = plot.Metadata(self.plot_file)
        metadata.meta[parsed_input[0]] = None
        metadata.save()

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
            print('\033[4m'+str(i)+'\033[0m '+name+', id: '+fixture.uuid)
            self.interface.append(i, fixture)
            i = i+1

    def fixture_filter(self, parsed_input):
        try:
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
                        print('\033[4m'+str(i)+'\033[0m '+name+
                              ', id: '+fixture.uuid+', '+key+': '+value)
                        self.interface.append(i, fixture)
                        i = i+1
                else:
                    pass
        except IndexError:
            print('Error: You need to specify a key and value!')

    def fixture_remove(self, parsed_input):
        fixture_list = plot.FixtureList(self.plot_file)
        fixtures = self.interface.get(parsed_input[0])
        for fixture in fixtures:
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
        if len(fixtures) > 1 and parsed_input[2] != 'auto':
            print('Error: You must specify auto if you address more than '
                  'one fixture.')
        else:
            registry = plot.DmxRegistry(self.plot_file, parsed_input[1])
            for fixture in fixtures:
                registry.address(fixture, parsed_input[2])
        self.interface.update_this(parsed_input[0])

    def fixture_purge(self, parsed_input):
        fixtures = self.interface.get(parsed_input[0])
        for fixture in fixtures:
            registry = plot.DmxRegistry(self.plot_file, fixture.data['universe'])
            registry.unaddress(fixture)
            fixture_list = plot.FixtureList(self.plot_file)
            fixture_list.remove(fixture)

    def registry_list(self, parsed_input):
        try:
            registry = plot.DmxRegistry(self.plot_file, parsed_input[0])
            for channel in registry.registry:
                uuid = registry.registry[channel][0]
                func = registry.registry[channel][1]
                print(str(format(channel, '03d'))+' uuid: '+uuid+', func: '+func)
        except IndexError:
            print('You need to specify a DMX registry!')

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
        cues.move_after(self.plot_file, int(parsed_input[0]), int(parsed_input[1]))

    def cue_movebefore(self, parsed_input):
        cues = plot.CueList(self.plot_file)
        cues.move_before(self.plot_file, int(parsed_input[0]), int(parsed_input[1]))


def get_context():
    return EditorContext()
