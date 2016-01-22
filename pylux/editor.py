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
import logging
from pylux import get_data


def file_open(inputs):
    try:
        PLOT_FILE.load(inputs[1])
    except IndexError:
        print('Error: You need to specify a file path to load')
    except AttributeError:
        pass


def file_write(inputs):
    try:
        PLOT_FILE.save()
    except AttributeError:
        print('Error: No file is loaded')


def file_writeas(inputs):
    try:
        PLOT_FILE.saveas(inputs[1])
    except IndexError:
        print('Error: You need to specify a destination path!')


def file_get(inputs):
    print('Using plot file '+PLOT_FILE.file)


def file_new(inputs):
    PLOT_FILE.generate(os.path.expanduser(inputs[1]))
    PLOT_FILE.load(os.path.expanduser(inputs[1]))
    file_get(inputs)


def metadata_list(inputs):
    metadata = plot.Metadata(PLOT_FILE)
    for i in metadata.meta:
        print(i+': '+metadata.meta[i])


def metadata_set(inputs):
    metadata = plot.Metadata(PLOT_FILE)
    metadata.meta[inputs[1]] = clihelper.resolve_input(inputs, 2)[-1]
    metadata.save()


def metadata_remove(inputs):
    metadata = plot.Metadata(PLOT_FILE)
    metadata.meta[inputs[1]] = None
    metadata.save()


def metadata_get(inputs):
    metadata = plot.Metadata(PLOT_FILE)
    print(inputs[1]+': '+metadata.meta[inputs[1]])


def fixture_new(inputs):
    fixture = plot.Fixture(PLOT_FILE)
    try:
        fixture.new(inputs[1], FIXTURES_DIR)
    except FileNotFoundError:
        print('Error: Couldn\'t find a fixture file with this name')
    else:
        fixture.add()
        fixture.save()


def fixture_clone(inputs):
    src_fixture = INTERFACE.get(inputs[1])
    if len(src_fixture) > 1:
        print('Error: You can only clone one fixture!')
    else:
        new_fixture = plot.Fixture(PLOT_FILE, FIXTURES_DIR)
        new_fixture.clone(src_fixture[0])
        new_fixture.add()
        new_fixture.save()


def fixture_list(inputs):
    fixtures = plot.FixtureList(PLOT_FILE)
    i = 1
    INTERFACE.clear()
    for fixture in fixtures.fixtures:
        if 'name' in fixture.data:
            name = fixture.data['name']
        else:
            name = fixture.data['type']
        print('\033[4m'+str(i)+'\033[0m '+name+', id: '+fixture.uuid)
        INTERFACE.append(i, fixture)
        i = i+1


def fixture_filter(inputs):
    try:
        key = inputs[1]
        value = clihelper.resolve_input(inputs, 2)[-1]
        fixtures = plot.FixtureList(PLOT_FILE)
        INTERFACE.clear()
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
                    INTERFACE.append(i, fixture)
                    i = i+1
            else:
                pass
    except IndexError:
        print('Error: You need to specify a key and value!')


def fixture_remove(inputs):
    fixture_list = plot.FixtureList(PLOT_FILE)
    fixtures = INTERFACE.get(inputs[1])
    for fixture in fixtures:
        fixture_list.remove(fixture)


def fixture_get(inputs):
    fixtures = INTERFACE.get(inputs[1])
    for fixture in fixtures:
        if inputs[2] in fixture.data:
            print(fixture.data[inputs[2]])
        else:
            print(None)
    INTERFACE.update_this(inputs[1])


def fixture_getall(inputs):
    fixtures = INTERFACE.get(inputs[1])
    for fixture in fixtures:
        for data_item in fixture.data:
            print(data_item+': '+str(fixture.data[data_item]))
    INTERFACE.update_this(inputs[1])


def fixture_set(inputs):
    fixtures = INTERFACE.get(inputs[1])
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
            fixture.data['dimmer_uuid'] = INTERFACE.get(inputs[3])[0].uuid
            fixture.data['dimmer_channel'] = inputs[4]
        # Otherwise just set it
        else:
            fixture.data[tag] = value
        fixture.save()
    INTERFACE.update_this(inputs[1])


def fixture_address(inputs):
    fixtures = INTERFACE.get(inputs[1])
    if len(fixtures) > 1 and inputs[3] != 'auto':
        print('Error: You must specify auto if you address more than '
              'one fixture.')
    else:
        registry = plot.DmxRegistry(PLOT_FILE, inputs[2])
        for fixture in fixtures:
            registry.address(fixture, inputs[3])
    INTERFACE.update_this(inputs[1])


