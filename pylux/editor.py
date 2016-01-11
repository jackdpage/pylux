# editor.py is part of Pylux
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

"""Edit the content of Pylux plot files.

editor is a CLI implementation of the Pylux plot editor, allowing 
for the reading and editing of Pylux plot files.
"""

import os
import sys
import pylux.plot as plot
import pylux.clihelper as clihelper
import runpy


def file_open(inputs):
    try:
        globals['plot_file'].load(inputs[1])
    except IndexError:
        print('Error: You need to specify a file path to load')
    except AttributeError:
        pass

def file_write(inputs):
    try:
        globals['plot_file'].save()
    except AttributeError:
        print('Error: No file is loaded')

def file_writeas(inputs):
    try:
        globals['plot_file'].saveas(inputs[1])
    except IndexError:
        print('Error: You need to specify a destination path!')

def file_get(inputs):
    print('Using plot file '+globals['plot_file'].file)

def file_new(inputs):
    globals['plot_file'].generate(os.path.expanduser(inputs[1]))
    globals['plot_file'].load(os.path.expanduser(inputs[1]))
    file_get(inputs)

def metadata_list(inputs):
    metadata = plot.Metadata(globals['plot_file'])
    for i in metadata.meta:
        print(i+': '+metadata.meta[i])

def metadata_set(inputs):
    metadata = plot.Metadata(globals['plot_file'])
    metadata.meta[inputs[1]] = clihelper.resolve_input(inputs, 2)[-1]
    metadata.save()
     
def metadata_remove(inputs):
    metadata = plot.Metadata(globals['plot_file'])
    metadata.meta[inputs[1]] = None
    metadata.save()

def metadata_get(inputs):
    metadata = plot.Metadata(globals['plot_file'])
    print(inputs[1]+': '+metadata.meta[inputs[1]])

def fixture_new(inputs):
    fixture = plot.Fixture(globals['plot_file'])
    try:
        fixture.new(inputs[1], globals['fixtures_dir'])
    except FileNotFoundError:
        print('Error: Couldn\'t find a fixture file with this name')
    else:
        fixture.add()
        fixture.save()

def fixture_clone(inputs):
    src_fixture = globals['interface'].get(inputs[1])
    if len(src_fixture) > 1:
        print('Error: You can only clone one fixture!')
    else:
        new_fixture = plot.Fixture(globals['plot_file'], 
            globals['fixtures_dir'])
        new_fixture.clone(src_fixture[0])
        new_fixture.add()
        new_fixture.save()

def fixture_list(inputs):
    fixtures = plot.FixtureList(globals['plot_file'])
    i = 1
    globals['interface'].clear()
    for fixture in fixtures.fixtures:
        if 'name' in fixture.data:
            name = fixture.data['name']
        else:
            name = fixture.data['type']
        print('\033[4m'+str(i)+'\033[0m '+name+', id: '+fixture.uuid)
        globals['interface'].append(i, fixture)
        i = i+1

def fixture_filter(inputs):
    try:
        key = inputs[1]
        value = clihelper.resolve_input(inputs, 2)[-1]
        fixtures = plot.FixtureList(globals['plot_file'])
        globals['interface'].clear()
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
                    globals['interface'].append(i, fixture)
                    i = i+1
            else:
                pass
    except IndexError:
        print('Error: You need to specify a key and value!')

def fixture_remove(inputs):
    fixture_list = plot.FixtureList(globals['plot_file'])
    fixtures = globals['interface'].get(inputs[1])
    for fixture in fixtures:
        fixture_list.remove(fixture)

def fixture_get(inputs):
    fixtures = globals['interface'].get(inputs[1])
    for fixture in fixtures:
        if inputs[2] in fixture.data:
            print(fixture.data[inputs[2]])
        else:
            print(None)
    globals['interface'].update_this(inputs[1])

