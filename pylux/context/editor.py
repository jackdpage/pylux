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

import clihelper
import uuid
from clihelper import ReferenceBuffer
from context.context import Context, Command
from lib import pseudotag, data, printer
import xml.etree.ElementTree as ET
import re

# temporary solution before api is properly written
import document


class EditorContext(Context):

    def __init__(self):
        """Registers commands."""
        super().__init__()
        self.name = 'editor'

        # Command Registration

        self.register(Command('fo', self.file_open, [
            ('path', True, 'Path of the file to load.')])) 
        self.register(Command('fw', self.file_write, []))
        self.register(Command('fW', self.file_writeas, [
            ('path', True, 'Path to save the buffer to.')]))
        self.register(Command('fg', self.file_get, []))
        self.register(Command('fs', self.file_set, [
            ('path', True, 'Path to set as default save location.')]))

        self.register(Command('ml', self.metadata_list, []))
        self.register(Command('mn', self.metadata_new, [
            ('name', True, 'The name of the metadata to add.')]))
        self.register(Command('ms', self.metadata_set, [
            ('MET', True, 'The metadata to set the value of.'),
            ('value', True, 'Value for the metadata to take.')]))
        self.register(Command('mr', self.metadata_remove, [
            ('MET', True, 'The metadata to remove.')]))
        self.register(Command('mg', self.metadata_get, [
            ('name', True, 'Name of the metadata to print the value of.')]))

        self.register(Command('xn', self.fixture_new, [
            ('name', True, 'Human-readable name of the new fixture.')]))
        self.register(Command('xN', self.fixture_from_template, [
            ('template', True, 'Path to the file to load data from.')]))
        self.register(Command('xc', self.fixture_clone, [
            ('FIX', True, 'The fixture to make a copy of.')]))
        self.register(Command('xl', self.fixture_list, []))
        self.register(Command('xf', self.fixture_filter, [
            ('tag', True, 'The tag to filter by.'),
            ('value', True, 'The value the tag must be to be displayed.')]))
        self.register(Command('xr', self.fixture_remove, [
            ('FIX', True, 'The fixture to remove.')]))
        self.register(Command('xg', self.fixture_get, [
            ('FIX', True, 'The fixture to get a tag from.'),
            ('tag', True, 'The name of the tag to print the vAlue of.')]))
        self.register(Command('xG', self.fixture_getall, [
            ('FIX', True, 'The fixture to print the tags of.')]))
        self.register(Command('xs', self.fixture_set, [
            ('FIX', True, 'The fixture to set a tag of.'), 
            ('tag', True, 'The name of the tag to set.'), 
            ('value', True, 'The value to set the tag to.')]))
        self.register(Command('xa', self.fixture_address, [
            ('FIX', True, 'The fixture to assign addresses to.'), 
            ('REG', True, 'The name of the universe to address in.'), 
            ('address', True, 'The addresses to begin addressing at.')]))
        self.register(Command('xA', self.fixture_unaddress, [
            ('FIX', True, 'The fixture to unassign addresses for.')]))

        self.register(Command('rl', self.registry_list, []))
        self.register(Command('rL', self.registry_query, [
            ('REG', True, 'The registry to list used channels of.')]))
        self.register(Command('rn', self.registry_new, [
            ('name', True, 'The name of the new registry.')]))
        self.register(Command('rp', self.registry_probe, [
            ('REG', True, 'The registry to probe the channels of.')]))
