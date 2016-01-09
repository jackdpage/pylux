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
import plot
import clihelper
import runpy


def main(plot_file, config):
    """The main user loop."""
    interface = clihelper.Interface()
    prompt = config['Settings']['prompt']+' '
    fixtures_dir = '/usr/share/pylux/fixture/'
    print('Welcome to Pylux! Type \'h\' to view a list of commands.')
    # Begin the main loop
    while True:
        user_input = input(config['Settings']['prompt']+' ')
        inputs = user_input.split(' ')

        # File actions
        if inputs[0] == 'fo':
            try:
                plot_file.load(inputs[1])
            except UnboundLocalError:
                print('Error: You need to specify a file path to load')

        elif inputs[0] == 'fw':
            plot_file.save()

        elif inputs[0] == 'fW':
            try:
                plot_file.saveas(inputs[1])
            except IndexError:
                print('Error: You need to specify a destination path!')

        elif inputs[0] == 'fg':
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

        elif inputs[0] == 'ms':
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
        elif inputs[0] == 'xn':
            fixture = plot.Fixture(plot_file)
            try:
                fixture.new(inputs[1], fixtures_dir)
            except FileNotFoundError:
                print('Error: Couldn\'t find a fixture file with this name')
            else:
                fixture.add()
                fixture.save()

        elif inputs[0] == 'xc':
            src_fixture = interface.get(inputs[1])
            if len(src_fixture) > 1:
                print('Error: You can only clone one fixture!')
            else:
                new_fixture = plot.Fixture(plot_file, fixtures_dir)
                new_fixture.clone(src_fixture[0])
                new_fixture.add()
                new_fixture.save()

        elif inputs[0] == 'xl':
            fixtures = plot.FixtureList(plot_file)
            i = 1
            interface.clear()
            for fixture in fixtures.fixtures:
                fixture_type = fixture.data['type']
                print('\033[4m'+str(i)+'\033[0m '+fixture_type+', id: '+
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
                    try:
                        test_value = fixture.data[key]
                    except KeyError:
                        pass
                    else:
                        if test_value == value:
                            fix_type = fixture.data['type']
                            print('\033[4m'+str(i)+'\033[0m '+fix_type+
                                ', id: '+fixture.uuid+', '+key+': '+value)
                            interface.append(i, fixture)
                            i = i+1
                        
            except IndexError:
                print('Error: You need to specify a key and value!')

        elif inputs[0] == 'xr':
            fixture_list = plot.FixtureList(plot_file)
            fixtures = interface.get(inputs[1])
            for fixture in fixtures:
                fixture_list.remove(fixture)

        elif inputs[0] == 'xg':
            fixtures = interface.get(inputs[1])
            for fixture in fixtures:
                try:
                    print(fixture.data[inputs[2]])
                except KeyError:
                    print('Error: This fixture has no data with that name')
            interface.update_this(inputs[1])

        elif inputs[0] == 'xG':
            fixtures = interface.get(inputs[1])
            for fixture in fixtures:
                for data_item in fixture.data:
                    print(data_item+': '+str(fixture.data[data_item]))
            interface.update_this(inputs[1])

        elif inputs[0] == 'xs':
            fixtures = interface.get(inputs[1])
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
                # Otherwise just set it
                else:
                    fixture.data[tag] = value
                fixture.save()
            interface.update_this(inputs[1])

        elif inputs[0] == 'xA':
            fixtures = interface.get(inputs[1])
            if len(fixtures) > 1 and inputs[3] != 'auto':
                print('Error: You must specify auto if you address more than '
                    'one fixture.')
            else:
                registry = plot.DmxRegistry(plot_file, inputs[2])
                for fixture in fixtures:
                    registry.address(fixture, inputs[3])
            interface.update_this(inputs[1])

        elif inputs[0] == 'xp':
            fixtures = interface.get(inputs[1])
            for fixture in fixtures:
                registry = plot.DmxRegistry(plot_file, fixture.data['universe'])
                registry.unaddress(fixture)
                fixture_list = plot.FixtureList(plot_file)
                fixture_list.remove(fixture)

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
            extensions_dir = '/usr/share/pylux/extension/'
            module_name = inputs[0].split(':')[1]
            try:
                runpy.run_path(extensions_dir+module_name+'.py',
                    init_globals={'plot_file': plot_file}, run_name='pyext')
            except FileNotFoundError:
                print('No extension with this name!')

        # Utility actions
        elif inputs[0] == 'h':
            text = ""
            with open('help.txt') as man:
                for line in man:
                    text = text+line
            print(text)

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
