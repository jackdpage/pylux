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

from pylux.context.context import Context, Command
import os.path
import logging
from tqdm import tqdm
import base64
import math
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
                fixture_group = ET.SubElement(self.image_plot, 'g')
                fixture.data['rotation'] = fixture.generate_rotation()
                if not fixture.generate_colour():
                    fixture.data['colour'] = '#000000'
                else:
                    fixture.data['colour'] = fixture.generate_colour()
                symbol_instance = FixtureSymbol(fixture)
                fixture_symbol = symbol_instance.get_fixture_group()
                fixture_beam = symbol_instance.get_fixture_beam()
#                fixture_circuit = symbol_instance.get_circuit_icon()
#                fixture_group.append(fixture_circuit)
                fixture_group.append(fixture_beam)
                fixture_group.append(fixture_symbol)
            else:
                pass

    def add_background(self):
        """Set the background image.

        Literally just imports the first group from the background 
        image file.
        """
        tree = ET.parse(self.options['background_image'])
        root = tree.getroot()
        ns = {'ns0': 'http://www.w3.org/2000/svg'}
        image_group = root.find('ns0:g', ns)
        self.image_plot.append(image_group)


class PlotOptions():

    def __init__(self):
        self.options = {
            'beam_colour': 'Black',
            'beam_width': '6',
            'show_beams': 'True',
            'background_image': 'None',
            'show_circuits': 'True'}

    def set(self, option, value):
        self.options[option] = value

    def get(self, option):
        if option in self.options:
            return self.options[option]
        else:
            return None


class FixtureSymbol:
    """Manages the SVG symbols for fixtures."""

    def __init__(self, fixture):
        """Load the fixture symbol file."""
        self.fixture = fixture
        symbol_name = fixture.data['symbol']
        tree = ET.parse(get_data('symbol/'+symbol_name+'.svg'))
        root = tree.getroot()
        self.ns = {'ns0': 'http://www.w3.org/2000/svg'}
        self.image_group = root.find('ns0:g', self.ns)

    def get_fixture_group(self):
        """Return a transformed symbol g element."""
        posX_mm = float(self.fixture.data['posX'])*1000
        posY_mm = float(self.fixture.data['posY'])*1000
        rotation_deg = self.fixture.data['rotation']
        colour = self.fixture.data['colour']
        self.image_group.set('transform', 'translate('+
            str(posX_mm)+' '+str(posY_mm)+') rotate('+str(rotation_deg)+')')
        for path in self.image_group:
            if path.get('class') == 'outer':
                path.set('fill', colour)
        return self.image_group

    def get_fixture_beam(self):
        """Return a beam path element."""
        posX_mm = str(float(self.fixture.data['posX'])*1000)
        posY_mm = str(float(self.fixture.data['posY'])*1000)
        focusX_mm = str(float(self.fixture.data['focusX'])*1000)
        focusY_mm = str(float(self.fixture.data['focusY'])*1000)
        beam = ET.Element('path')
        beam.set('d', 'M '+posX_mm+' '+posY_mm+' L '+focusX_mm+' '+focusY_mm)
        beam.set('stroke', 'black')
        beam.set('stroke-width', '6')
        beam.set('stroke-dasharray', '10,10')
        return beam

    def get_circuit_icon(self):
        """Return a circuit and connector g element."""
        rotation_deg = self.fixture.data['rotation']
        posX_mm = float(self.fixture.data['posX'])*1000
        posY_mm = float(self.fixture.data['posY'])*1000
        connector_endX = posX_mm-200*math.cos(math.radians(rotation_deg))
        connector_endY = posY_mm-200*math.sin(math.radians(rotation_deg))
        icon_group = ET.Element('g')
        connector = ET.SubElement(icon_group, 'path')
        connector.set('d', 'M '+str(posX_mm)+' '+str(posY_mm)+
                      ' L '+str(connector_endX)+' '+str(connector_endY))
        connector.set('stroke', 'black')
        connector.set('stroke-width', '3')
        circle = ET.SubElement(icon_group, 'circle')
        circle.set('cx', str(connector_endX))
        circle.set('cy', str(connector_endY))
        circle.set('r', '60')
        circle.set('stroke', 'black')
        circle.set('stroke-width', '6')
        circle.set('fill', 'white')
        text = ET.SubElement(icon_group, 'text')
        text.text = self.fixture.data['circuit']
        text.set('x', str(connector_endX))
        text.set('y', str(connector_endY))
        text.set('font-size', '60')
        return icon_group


class PlotterContext(Context):

    def __init__(self):
        print('[NOTICE] THIS IS A TEMPORARY IMPLEMENTATION OF PLOTTER WHILST '
              'A MORE FULLY FEATURED VERSION IS CREATED. You can access the '
              'development version of plotter in the plotterNEW module.')
        self.name = 'plotter'
        super().__init__()
        self.register(Command('pn', self.plot_new, [], 
                              synopsis='Create a new plot.'))
        self.register(Command('pw', self.plot_write, ['path'], 
                              synopsis='Write the plot buffer to a file.'))
        self.register(Command('os', self.option_set, ['name', 'value'], 
                              synopsis='Set the value of an option.'))
        self.register(Command('og', self.option_get, ['name'], 
                              synopsis='Print the value of an option.'))
        self.register(Command('ol', self.option_list, [],
                              synopsis='Print the value of all options.'))
        self.init_plot()

    def init_plot(self):
        self.options = PlotOptions()

    def plot_new(self, parsed_input):
        self.image_plot = ImagePlot(self.plot_file, self.options.options)
        if self.options.options['background_image'] != 'None':
            self.image_plot.add_background()
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