def fixture_getall(inputs):
    fixtures = globals['interface'].get(inputs[1])
    for fixture in fixtures:
        for data_item in fixture.data:
            print(data_item+': '+str(fixture.data[data_item]))
    globals['interface'].update_this(inputs[1])

def fixture_set(inputs):
    fixtures = globals['interface'].get(inputs[1])
    tag = inputs[2]
    value = clihelper.resolve_input(inputs, 3)[-1]
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
            fixture.data['dimmer_uuid'] = globals['interface'].get(inputs[3])[0].uuid
            fixture.data['dimmer_channel'] = inputs[4]
        # Otherwise just set it
        else:
            fixture.data[tag] = value
        fixture.save()
    globals['interface'].update_this(inputs[1])

def fixture_address(inputs):
    fixtures = globals['interface'].get(inputs[1])
    if len(fixtures) > 1 and inputs[3] != 'auto':
        print('Error: You must specify auto if you address more than '
            'one fixture.')
    else:
        registry = plot.DmxRegistry(globals['plot_file'], inputs[2])
        for fixture in fixtures:
            registry.address(fixture, inputs[3])
    globals['interface'].update_this(inputs[1])


def fixture_purge(inputs):
    fixtures = globals['interface'].get(inputs[1])
    for fixture in fixtures:
        registry = plot.DmxRegistry(globals['plot_file'], 
            fixture.data['universe'])
        registry.unaddress(fixture)
        fixture_list = plot.FixtureList(globals['plot_file'])
        fixture_list.remove(fixture)

def registry_list(inputs):
    try:
        registry = plot.DmxRegistry(globals['plot_file'], inputs[1])
        for channel in registry.registry:
            uuid = registry.registry[channel][0]
            func = registry.registry[channel][1]
            print(str(format(channel, '03d'))+' uuid: '+uuid+', func: '+func)
    except IndexError:
        print('You need to specify a DMX registry!')

def utility_help(inputs):
    text = ""
    with open('help.txt') as man:
        for line in man:
            text = text+line
    print(text)

def utility_clear(inputs):
    os.system('cls' if os.name == 'nt' else 'clear')
    
def utility_quit(inputs):
    print('Autosaving changes...')
    file_write(inputs)
    sys.exit()

def utility_kill(inputs):
    print('Ignoring changes and exiting...')
    sys.exit()


def main(plot_file, config):
    """The main user loop."""
    interface = clihelper.Interface()
    global globals
    globals = {
        'plot_file': plot_file, 
        'config': config, 
        'interface': interface,
        'fixtures_dir': '/usr/share/pylux/fixture/'}

    functions_dict = {
        'fo': file_open,
        'fw': file_write,
        'fW': file_writeas,
        'fg': file_get,
        'fn': file_new,
        'ml': metadata_list,
        'ms': metadata_set,
        'mr': metadata_remove,
        'mg': metadata_get,
        'xn': fixture_new,
        'xc': fixture_clone,
        'xl': fixture_list,
        'xf': fixture_filter,
        'xr': fixture_remove,
        'xg': fixture_get,
        'xG': fixture_getall,
        'xs': fixture_set,
        'xa': fixture_address,
        'xp': fixture_purge,
        'rl': registry_list,
        'h': utility_help,
        'c': utility_clear,
        'q': utility_quit,
        'Q': utility_kill}
        
    print('Welcome to Pylux! Type \'h\' to view a list of commands.')
    # Begin the main loop
    while True:
        user_input = input(config['Settings']['prompt']+' ')
        inputs = user_input.split(' ')

        if inputs[0][0] == ':':
            extensions_dir = '/usr/share/pylux/extension/'
            module_name = inputs[0].split(':')[1]
            try:
                runpy.run_path(extensions_dir+module_name+'.py',
                    init_globals={'plot_file': plot_file}, run_name='pyext')
            except FileNotFoundError:
                print('No extension with this name!')

        else:
            try:
                functions_dict[inputs[0]](inputs)
            except KeyError:
                print('Error: Command doesn\'t exist.') 
                print('Type \'h\' for a list of available commands.')
