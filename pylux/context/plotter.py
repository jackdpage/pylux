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

from context.context import Context, Command
import clihelper
import os.path
import logging
import math
import xml.etree.ElementTree as ET
from tqdm import tqdm
import reference
from lib import data, tagger
import document

class LightingPlot():

    def __init__(self, plot_file, options):
        self.fixtures = document.get_by_type(plot_file, 'fixture')
        self.fixtures = self.get_hung_fixtures()
        self.meta = document.get_by_type(plot_file, 'metadata')
        self.options = options

    def get_hung_fixtures(self):
        """Return a list of the fixtures that are used.

        Trim the fixtures list so that it only contains fixtures 
        which are hung in the plot. In other words, remove fixtures 
        which don\'t have position or focus attributes.

        Returns:
            A list of fixture objects which are used in the plot.
        """
        hung_fixtures = []
        for fixture in self.fixtures:
            if 'posX' and 'posY' in fixture:
                hung_fixtures.append(fixture)
        return hung_fixtures

    def get_page_dimensions(self):
        """Return the physical size of the paper. 

        Search in the reference module for the paper size in mm then 
        determine coordinate order based on orientation.

        Returns:
            A tuple in the form (X, Y) of the dimensions of the paper.
        """
        paper_type = self.options['paper-size']
        orientation = self.options['orientation']
        dimensions = reference.paper_sizes[paper_type]
        if orientation == 'portrait':
            return dimensions
        elif orientation == 'landscape':
            return (dimensions[1], dimensions[0])

    def get_margin_bounds(self):
        # This could be a function to get margin coordinates to make
        # placement easier, but it isn't
        return None

    def get_plot_size(self):
        """Return the physical size of the plot area.

        From the fixtures\' locations and focus points, find the 
        greatest and least values of X and Y then calculate the 
        dimensions that the plot covers.

        Returns:
            A tuple in the form (X, Y) of the dimensions of the plot.
        """
        x_values = []
        y_values = []
        for fixture in self.fixtures:
            get_mm = lambda field: float(field)*1000
            x_values.append(get_mm(fixture['posX']))
            x_values.append(get_mm(fixture['focusX']))
            y_values.append(get_mm(fixture['posY']))
            y_values.append(get_mm(fixture['focusY']))
        x_range = max(x_values) - min(x_values)
        y_range = max(y_values) - min(y_values)
        return (x_range, y_range)

    def can_fit_page(self):
        """Test if the plot can fit on the page.

        Uses the size of the page and scaling to determine whether 
        the page is large enough to fit the plot.
        """
        actual_size = self.get_plot_size()
        scaling = float(self.options['scale'])
        get_scaled = lambda dim: dim/scaling
        scaled_size = (get_scaled(actual_size[0]), get_scaled(actual_size[1]))
        paper_size = self.get_page_dimensions()
        remove_margin = lambda dim: dim-2*float(self.options['margin'])
        draw_area = (remove_margin(paper_size[0]), remove_margin(paper_size[1]))
        if draw_area[0] < scaled_size[0] or draw_area[1] < scaled_size[1]:
            return False
        else:
            return True

    def get_empty_plot(self):
        """Get an ElementTree tree with no content.

        Make a new ElementTree with a root svg element, set the 
        properties of the svg element to match paper size.
        """
        page_dims = self.get_page_dimensions()
        svg_root = ET.Element('svg')
        svg_root.set('width', str(page_dims[0])+'mm')
        svg_root.set('height', str(page_dims[1])+'mm')
        svg_root.set('xmlns', 'http://www.w3.org/2000/svg')
        svg_root.set('viewBox', '0 0 '+str(page_dims[0])+' '+str(page_dims[1]))
        svg_tree = ET.ElementTree(element=svg_root)
        return svg_tree

    def get_page_border(self):
        """Get the page border ready to be put into the plot.

        Returns a path element that borders the plot on all four 
        sides.

        Returns:
            An ElementTree element - an SVG path.
        """
        margin = float(self.options['margin'])
        weight = float(self.options['line-weight-heavy'])
        paper = self.get_page_dimensions()
        border = ET.Element('path')
        border.set('d', 'M '+str(margin)+' '+str(margin)+' '
                   'L '+str(paper[0]-margin)+' '+str(margin)+' '
                   'L '+str(paper[0]-margin)+' '+str(paper[1]-margin)+' '
                   'L '+str(margin)+' '+str(paper[1]-margin)+' '
                   'L '+str(margin)+' '+str(margin))
        border.set('fill', 'white')
        border.set('stroke', 'black')
        border.set('stroke-width', str(weight))
        return border

    def get_centre_line(self):
        """Get the centre line to insert.

        Returns a path element that represents the centre line, 
        containing the recommended dash appearance.

        Returns:
            An ElementTree element - an SVG path.
        """
        centre = self.get_page_dimensions()[0]/2
        height = self.get_page_dimensions()[1]
        margin = float(self.options['margin'])
        centre_line = ET.Element('path')
        if self.options['centre-line-extend'] == 'True':
            centre_line.set('d', 'M '+str(centre)+' 0 '
                                 'L '+str(centre)+' '+str(height))
        else:
            centre_line.set('d', 'M '+str(centre)+' '+str(margin)+' '
                                 'L '+str(centre)+' '+str(height-margin))
        centre_line.set('stroke', 'black')
        centre_line.set('stroke-width', 
                        str(self.options['line-weight-medium']))
        centre_line.set('stroke-dasharray', 
                        self.options['centre-line-dasharray'])
        return centre_line

    def get_plaster_line(self):
        """Get the plaster line to insert.

        Returns a path element that represents the plaster line.

        Returns:
            An ElementTree element - an SVG path.
        """
        scale = float(self.options['scale'])
        padding = float(self.options['plaster-line-padding'])*1000/scale
        margin = float(self.options['margin'])
        width = self.get_page_dimensions()[0]
        plaster_line = ET.Element('path')
        if self.options['plaster-line-extend'] == 'True':
            plaster_line.set('d', 'M 0 '+str(margin+padding)+' '
                                  'L '+str(width)+' '+str(margin+padding))
        else:
            plaster_line.set('d', 'M '+str(margin)+' '+str(margin+padding)+' ' 
                                  'L '+str(width-margin)+' '+
                                  str(margin+padding))
        plaster_line.set('stroke', 'black')
        plaster_line.set('stroke-width', 
                         str(self.options['line-weight-medium']))
        plaster_line.set('stroke-dasharray',
                         self.options['plaster-line-dasharray'])
        return plaster_line 

    def get_plaster_coord(self):
        """Get the plaster line y coordinate.

        Returns the plaster line y coordinate to allow offsets to 
        be calculated when plotting fixtures.

        Returns:
            A float representing the y coordinate in mm.
        """
        scale = float(self.options['scale'])
        margin = float(self.options['margin'])
        padding = float(self.options['plaster-line-padding'])*1000/scale
        return margin+padding

    def get_background_image(self):
        """Get the background image from file.

        Returns:
            The first group element of the SVG image file.
        """
        scale = float(self.options['scale'])
        svg_ns = {'ns0': 'http://www.w3.org/2000/svg'}
        xloc = self.get_page_dimensions()[0]/2
        yloc = self.get_plaster_coord()
        image_file = os.path.expanduser(self.options['background-image'])
        image_tree = ET.parse(image_file)
        image_root = image_tree.getroot()
        image_group = image_root.find('ns0:g', svg_ns)
        image_group.set('transform', 'scale('+str(1/scale)+') '
                                     'translate('+str(xloc*scale)+' '+
                                     str(yloc*scale)+')')
        for path in image_group:
            path_class = path.get('class')
            if path.get('class') in reference.usitt_line_weights:
                weight = reference.usitt_line_weights[path_class]
            else:
                weight = 'line-weight-medium'
            path.set('stroke-width', 
                     str(float(self.options[weight])*scale))
            
        return image_group

    def get_title_block(self):
        if self.options['title-block'] == 'corner':
            return self.get_title_corner()
        elif self.options['title-block'] == 'sidebar':
            return self.get_title_sidebar()
        elif self.options['title-block'] == None:
            return None

    def get_title_corner(self):
        """Get the title block ready to be put into the plot."""
        return None

    def get_title_sidebar(self):
        """Get the title block in vertical form."""
        
        def get_sidebar_width(self):
            page_dims = self.get_page_dimensions()
            pc_width = page_dims[0]*float(self.options['vertical-title-width-pc'])
            if pc_width > float(self.options['vertical-title-max-width']):
                return float(self.options['vertical-title-max-width'])
            elif pc_width < float(self.options['vertical-title-min-width']):
                return float(self.options['vertical-title-min-width'])
            else:
                return pc_width

        # Create sidebar group
        sidebar = ET.Element('g')
        # Create sidebar border
        sidebar_width = get_sidebar_width(self)
        page_dims = self.get_page_dimensions()
        margin = float(self.options['margin'])
        left_border = page_dims[0]-margin-sidebar_width
        sidebar_box = ET.SubElement(sidebar, 'path')
        sidebar_box.set('d', 'M '+str(left_border)+' '+str(margin)+
                          ' L '+str(left_border)+' '+str(page_dims[1]-margin))
        sidebar_box.set('stroke', 'black')
        sidebar_box.set('stroke-width', str(self.options['line-weight-heavy']))
        # Create title text within HTML foreignObject element (to support text wrapping)
        html_cont = ET.SubElement(sidebar, 'foreignObject')
        html_cont.set('width', str(get_sidebar_width(self)))
        html_cont.set('height', str(page_dims[1]-2*margin))
        html_cont.set('x', str(left_border))
        html_cont.set('y', str(margin))
        text_title = ET.SubElement(html_cont, 'p')
        text_title.text = document.get_by_value(self.meta, 'metadata-key', 'Production')[0]['metadata-value']
        text_title.set('xmlns', 'http://www.w3.org/1999/xhtml')

        def generate_title_text_style(self):
            style = []
            style.append(('text-transform','uppercase'))
            style.append(('font-size', str(self.options['font-size-title'])+'pt'))

            style_str = ''
            for i in style:
                style_str += i[0]+':'+i[1]+';'

            return style_str

        text_title.set('style', generate_title_text_style(self))
        return sidebar

    def get_fixture_icon(self, fixture):
        """Return an SVG group for a single fixture.

        Search the package data for a symbol for this fixture, then 
        transform as appropriate based on tags and plot scaling.

        Args:
            fixture: the fixture object to create an icon for.

        Returns:
            An ElementTree object representing an SVG 'g' element.
        """
        # Get the base SVG element
        symbol_name = fixture['symbol']
        tree = ET.parse(data.get_data('symbol/'+symbol_name+'.svg'))
        root = tree.getroot()
        svg_ns = {'ns0': 'http://www.w3.org/2000/svg'}
        symbol = root.find('ns0:g', svg_ns)
        # Transform based on scaling and data
        centre = self.get_page_dimensions()[0]/2
        plaster = self.get_plaster_coord()
        scale = float(self.options['scale'])
        plot_pos = lambda dim: (float(fixture['pos'+dim])*1000)
        rotation = fixture['rotation']
        colour = fixture['colour']
        symbol.set('transform', 'scale( '+str(1/scale)+' ) '
                   'translate('+str(centre*scale+plot_pos('X'))+' '+
                   str(plot_pos('Y')+plaster*scale)+') '
                   'rotate('+str(rotation)+')')
        for path in symbol:
            if path.get('class') == 'outer':
                path.set('fill', colour)
                path.set('stroke-width', 
                         str(float(self.options['line-weight-heavy'])*scale))
        return symbol

    def get_fixture_beam(self, fixture):
        if self.options['beam-source-colour'] == 'True':
            colour = self.get_fixture_colour(fixture)
        else:
            colour = 'black'
        beam = ET.Element('path')
        scale = float(self.options['scale'])
        centre = self.get_page_dimensions()[0]/2
        plaster = self.get_plaster_coord()
        startx = (float(fixture['posX'])*1000)*(1/scale)+centre
        starty = (float(fixture['posY'])*1000)*(1/scale)+plaster
        endx = (float(fixture['focusX'])*1000)*(1/scale)+centre
        endy = (float(fixture['focusY'])*1000)*(1/scale)+plaster
        beam.set('d', 'M '+str(startx)+' '+str(starty)+
                      ' L '+str(endx)+' '+str(endy))
        beam.set('stroke', colour)
        beam.set('stroke-width', self.options['line-weight-light'])
        beam.set('stroke-dasharray', self.options['beam-dasharray'])
        return beam

    def get_fixture_focus_point(self, fixture):
        if self.options['focus-point-source-colour'] == 'True':
            colour = self.get_fixture_colour(fixture)
        else:
            colour = 'black'
        point = ET.Element('circle')
        scale = float(self.options['scale'])
        centre = self.get_page_dimensions()[0]/2
        plaster = self.get_plaster_coord()
        posx = float(fixture['focusX'])*1000*(1/scale)+centre
        posy = float(fixture['focusY'])*1000*(1/scale)+plaster
        point.set('cx', str(posx))
        point.set('cy', str(posy))
        point.set('r', str(self.options['focus-point-radius']))
        point.set('fill', colour)

        return point

    def generate_plot(self):
        if not self.can_fit_page():
            print('PlotterError: Plot does not fit page with this scaling')
        else:
            self.lighting_plot = self.get_empty_plot()
            root = self.lighting_plot.getroot()
            root.append(self.get_page_border())
            try:
                root.append(self.get_background_image())
            except FileNotFoundError:
                print('Yeah it kind of didn\'t work. Just going to ignore this')
            root.append(self.get_centre_line())
            print('Plotted centre line')
            root.append(self.get_plaster_line())
            print('Plotted plaster line')
            for fixture in tqdm(self.fixtures, desc='Plotting fixtures: '):
                tagger.tag_fixture_all(fixture)
                if self.options['show-beams'] == 'True':
                    root.append(self.get_fixture_beam(fixture))
                if self.options['show-focus-point'] == 'True':
                    root.append(self.get_fixture_focus_point(fixture))
                root.append(self.get_fixture_icon(fixture))
            if self.options['title-block'] != 'None':
                root.append(self.get_title_block())
            print('Added title block')