#        self.register(Command('rr', self.registry_remove [
#            ('registry', True, 'The registry to remove.')]))
        self.register(Command('ra', self.registry_add, [
            ('FNC', True, 'The function(s) to address.'),
            ('REG', True, 'The name of the registry to address in.'),
            ('address', True, 'The address to begin addressing at.')]))

        self.register(Command('sl', self.scene_list, []))
        self.register(Command('sn', self.scene_new, [
            ('outputs', True, 'In the form FNC@###;FNC@###.'),
            ('name', True, 'The name of the scene.')]))
        self.register(Command('sg', self.scene_getall, [
            ('SCN', True, 'The scene to display the outputs of.')]))
        self.register(Command('sG', self.scene_getall_dmx, [
            ('SCN', True, 'The scene to display the outputs of.')]))

    def post_init(self):
        '''Registers interface buffers.'''

        self.interface.buffers['FIX'] = ReferenceBuffer(colour=92)
        self.interface.buffers['FNC'] = ReferenceBuffer(colour=95)
        self.interface.buffers['REG'] = ReferenceBuffer(colour=93)
        self.interface.buffers['MET'] = ReferenceBuffer(colour=94)
        self.interface.buffers['SCN'] = ReferenceBuffer(colour=96)
        self.interface.buffers['CHS'] = ReferenceBuffer(colour=96)

    # File commands

    def file_open(self, parsed_input):
        '''Open a new plot file, discarding any present buffer.'''
        self.load_location = parsed_input[0]
        s = document.get_string_from_file(parsed_input[0])
        self.plot_file = document.get_deserialised_document_from_string(s)

    def file_write(self, parsed_input):
        '''Write the contents of the file buffer to the original path.'''
        document.write_to_file(self.plot_file, self.load_location)

    def file_writeas(self, parsed_input):
        '''Write the contents of the file buffer to a new path.'''
        document.write_to_file(self.plot_file, parsed_input[0])

    def file_get(self, parsed_input):
        '''Print the original location of the plot file.'''
        print(self.load_location)

    def file_set(self, parsed_input):
        '''Set the default save location for the plot file.'''
        self.load_location = parsed_input[0]

    # Metadata commands

    def metadata_list(self, parsed_input):
        '''List the values of all metadata in the plot file.'''
        self.interface.open('MET')
        for meta in document.get_metadata(self.plot_file):
            s = meta['metadata-key']+': '+printer.get_metadata_value(meta)
            self.interface.add(s, meta['uuid'], 'MET')

    def metadata_set(self, parsed_input):
        meta_ids = self.interface.get('MET', parsed_input[0])
        for meta_id in meta_ids:
            document.get_by_uuid(self.plot_file, meta_id)['metadata-value'] = parsed_input[1]

    def metadata_remove(self, parsed_input):
        '''Remove a piece of metadata from the file.'''
        meta_ids = self.interface.get('MET', parsed_input[0])
        for meta_id in metas_ids:
            document.remove_by_uuid(self.plot_file, meta_id)

    def metadata_get(self, parsed_input):
        '''Print the values of metadata matching a name.'''
        self.interface.open('MET')
        for meta in document.get_metadata(self.plot_file):
            if meta['metadata-key'] == parsed_input[0]:
                s = meta['metadata-key']+': '+printer.get_metadata_value(meta)
                self.interface.add(s, meta['uuid'], 'MET')

    def metadata_new(self, parsed_input):
        '''Create a new metadata item.'''
        self.plot_file.append({'type': 'metadata',
                               'uuid': str(uuid.uuid4()),
                               'metadata-key': parsed_input[0]})

    # Fixture commands

    def fixture_new(self, parsed_input):
        '''Create a new fixture from scratch.'''
        self.plot_file.append({'type': 'fixture',
                               'uuid': str(uuid.uuid4())})

    def fixture_from_template(self, parsed_input):
        '''Create a new fixture from a template file.'''
        template_file = data.get_data('fixture/'+parsed_input[0]+'.json')
        if not template_file:
            self.log(30, 'No fixture template with this name exists')
        else:
            fixture = json.load(template_file)
            fixture['uuid'] = str(uuidv4())
            self.plot_file.append(fixture)

    def fixture_clone(self, parsed_input):
        '''Create a new fixture by copying an existing fixture.'''
        src_fixtures_ids = self.interface.get('FIX', parsed_input[0])
        for src_id in src_fixtures_ids:
            new_fixture = document.get_by_uuid(self.plot_file, src_id)
            new_fixture['uuid'] = str(uuid4())
            self.plot_file.append(new_fixture)

    def fixture_list(self, parsed_input):
        '''List all fixtures in the plot file.'''
        self.interface.open('FIX')
        for fixture in document.get_by_type(self.plot_file, 'fixture'):
            s = printer.get_fixture_string(fixture)
            self.interface.add(s, fixture['uuid'], 'FIX')

    def fixture_filter(self, parsed_input):
        '''List all fixtures that meet a certain criterion.'''
        self.interface.open('FIX')
        key = 'fixture-'+parsed_input[0]
        value = parsed_input[1]
        for fixture in document.get_by_type(self.plot_file, 'fixture'):
            if key in fixture:
                if fixture[key] == value:
                    s = printer.get_fixture_string(fixture)+' ('+key+'='+value+')'
                    self.interface.add(s, fixture['uuid'], 'FIX')

    def fixture_remove(self, parsed_input):
        '''Remove a fixture from the plot file.'''
        fixtures_ids = self.interface.get('FIX', parsed_input[0])
        for fixture_id in fixtures_ids:
            document.remove_by_uuid(self.plot_file, fixture_id)

    def fixture_get(self, parsed_input):
        '''Print the values of a fixture's tags.'''
        fixtures_ids = self.interface.get('FIX', parsed_input[0])
        regexp = re.compile('fixture-.*')
        for fixture_id in fixtures_ids:
            fixture = document.get_by_uuid(self.plot_file, fixture_id)
            s = printer.get_fixture_string(fixture)
            print('\033[1m'+s+'\033[0m')
            show_tags = {}
            hide_tags = {}
            for k, v in fixture.items():
                if regexp.match(k):
                    show_tags[k] = v
                else:
                    hide_tags[k] = v
            print(str(len(show_tags)), 'Data Tags: (+'+str(len(hide_tags))+' hidden)')
            for k, v in show_tags.items():
                print('    '+k+': '+v)
            

    def fixture_getall(self, parsed_input):
        '''Print the tags and functions of a fixture..'''
        fixtures = self.interface.get('FIX', parsed_input[0])
        self.interface.open('FNC')
        for fixture in fixtures:
            print('\033[1m'+fixture.name+'\033[0m')
            print(str(len(fixture.data)), 'Data Tags: ')
            for key, value in fixture.data.items():
                print('    '+key+': '+value)
            if len(fixture.functions):
                print(str(len(fixture.functions)), 'DMX Functions:')
                for function in fixture.functions:
                    s = function.name
                    self.interface.add(s, function, 'FNC', pre='    ')

    def fixture_set(self, parsed_input):
        '''Set the value of one of a fixture's tags.'''
        fixtures_ids = self.interface.get('FIX', parsed_input[0])
        tag = parsed_input[1]
        value = parsed_input[2]
        for fixture_id in fixtures_ids:
            # See if it is a special pseudo tag
            if tag in pseudotag.pseudotags:
                pseudotag.pseudotags[tag](fixture, self, value)
            else:
                fixture.data[tag] = value

    def fixture_address(self, parsed_input):
        '''Assign DMX addresses to a fixture.'''
        fixtures = self.interface.get('FIX', parsed_input[0])
        registries = self.interface.get('REG', parsed_input[1])
        for fixture in fixtures:
            n_chan = len(fixture.functions)
            for registry in registries:
                if parsed_input[2] == 'auto':
                    addr = registry.get_start_address(n_chan)
                else:
                    addr = int(parsed_input[2])
                for function in fixture.functions:
                    chan_obj = xpx.RegistryChannel(
                        address=addr, function=xpx.XPXReference(function.uuid))
                    registry.channels.append(chan_obj)
                    addr += 1

    def fixture_unaddress(self, parsed_input):
        '''Unassign addresses in all universes for this fixture.'''
        fixtures = self.interface.get('FIX', parsed_input[0])
        for fixture in fixtures:
            functions = [function.uuid for function in fixture.functions]
            for registry in self.plot_file.registries:
                # BUG: does not check last channel if len(channels) > 1
                for channel in registry.channels:
                    if channel.function.uuid in functions:
                        registry.channels.remove(channel)

    # Registry commands

    def registry_new(self, parsed_input):
        '''Create a new registry.'''
        registry = xpx.Registry(name=parsed_input[0], channels=[])
        self.plot_file.registries.append(registry)

    def registry_remove(self, parsed_input):
        '''Delete one or more registries.'''
        registries = self.interface.get('REG', parsed_input[0])
        for registry in registries:
            self.plot_file.registries.remove(registry)

    def registry_list(self, parsed_input):
        '''List all registries.'''
        self.interface.open('REG')
        for registry in self.plot_file.registries:
            s = (registry.name+' ('+str(len(registry.get_occupied_addresses()))
                 +' occupied)')
            self.interface.add(s, registry, 'REG') 

    def registry_query(self, parsed_input):
        '''List the functions of all used channels in a registry.'''
        registries = self.interface.get('REG', parsed_input[0])
        self.interface.open('FNC')
        for registry in registries:
            print('\033[1mUniverse: '+registry.name+'\033[0m')
            for channel in registry.channels:
                address = channel.address
                func = self.plot_file.get_object_by_uuid(channel.function.uuid)
                fix = self.plot_file.get_fixture_for_function(func)
                s = ('DMX'+str(format(address, '03d'))+': '+fix.name+' ('
                     +func.name+')')
                self.interface.add(s, func, 'FNC')

    def registry_probe(self, parsed_input):
        '''List channels and dimmer controlled lights.'''
        registries = self.interface.get('REG', parsed_input[0])
        self.interface.open('FNC')
        for registry in registries:
            print('\033[1mUniverse: '+registry.name+'\033[0m')
            for channel in registry.channels:
                address = channel.address
                func = self.plot_file.get_object_by_uuid(channel.function.uuid)
                fixture = self.plot_file.get_fixture_for_function(func)
                s = ('DMX'+str(format(address, '03d'))+': '+fixture.name+' ('
                     +func.name+')')
                self.interface.add(s, func, 'FNC')
                controlled = self.plot_file.get_fixtures_for_dimmer_function(func)
                for dimmed_fixture in controlled:
                    print('\t→ '+dimmed_fixture.name)

    def registry_add(self, parsed_input):
        '''Manually add a function to a registry.'''
        functions = self.interface.get('FNC', parsed_input[0])
        registries = self.interface.get('REG', parsed_input[1])
        n_chan = len(functions)
        if parsed_input[2] == 'auto':
            addr = registry.get_start_address(n_chan)
        else:
            addr = int(parsed_input[2])
        for function in functions:
            chan_obj = xpx.RegistryChannel(address=addr, function=function)
            registry.channels.append(chan_obj)
            addr += 1

    # Scene commands

    def scene_list(self, parsed_input):
        '''List all scenes.'''
        self.interface.open('SCN')
        for scene in self.plot_file.scenes:
            s = scene.name+' (Affects '+str(len(scene.outputs))+' functions)'
            self.interface.add(s, scene, 'SCN')

    def scene_new(self, parsed_input):
        '''Create a new scene.'''
        outputs = []
        for output in parsed_input[0].split(';'):
            functions = self.interface.get('FNC', output.split('@')[0])
            for function in functions:
                outputs.append(xpx.OutputState(
                    function=xpx.XPXReference(function.uuid),
                    value=output.split('@')[1]))
        self.plot_file.scenes.append(xpx.Scene(outputs=outputs, 
                                               name=parsed_input[1]))

    def scene_getall(self, parsed_input):
        '''Display the outputs of a scene.'''
        self.interface.open('FNC')
        scenes = self.interface.get('SCN', parsed_input[0])
        for scene in scenes:
            print('\033[1mScene: '+scene.name+'\033[0m')
            for output in scene.outputs:
                function = self.plot_file.get_object_by_uuid(
                    output.function.uuid)
                value = clihelper.ProgressBar()
                value = value+output.value
                fixture = self.plot_file.get_fixture_for_function(function)
                s = str(value)+' '+function.name+' ('+fixture.name+')'
                self.interface.add(s, function, 'FNC')

    def scene_getall_dmx(self, parsed_input):
        '''Display the outputs of a scene in terms of DMX channels.'''
        self.interface.open('FNC')
        scenes = self.interface.get('SCN', parsed_input[0])
        for scene in scenes:
            printlines = []
            registries = []
            print('\033[1mScene: '+scene.name+'\033[0m')
            for output in scene.outputs:
                function = self.plot_file.get_object_by_uuid(
                    output.function.uuid)
                channels = self.plot_file.get_channels_for_function(function)
                for channel in channels:
                    registry = self.plot_file.get_registry_for_channel(channel)
                    if registry not in registries:
                        registries.append(registry)
                    printlines.append((registry, channel, output.value))
            for registry in registries:
                print('\033[3mRegistry: '+registry.name+'\033[0m')
                for printline in printlines:
                    if printline[0] == registry:
                        value = clihelper.ProgressBar()
                        value = value+printline[2]
                        s = ('DMX'+str(format(printline[1].address, '03d'))+
                             ' '+str(value))
                        self.interface.add(s, printline[1].function, 'FNC')
                

    def scene_remove(self, parsed_input):
        '''Remove a scene.'''
        scenes = self.interface.get('SCN', parsed_input[0])
        for scene in scenes:
            self.plot_file.remove(scene)

    # Chase commands


def get_context():
    return EditorContext()
