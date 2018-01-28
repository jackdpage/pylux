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

import json
import re
import uuid

import clihelper
from context.context import Context, Command
import document
from lib import data, printer


class EditorContext(Context):

    def __init__(self):
        """Registers commands."""
        super().__init__()
        self.name = 'editor'

        # Command Registration

        self.register(Command('ml', self.metadata_list, []))
        self.register(Command('mn', self.metadata_new, [
            ('ref', True, 'Reference to assign to the metadata.'),
            ('name', True, 'The name of the metadata to add.')]))
        self.register(Command('ms', self.metadata_set, [
            ('ref', True, 'The metadata to set the value of.'),
            ('value', True, 'Value for the metadata to take.')]))
        self.register(Command('mr', self.metadata_remove, [
            ('ref', True, 'The metadata to remove.')]))
        self.register(Command('mg', self.metadata_get, [
            ('name', True, 'Name of the metadata to print the value of.')]))

        self.register(Command('xn', self.fixture_new, [
            ('ref', True, 'The reference to give this new fixture.')]))
        self.register(Command('xN', self.fixture_from_template, [
            ('ref', True, 'The reference to give this new fixture.'),
            ('template', True, 'Path to the file to load data from.')]))
        self.register(Command('xc', self.fixture_clone, [
            ('src', True, 'The fixture to make a copy of.'),
            ('dest', True, 'References to clone the fixture to.')]))
        self.register(Command('xl', self.fixture_list, []))
        self.register(Command('xf', self.fixture_filter, [
            ('tag', True, 'The tag to filter by.'),
            ('value', True, 'The value the tag must be to be displayed.')]))
        self.register(Command('xr', self.fixture_remove, [
            ('ref', True, 'The fixture to remove.')]))
        self.register(Command('xg', self.fixture_get, [
            ('ref', True, 'The fixture to get a tag from.'),
            ('tag', True, 'The name of the tag to print the value of.')]))
        self.register(Command('xG', self.fixture_getall, [
            ('FIX', True, 'The fixture to print the tags of.')]))
        self.register(Command('xs', self.fixture_set, [
             ('FIX', True, 'The fixture to set a tag of.'),
             ('tag', True, 'The name of the tag to set.'),
             ('value', True, 'The value to set the tag to.')]))
        self.register(Command('xa', self.fixture_address, [
             ('ref', True, 'The fixture to assign addresses to.'),
             ('reg', True, 'The name of the universe to address in.'),
             ('addr', True, 'The addresses to begin addressing at.')]))
        # self.register(Command('xA', self.fixture_unaddress, [
        #     ('FIX', True, 'The fixture to unassign addresses for.')]))

        self.register(Command('rl', self.registry_list, []))
        self.register(Command('rL', self.registry_query, [
            ('REG', True, 'The registry to list used channels of.')]))
        self.register(Command('rn', self.registry_new, [
            ('ref', True, 'The reference to give this new registry.'),
            ('name', True, 'The name of the new registry.')]))
        # self.register(Command('rp', self.registry_probe, [
        #     ('REG', True, 'The registry to probe the channels of.')]))
        self.register(Command('rr', self.registry_remove, [
            ('registry', True, 'The registry to remove.')]))
        # self.register(Command('ra', self.registry_add, [
        #     ('FNC', True, 'The function(s) to address.'),
        #     ('REG', True, 'The name of the registry to address in.'),
        #     ('address', True, 'The address to begin addressing at.')]))

        # self.register(Command('sl', self.scene_list, []))
        # self.register(Command('sn', self.scene_new, [
        #     ('outputs', True, 'In the form FNC@###;FNC@###.'),
        #     ('name', True, 'The name of the scene.')]))
        # self.register(Command('sg', self.scene_getall, [
        #     ('SCN', True, 'The scene to display the outputs of.')]))
        # self.register(Command('sG', self.scene_getall_dmx, [
        #     ('SCN', True, 'The scene to display the outputs of.')]))

    def post_init(self):
        pass

    # Metadata commands

    def metadata_list(self, parsed_input):
        '''List the values of all metadata in the plot file.'''
        for meta in clihelper.refsort(document.get_metadata(self.plot_file)):
            clihelper.print_object(meta)

    def metadata_set(self, parsed_input):
        refs = clihelper.resolve_references(parsed_input[0])
        objs = [document.get_by_ref(self.plot_file, 'metadata', ref) for ref in refs]
        for obj in objs:
            obj['metadata-value'] = parsed_input[1]
            obj['name'] = parsed_input[1]

    def metadata_remove(self, parsed_input):
        '''Remove a piece of metadata from the file.'''
        refs = clihelper.resolve_references(parsed_input[0])
        for ref in refs:
            document.remove_by_ref(self.plot_file, 'metadata', ref)

    def metadata_get(self, parsed_input):
        '''Print the values of metadata matching a name.'''
        for match in document.get_by_value(self.plot_file, 'metadata-key', parsed_input[0]):
            clihelper.print_object(match)

    def metadata_new(self, parsed_input):
        '''Create a new metadata item.'''
        if parsed_input[0] == 'auto':
            refs = [document.autoref(self.plot_file, 'metadata')]
        else:
            refs = clihelper.resolve_references(parsed_input[0])
        for ref in refs:
            self.plot_file.append({
                'type': 'metadata',
                'uuid': str(uuid.uuid4()),
                'ref': ref,
                'name': parsed_input[1],
                'metadata-key': parsed_input[1]
            })

    # Fixture commands

    def fixture_new(self, parsed_input):
        '''Create a new fixture from scratch.'''
        if parsed_input[0] == 'auto':
            refs = [document.autoref(self.plot_file, 'fixture')]
        else:
            refs = clihelper.resolve_references(parsed_input[0])
        for ref in refs:
            self.plot_file.append({
                'type': 'fixture',
                'uuid': str(uuid.uuid4()),
                'ref': ref
            })

    def fixture_from_template(self, parsed_input):
        '''Create a new fixture from a template file.'''
        if parsed_input[0] == 'auto':
            refs = [document.autoref(self.plot_file, 'fixture')]
        else:
            refs = clihelper.resolve_references(parsed_input[0])
        template_file = data.get_data('fixture/'+parsed_input[1]+'.json')
        if not template_file:
            print('does not exist')
        else:
            for ref in refs:
                with open(template_file) as f:
                    fixture = json.load(f)
                fixture['ref'] = ref
                fixture['uuid'] = str(uuid.uuid4())
                if 'fixture-functions' in fixture:
                    for function in fixture['fixture-functions']:
                        function['uuid'] = str(uuid.uuid4())
                self.plot_file.append(fixture)

    def fixture_clone(self, parsed_input):
        '''Create a new fixture by copying an existing fixture.'''
        src = document.get_by_ref(self.plot_file, 'fixture', int(parsed_input[0]))
        dest = clihelper.resolve_references(parsed_input[1])
        for loc in dest:
            new = dict.copy(src)
            new['uuid'] = str(uuid.uuid4())
            new['ref'] = loc
            self.plot_file.append(new)

    def fixture_list(self, parsed_input):
        '''List all fixtures in the plot file.'''
        for fix in clihelper.refsort(document.get_by_type(self.plot_file, 'fixture')):
            clihelper.print_object(fix)

    def fixture_filter(self, parsed_input):
        '''List all fixtures that meet a certain criterion.'''
        k = parsed_input[0]
        v = parsed_input[1]
        fixtures = document.get_by_type(self.plot_file, 'fixture')
        for match in document.get_by_value(fixtures, k, v):
            clihelper.print_object(match)

    def fixture_remove(self, parsed_input):
        '''Remove a fixture from the plot file.'''
        refs = clihelper.resolve_references(parsed_input[0])
        for ref in refs:
            document.remove_by_ref(self.plot_file, 'fixture', ref)

    def fixture_get(self, parsed_input):
        '''Print the values of a fixture's tags.'''
        refs = clihelper.resolve_references(parsed_input[0])
        for ref in refs:
            f = document.get_by_ref(self.plot_file, 'fixture', ref)
            clihelper.print_object(f)
            print(str(len(f)), 'Data Tags:')
            for k, v in sorted(f.items()):
                print('    '+str(k)+': '+str(v))

    def fixture_getall(self, parsed_input):
        '''Print the tags and functions of a fixture..'''
        refs = clihelper.resolve_references(parsed_input[0])
        for ref in refs:
            f = document.get_by_ref(self.plot_file, 'fixture', ref)
            clihelper.print_object(f)
            print(str(len(f)), 'Data Tags:')
            for k, v in sorted(f.items()):
                print('    ' + str(k) + ': ' + str(v))
            if len(f['fixture-functions']):
                print(str(len(f['fixture-functions'])), 'DMX Functions:')
                for func in f['fixture-functions']:
                    print('   ', printer.get_generic_string(func))

    def fixture_set(self, parsed_input):
        '''Set the value of one of a fixture's tags.'''
        refs = clihelper.resolve_references(parsed_input[0])
        objs = [document.get_by_ref(self.plot_file, 'fixture', ref) for ref in refs]
        for obj in objs:
            obj[parsed_input[1]] = parsed_input[2]

    def fixture_address(self, parsed_input):
        '''Assign DMX addresses to a fixture.'''
        refs = clihelper.resolve_references(parsed_input[0])
        reg = document.get_by_ref(self.plot_file, 'registry', int(parsed_input[1]))
        for ref in refs:
            f = document.get_by_ref(self.plot_file, 'fixture', ref)
            if parsed_input[2] == 'auto':
                n = len(f['fixture-functions'])
                addr = document.get_start_address(reg, n)
            else:
                addr = int(parsed_input[2])
            for func in f['fixture-functions']:
                reg['table'][addr] = func['uuid']
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
        if parsed_input[0] == 'auto':
            refs = [document.autoref(self.plot_file, 'registry')]
        else:
            refs = clihelper.resolve_references(parsed_input[0])
        for ref in refs:
            self.plot_file.append({
                'type': 'registry',
                'uuid': str(uuid.uuid4()),
                'ref': ref,
                'table': {}
            })

    def registry_remove(self, parsed_input):
        '''Delete one or more registries.'''
        refs = clihelper.resolve_references(parsed_input[0])
        for ref in refs:
            document.remove_by_ref(self.plot_file, 'registry', ref)

    def registry_list(self, parsed_input):
        '''List all registries.'''
        for reg in clihelper.refsort(document.get_by_type(self.plot_file, 'registry')):
            clihelper.print_object(reg)

    def registry_query(self, parsed_input):
        '''List the functions of all used channels in a registry.'''
        refs = clihelper.resolve_references(parsed_input[0])
        for ref in refs:
            r = document.get_by_ref(self.plot_file, 'registry', ref)
            clihelper.print_object(r)
            t = {int(i): r['table'][i] for i in r['table']}
            print(str(len(t)), 'Used Addresses:')
            for k, v in sorted(t.items()):
                func = document.get_function_by_uuid(self.plot_file, v)
                f = document.get_function_parent(self.plot_file, func)
                print(''.join(['DMX',str(format(k, '03d')),': ',
                               printer.get_generic_string(f),' (',
                               printer.get_generic_string(func),')']))

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
