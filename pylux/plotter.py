#!/usr/bin/python3

# plotter.py is part of Pylux
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

import os
import sys
from __init__ import __version__
import plot
import clihelper
import importlib.util as IL


def get_olf_library():
    """Return a list of the installed OLF files."""
    library = os.listdir(OL_FIXTURES_DIR)
    for olf in library:
        olid = olf.split('.')[0]
        library[library.index(olf)] = olid
    return library


def get_command_list():
    """Display the help page."""
    text = ""
    with open('help.txt') as man:
        for line in man:
            text = text+line
    print(text)


def main(plot_file, config):
    """The main user loop."""
    interface = clihelper.Interface()
    prompt = config['Settings']['prompt']+' '
    fixtures_dir = os.path.expanduser(config['Fixtures']['dir'])
    print('Welcome to Pylux! Type \'h\' to view a list of commands.')
    # Begin the main loop
    while True:
        user_input = input(config['Settings']['prompt']+' ')
        inputs = []
        for i in user_input.split(' '):
            inputs.append(i)

        # File actions
        if inputs[0] == 'fl':
            try:
                plot_file.load(inputs[1])
            except UnboundLocalError:
                print('Error: You need to specify a file path to load')

        elif inputs[0] == 'fs':
            plot_file.save()

        elif inputs[0] == 'fS':
            try:
                plot_file.saveas(inputs[1])
            except IndexError:
                print('Error: You need to specify a destination path!')

        elif inputs[0] == 'fp':
            print('Using plot file '+plot_file.file)

        elif inputs[0] == 'fn':
            plot_file.generate(os.path.expanduser(inputs[1]))
            plot_file.load(os.path.expanduser(inputs[1]))
            print('Using plot file '+plot_file.file)

        # Metadata actions
        elif inputs[0] == 'ml':
            metadata = plot.Metadata(plot_file)
            for i in metadata.meta:
                print(i+': '+metadata.meta[i])

        elif inputs[0] == 'ma':
            metadata = plot.Metadata(plot_file)
            metadata.meta[inputs[1]] = clihelper.resolve_input(inputs, 2)[-1]
            metadata.save()

        elif inputs[0] == 'mr':
            metadata = plot.Metadata(plot_file)
            metadata.meta[inputs[1]] = None
            metadata.save()

        elif inputs[0] == 'mg':
            metadata = plot.Metadata(plot_file)
            print(inputs[1]+': '+metadata.meta[inputs[1]])

        # Fixture actions
        elif inputs[0] == 'xa':
            fixture = plot.Fixture(plot_file)
            try:
                fixture.new(inputs[1], fixtures_dir)
            except FileNotFoundError:
                print('Error: Couldn\'t find an OLF file with OLID '+inputs[1])
            else:
                fixture.add()
                fixture.save()
                interface.option_list['this'] = fixture

        elif inputs[0] == 'xc':
            src_fixture = interface.get(inputs[1])
            new_fixture = plot.Fixture(plot_file, fixtures_dir)
            new_fixture.clone(src_fixture)
            new_fixture.add()
            new_fixture.save()

        elif inputs[0] == 'xl':
            fixtures = plot.FixtureList(plot_file)
            i = 1
            interface.clear()
            for fixture in fixtures.fixtures:
                print('\033[4m'+str(i)+'\033[0m '+fixture.olid+', id: '+
                    fixture.uuid)
                interface.append(i, fixture)
                i = i+1

        elif inputs[0] == 'xf':
            try:
                key = inputs[1]
                value = clihelper.resolve_input(inputs, 2)[-1]
                fixtures = plot.FixtureList(plot_file)
                interface.clear()
                i = 1
                for fixture in fixtures.fixtures:
                    if key == 'olid':
                        test_value = fixture.olid
                    else:
                        try:
                            test_value = fixture.data[key]
                        except IndexError:
                            pass
                    if test_value == value:
                        print('\033[4m'+str(i)+'\033[0m '+fixture.olid+
                            ', id: '+fixture.uuid+', '+key+': '+value)
                        interface.append(i, fixture)
                        i = i+1
                        
            except IndexError:
                print('Error: You need to specify a key and value!')

        elif inputs[0] == 'xr':
            try:
                fixtures = plot.FixtureList(plot_file)
                fixtures.remove(interface.get(inputs[1]))
            except IndexError:
                print('Error: You need to run either xl or xf then specify the'
                      ' interface id of the fixture you wish to remove')

        elif inputs[0] == 'xi':
            fixture = interface.get(inputs[1])
            for data_item in fixture.data:
                print(data_item+': '+fixture.data[data_item])
            interface.option_list['this'] = fixture

        elif inputs[0] == 'xs':
            fixture = interface.get(inputs[1])
            fixture.data[inputs[2]] = clihelper.resolve_input(inputs, 3)[-1]
            fixture.save()
            interface.option_list['this'] = fixture

        elif inputs[0] == 'xA':
            fixture = interface.get(inputs[1])
            registry = plot.DmxRegistry(plot_file, inputs[2])
            registry.address(fixture, inputs[3])
            interface.option_list['this'] = fixture

        elif inputs[0] == 'xp':
            fixture = interface.get(inputs[1])
            registry = plot.DmxRegistry(plot_file, fixture.data['universe'])
            registry.unaddress(fixture)
            fixtures = plot.FixtureList(plot_file)
            fixtures.remove(fixture)

        # DMX registry actions
        elif inputs[0] == 'rl':
            try:
                registry = plot.DmxRegistry(plot_file, inputs[1])
                interface.clear()
                for channel in registry.registry:
                    uuid = registry.registry[channel][0]
                    func = registry.registry[channel][1]
                    print('\033[4m'+str(format(channel, '03d'))+
                        '\033[0m uuid: '+uuid+', func: '+func)
                    interface.append(channel, plot.Fixture(plot_file, uuid))
            except IndexError:
                print('You need to specify a DMX registry!')

        # Extension actions
        elif inputs[0][0] == ':':
            extensions_dir = os.path.expanduser('~/.pylux/extension/')
            module_name = inputs[0].split(':')[1]
            try:
                ext_spec = IL.spec_from_file_location(module_name, 
                    extensions_dir+module_name+'.py')
                ext_module = IL.module_from_spec(ext_spec)
                ext_spec.loader.exec_module(ext_module)
            except ImportError:
                print('No extension with this name!')
            else:
                ext_module.run_pylux_extension(plot_file)
                #try:
                #except Exception:
                #    print('This module is not a valid Pylux extension!')

        # Utility actions
        elif inputs[0] == 'h':
            get_command_list()

        elif inputs[0] == 'c':
            os.system('cls' if os.name == 'nt' else 'clear')

        elif inputs[0] == 'q':
            print('Autosaving changes...')
            plot_file.save()
            sys.exit()

        elif inputs[0] == 'Q':
            print('Ignoring changes and exiting...')
            sys.exit()

        else:
            print('Error: Command doesn\'t exist.') 
            print('Type \'h\' for a list of available commands.')


# Check that the program isn't imported, then run main
if __name__ == '__main__':
    main()
