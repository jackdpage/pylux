# plotgen.py is part of Pylux
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

import plot
import os
import math
import xml.etree.ElementTree as ET
import clihelper
import reference


class ImagePlot:

    def __init__(self, options):    
        self.fixtures = plot.FixtureList(plot_file)
        self.image_plot = ET.Element('svg')
        self.options = options

    def add_fixtures(self):
        for fixture in self.fixtures.fixtures:
            symbol_name = fixture.data['symbol']
            posX = fixture.data['posX']
            posY = fixture.data['posY']
            rotation = fixture.data['rotation']
            colour = fixture.data['colour']
            symbol = plot.FixtureSymbol('/usr/share/pylux/symbol/'+
                symbol_name+'.svg')
            symbol.prepare(posX, posY, rotation, colour)
            self.image_plot.append(symbol.image_group)

    def add_beams(self):
        beam_group = ET.SubElement(self.image_plot, 'g')
        beam_group.set('class', 'beam-group')
        for fixture in self.fixtures.fixtures:
            posX = str(float(fixture.data['posX'])*1000)
            posY = str(float(fixture.data['posY'])*1000)
            focusX = str(float(fixture.data['focusX'])*1000)
            focusY = str(float(fixture.data['focusY'])*1000)
            beam = ET.SubElement(beam_group, 'path')
            beam.set('d', 'M '+posX+' '+posY+' L '+focusX+' '+focusY)
            if self.options['beam_colour'] == 'auto':
                beam.set('stroke', fixture.data['colour'])
            else:
                beam.set('stroke', 
                    reference.gel_colours[self.options['beam_colour']])
            beam.set('stroke-dasharray', '10,10')
            beam.set('stroke-width', self.options['beam_width'])
            

def default_options():
    options = {
        'beam_colour': 'Black',
        'beam_width': '6',
        'show_beams': 'true'}
    return options

def run_pylux_extension():
    options = default_options()
    while True:
        user_input = input('(pylux:plotter) ')
        inputs = user_input.split(' ')

        if inputs[0] == 'os':
            options[inputs[1]] = clihelper.resolve_input(inputs, 2)[-1]

        elif inputs[0] == 'og':
            print(inputs[1]+': '+options[inputs[1]])

        elif inputs[0] == 'oG':
            for option in options:
                print(option+': '+options[option])

        elif inputs[0] == 'pn':
            image_plot = ImagePlot(options)
            if options['show_beams'] == 'true':
                image_plot.add_beams()
            image_plot.add_fixtures()
            output_tree = ET.ElementTree(image_plot.image_plot)
            output_tree.write(os.path.expanduser(inputs[1]))

        elif inputs[0] == '::':
            break

        else:
            print('That command doesn\'t exist!')

if __name__ == 'pyext':
    run_pylux_extension()
