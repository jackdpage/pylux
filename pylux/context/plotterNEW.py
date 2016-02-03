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
import math
import xml.etree.ElementTree as ET
import pylux.plot as plot
import pylux.clihelper as clihelper
import pylux.reference as reference
from pylux import get_data


class LightingPlot():

    def __init__(self, plot_file, options):
        self.fixtures = plot.FixtureList(plot_file).fixtures
        self.options = options

    def get_page_dimensions(self):
        paper_type = self.options['paper_size']
        orientation = self.options['orientation']
        dimensions = reference.paper_sizes[paper_type]
        if orientation == 'portrait':
            return dimensions
        elif orientation == 'landscape':
            return (dimensions[1], dimensions[0])

    def get_plot_size(self):
        """Return the physical size of the plot area.

        From the fixtures' locations and focus points, find the 
        greatest and least values of X and Y then calculate the 
        dimensions that the plot covers.

        Returns:
            A tuple in the form (X, Y) of the dimensions of the plot.
        """
        x_values = []
        y_values = []
        for fixture in self.fixtures:
            get_mm = lambda field: float(field)*1000
            x_values.append(get_mm(fixture.data['posX']))
            x_values.append(get_mm(fixture.data['focusX']))
            y_values.append(get_mm(fixture.data['posY']))
            y_values.append(get_mm(fixture.data['focusY']))
        min_x = min(x_values)
        min_y = min(y_values)
        return (min_x, min_y)

    def can_fit_page(self):
        """Test if the plot can fit on the page.

        Uses the size of the page and scaling to determine whether 
        the page is large enough to fit the plot.
        """
        actual_size = self.get_plot_size()
        scaling = self.options['scale']
        get_scaled = lambda dim: dim/scaling
        scaled_size = (get_scaled(actual_size[0]), get_scaled(actual_size[1]))
        paper_size = self.get_page_dimensions()
        remove_margin = lambda dim: dim-2*self.options['margin']
        draw_area = (remove_margin(paper_size[0]), remove_margin(paper_size[1]))
        if draw_area[0] < scaled_size[0] or draw_area[1] < scaled_size[1]:
            return False
        else:
            return True

    def get_page_border(self):
        """Get the page border ready to be put into the plot.

        Returns a path element that borders the plot on all four 
        sides.

        Returns:
            An ElementTree element - an SVG path.
        """
        marign = self.options['margin_width']
        weight = self.options['line_weight_heavy']
        paper = reference.paper_sizes[self.options['paper_size']]
        border = ET.Element('path')
        border.set('d', 'M '+str(margin)+' -'+str(margin)+' '
                   'L '+str(paper[0]-margin)+' -'+str(margin)+' '
                   'L '+str(paper[0]-margin)+' -'+str(paper[1]-margin)+' '
                   'L '+str(margin)+' -'+str(paper[1]-margin)+' '
                   'L '+str(margin)+' -'+str(margin))
        return border

    def get_title_block(self):
        if self.options['title_block'] == 'corner':
            return self.get_title_corner()
        elif self.options['title_block'] == 'sidebar':
            return self.get_title_sidebar()
        elif self.options['title_block'] == None:
            return None

    def get_title_corner(self):
        """Get the title block ready to be put into the plot."""

    def get_title_sidebar(self):
        """Get the title block in vertical form."""

class PlotOptions():

    DEFAULTS = {
        # [A[0-4]]
        'paper_size' : 'A4',
        # ['landscape', 'portrait']
        'orientation' : 'landscape',
        # int
        'scale' : 50,
        # int
        'margin' : 20,
        # int
        'line_weight_heavy' : 6,
        # ['corner', 'sidebar', None]
        'title_block' : 'corner'}
    
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
        self.name = 'plotter-dev'
        self.init_commands()
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
        self.lighting_plot = LightingPlot(self.plot_file, self.options.DEFAULTS)

    def plot_write(self, parsed_input):
        output_tree = ET.ElementTree(self.image_plot.image_plot)
        output_tree.write(os.path.expanduser(parsed_input[0]))

    def option_set(self, parsed_input):
        self.options.set(parsed_input[0], parsed_input[1])

    def option_get(self, parsed_input):
        print(self.options.get(parsed_input[0]))

    def option_list(self, parsed_input):
        for option in self.options.DEFAULTS:
            print(option+': '+str(self.options.DEFAULTS[option]))

def get_context():
    return PlotterContext()