class PlotOptions():

    def __init__(self, config):
        
        self.options = config['plotter']

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
        super().__init__()
        self.name = 'plotter'
        self.register(Command('pn', self.plot_new, []))
        self.register(Command('pw', self.plot_write, [
            ('path', True, 'The location to save the plot to.')]))
        self.register(Command('pd', self.plot_dump, []))
        self.register(Command('os', self.option_set, [
            ('name', True, 'The name of the option to set the value of.'), 
            ('value', True, 'The new value of the option.')]))
        self.register(Command('og', self.option_get, [
            ('name', True, 'The name of the option to print the value of.')]))
        self.register(Command('ol', self.option_list, []))

    def post_init(self):
        super().post_init()
        self.options = PlotOptions(self.config)

    def plot_new(self, parsed_input):
        '''Create a new SVG plot in a temporary buffer.'''
        self.plot = LightingPlot(self.plot_file, self.options.options)
        self.plot.generate_plot()

    def plot_write(self, parsed_input):
        '''Write the plot to a file either as SVG or PDF.'''
        if parsed_input[0].split('.')[-1] == 'svg':
            self.plot.lighting_plot.write(os.path.expanduser(parsed_input[0]))
        elif parsed_input[0].split('.')[-1] == 'pdf':
            plot_bytes = ET.tostring(self.plot.lighting_plot.getroot())
#            cairosvg.svg2pdf(bytestring=plot_bytes, write_to=parsed_input[0])
        else:
            print('WARNING: File format not supported, writing as SVG')
            self.plot.lighting_plot.write(os.path.expanduser(parsed_input[0]))

    def plot_dump(self, parsed_input):
        '''Dump the plot (for debugging purposes.'''
        ET.dump(self.plot.lighting_plot.getroot())

    def option_set(self, parsed_input):
        '''Set the value of an option.'''
        self.options.set(parsed_input[0], parsed_input[1])

    def option_get(self, parsed_input):
        '''Print the value of an option.'''
        print(self.options.get(parsed_input[0]))

    def option_list(self, parsed_input):
        '''List the values of all options.'''
        for option in self.options.options:
            print(option+': '+str(self.options.options[option]))

def get_context():
    return PlotterContext()
