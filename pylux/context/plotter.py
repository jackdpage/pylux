# plotter.py is part of Pylux
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

"""Generate SVG lighting plots.

Context that provides commands to create lighting plot images in 
SVG format.
"""

from pylux.context.context import Context
import os.path
import logging
from tqdm import tqdm
import base64
import xml.etree.ElementTree as ET
import pylux.plot as plot
import pylux.clihelper as clihelper
import pylux.reference as reference
from pylux import get_data

class ImagePlot:

    def __init__(self, plot_file, options):    
        self.fixtures = plot.FixtureList(plot_file)
        self.image_plot = ET.Element('svg')
        self.options = options

    def verify_fixture(self, fixture):
        errors = []
        if 'posX' not in fixture.data or 'posY' not in fixture.data:
            errors.append('No position')
        if 'focusX' not in fixture.data or 'focusY' not in fixture.data:
            errors.append('No focus')
        if 'gel' not in fixture.data:
            errors.append('No gel')
        if 'symbol' not in fixture.data:
            errors.append('No symbol')
        elif fixture.data['symbol'] == 'PHANTOM':
            errors.append('Phantom fixture')
        if len(errors) == 0:
            return True
        else:
            return errors

    def add_fixtures(self):
        for fixture in tqdm(self.fixtures.fixtures):
            if self.verify_fixture(fixture) == True:
                fixture.data['rotation'] = fixture.generate_rotation()
                if not fixture.generate_colour():
                    fixture.data['colour'] = '#000000'
                else:
                    fixture.data['colour'] = fixture.generate_colour()
                symbol_name = fixture.data['symbol']
                posX = fixture.data['posX']
                posY = fixture.data['posY']
                rotation = fixture.data['rotation']
                colour = fixture.data['colour']
                symbol = plot.FixtureSymbol(get_data('symbol/'+symbol_name+'.svg'))
                symbol.prepare(posX, posY, rotation, colour)
                self.image_plot.append(symbol.image_group)
            else:
                pass

    def add_beams(self):
        beam_group = ET.SubElement(self.image_plot, 'g')
        beam_group.set('class', 'beam-group')
        for fixture in self.fixtures.fixtures:
            if self.verify_fixture(fixture) == True:
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

    def add_background(self):
        """Set the background image.

        Read the bytes from the file given in the background 
        image option, encode in base64 then add as an image 
        element.
        """
        with open(self.options['background_image'], 'rb') as bgfile:
            background_bytes = bgfile.read()
        background_image = ET.SubElement(self.image_plot, 'image')
        background_image.set('href', 'data:image/png;base64,'+
                             str(base64.b64encode(background_bytes)))
        background_image.set('width', self.options['xrange'])
        background_image.set('height', self.options['yrange'])
            

class PlotOptions():

    def __init__(self):
        self.options = {
            'beam_colour': 'Black',
            'beam_width': '6',
            'show_beams': 'True',
            'background_image': 'None',
            'xrange': '0',
            'yrange': '0'}

    def set(self, option, value):
        self.options[option] = value

    def get(self, option):
        if option in self.options:
            return self.options[option]
        else:
            return None

class PlotterContext(Context):

    def __init__(self):
        self.name = 'plotter'
        self.init_commands()
        self.register('pn', self.plot_new, 0)
        self.register('pw', self.plot_write, 1)
        self.register('os', self.option_set, 2)
        self.register('og', self.option_get, 1)
        self.register('ol', self.option_list, 0)
        self.init_plot()

    def init_plot(self):
        self.options = PlotOptions()

    def plot_new(self, parsed_input):
        self.image_plot = ImagePlot(self.plot_file, self.options.options)
        if self.options.options['background_image'] != 'None':
            self.image_plot.add_background()
        if self.options.options['show_beams'] == 'True':
            self.image_plot.add_beams()
        self.image_plot.add_fixtures()

    def plot_write(self, parsed_input):
        output_tree = ET.ElementTree(self.image_plot.image_plot)
        output_tree.write(os.path.expanduser(parsed_input[0]))

    def option_set(self, parsed_input):
        self.options.set(parsed_input[0], parsed_input[1])

    def option_get(self, parsed_input):
        print(self.options.get(parsed_input[0]))

    def option_list(self, parsed_input):
        for option in self.options.options:
            print(option+': '+self.options.options[option])

def get_context():
    return PlotterContext()