def fixture_purge(inputs):
    fixtures = INTERFACE.get(inputs[1])
    for fixture in fixtures:
        registry = plot.DmxRegistry(PLOT_FILE, fixture.data['universe'])
        registry.unaddress(fixture)
        fixture_list = plot.FixtureList(PLOT_FILE)
        fixture_list.remove(fixture)


def registry_list(inputs):
    try:
        registry = plot.DmxRegistry(PLOT_FILE, inputs[1])
        for channel in registry.registry:
            uuid = registry.registry[channel][0]
            func = registry.registry[channel][1]
            print(str(format(channel, '03d'))+' uuid: '+uuid+', func: '+func)
    except IndexError:
        print('You need to specify a DMX registry!')


def cue_list(inputs):
    cues = plot.CueList(PLOT_FILE)
    INTERFACE.clear()
    for cue in cues.cues:
        cue_type = cue.data['type']
        cue_location = cue.data['location']
        print('\033[4m'+str(cue.key)+'\033[0m ('+cue_type+') at '+
              cue_location)
        INTERFACE.append(cue.key, cue)


def cue_new(inputs):
    cue = plot.Cue(PLOT_FILE)
    cue.data['type'] = inputs[1]
    cue.data['location'] = clihelper.resolve_input(inputs, 2)[-1]
    cue.save(PLOT_FILE)


def cue_remove(inputs):
    cues = plot.CueList(PLOT_FILE)
    removal_candidates = INTERFACE.get(inputs[1])
    for rc in removal_candidates:
        cues.remove(PLOT_FILE, rc.uuid)


def cue_set(inputs):
    cues_to_change = INTERFACE.get(inputs[1])
    for cue in cues_to_change:
        cue.data[inputs[2]] = clihelper.resolve_input(inputs, 3)[-1]
        cue.save(PLOT_FILE)


def cue_get(inputs):
    cues_to_get = INTERFACE.get(inputs[1])
    for cue in cues_to_get:
        if inputs[2] in cue.data:
            print(cue.data[inputs[2]])
        else:
            print(None)


def cue_getall(inputs):
    cues_to_get = INTERFACE.get(inputs[1])
    for cue in cues_to_get:
        for data_item in cue.data:
            print(data_item+': '+cue.data[data_item])


def cue_moveafter(inputs):
    cues = plot.CueList(PLOT_FILE)
    cues.move_after(PLOT_FILE, int(inputs[1]), int(inputs[2]))


def cue_movebefore(inputs):
    cues = plot.CueList(PLOT_FILE)
    cues.move_before(PLOT_FILE, int(inputs[1]), int(inputs[2]))


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


def main():
    """The main user loop."""
    global INTERFACE
    INTERFACE = clihelper.Interface()
    global FIXTURES_DIR 
    FIXTURES_DIR = get_data('fixture')

    functions_dict = {
        'fo': file_open,
        'fw': file_write,
        'fW': file_writeas,
        'fg': file_get,
        'fn': file_new,
        'mG': metadata_list,
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
        'ql': cue_list,
        'qn': cue_new,
        'qr': cue_remove,
        'qs': cue_set,
        'qg': cue_get,
        'qG': cue_getall,
        'qm': cue_moveafter,
        'qM': cue_movebefore,
        'h': utility_help,
        'c': utility_clear,
        'q': utility_quit,
        'Q': utility_kill}
        
    print('Welcome to Pylux! Type \'h\' to view a list of commands.')
    # Begin the main loop
    logging.basicConfig(level=LOG_LEVEL)
    while True:
        user_input = input(CONFIG['cli']['prompt']+' ')
        inputs = user_input.split(' ')

        if inputs[0][0] == ':':
            init_globals = {
                'PLOT_FILE': PLOT_FILE,
                'CONFIG': CONFIG,
                'LOG_LEVEL': LOG_LEVEL}
            extensions_dir = '/usr/share/pylux/extension/'
            module_name = inputs[0].split(':')[1]
            try:
                runpy.run_path(extensions_dir+module_name+'.py',
                               init_globals=init_globals, run_name='pyext')
            except FileNotFoundError:
                print('No extension with this name!')

        if inputs[0] in functions_dict:
            functions_dict[inputs[0]](inputs)

        else:
            print('Error: Command doesn\'t exist.') 
            print('Type \'h\' for a list of available commands.')

if __name__ == 'pylux_root':
    main()
