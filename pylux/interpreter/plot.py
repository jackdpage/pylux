from pylux.interpreter import InterpreterExtension, NoRefsCommand
from pylux import document, reference
from pylux.lib import data, tagger, polygon
import xml.etree.ElementTree as ET
import os
import math
from ast import literal_eval


class LightingPlot:

    def __init__(self, plot, options):
        self.fixtures = document.get_by_type(plot, 'fixture')
        self.fixtures = self.get_hung_fixtures()
        self.meta = document.get_by_type(plot, 'metadata')
        self.options = options
        self.plot_file = plot

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
            if 'posX' in fixture and 'posY' in fixture:
                hung_fixtures.append(fixture)
        return hung_fixtures

    def get_hung_types(self):
        """Return a list of fixture types used and their corresponding symbol
        tags. Will assume that all fixture types have the same symbol tag so tough
        luck if they don't."""
        fixture_types = {}
        hung = self.get_hung_fixtures()
        for f in hung:
            if f['fixture-type'] not in fixture_types:
                if 'symbol' in f:
                    fixture_types[f['fixture-type']] = f['symbol']
                else:
                    fixture_types[f['fixture-type']] = self.options['fallback-symbol']
        return fixture_types

    def get_plotted_fixtures(self):
        """Return a list of fixtures which are hung and also fit in the plot area."""
        return [i for i in self.get_hung_fixtures() if self.fixture_will_fit(i)]

    def get_plotted_types(self):
        """Return a list of fixture types used which actually managed to fit. Also
        provide symbol tags. As with get_hung_types, will assume the first fixture
        with a symbol tag it finds is the correct one for all of that type."""
        fixture_types = {}
        plotted = self.get_plotted_fixtures()
        for f in plotted:
            if f['fixture-type'] not in fixture_types:
                if 'symbol' in f:
                    fixture_types[f['fixture-type']] = f['symbol']
                else:
                    fixture_types[f['fixture-type']] = self.options['fallback-symbol']
        return fixture_types

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
        x_values = [0]
        y_values = [0]
        for fixture in self.get_hung_fixtures():
            get_mm = lambda field: float(field) * 1000
            x_values.append(get_mm(fixture['posX']))
            y_values.append(get_mm(fixture['posY']))
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
        get_scaled = lambda dim: dim / scaling
        scaled_size = (get_scaled(actual_size[0]), get_scaled(actual_size[1]))
        paper_size = self.get_page_dimensions()
        remove_margin = lambda dim: dim - 2 * float(self.options['margin'])
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
        svg_root.set('width', str(page_dims[0]) + 'mm')
        svg_root.set('height', str(page_dims[1]) + 'mm')
        svg_root.set('xmlns', 'http://www.w3.org/2000/svg')
        svg_root.set('viewBox', '0 0 ' + str(page_dims[0]) + ' ' + str(page_dims[1]))
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
        border.set('d', 'M ' + str(margin) + ' ' + str(margin) + ' '
                                                                 'L ' + str(paper[0] - margin) + ' ' + str(margin) + ' '
                                                                                                                     'L ' + str(
            paper[0] - margin) + ' ' + str(paper[1] - margin) + ' '
                                                                'L ' + str(margin) + ' ' + str(paper[1] - margin) + ' '
                                                                                                                    'L ' + str(
            margin) + ' ' + str(margin))
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
        centre = self.get_centre_coord()
        height = self.get_page_dimensions()[1]
        margin = float(self.options['margin'])
        centre_line = ET.Element('path')
        if self.options.getboolean('centre-line-extend'):
            centre_line.set('d', 'M ' + str(centre) + ' 0 ' +
                            'L ' + str(centre) + ' ' + str(height))
        else:
            centre_line.set('d', 'M ' + str(centre) + ' ' + str(margin) + ' ' +
                            'L ' + str(centre) + ' ' + str(
                height - margin))
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
        centre = self.get_page_dimensions()[1] / 2
        padding = float(self.options['plaster-line-padding']) * 1000 / scale
        width = self.get_page_dimensions()[0]
        width_extent = self.get_plot_width_extent()
        plaster_line = ET.Element('path')
        if self.options.getboolean('plaster-line-extend'):
            plaster_line.set('d', 'M 0 ' + str(centre + padding) + ' ' +
                             'L ' + str(width) + ' ' + str(centre + padding))
        else:
            plaster_line.set('d', 'M ' + str(width_extent[0]) + ' ' + str(centre + padding) + ' ' +
                             'L ' + str(width_extent[1]) + ' ' +
                             str(centre + padding))
        plaster_line.set('stroke', 'black')
        plaster_line.set('stroke-width',
                         str(self.options['line-weight-medium']))
        plaster_line.set('stroke-dasharray',
                         self.options['plaster-line-dasharray'])
        return plaster_line

    def get_centre_coord(self):
        """Get the centre line x coordinate.

        Returns the centre line x coordinate once offsets have
        been taken into account.

        Returns:
            A float representing the coordinate in mm.
        """
        page_centre = self.get_page_dimensions()[0] / 2
        if self.options['title-block'] == 'sidebar':
            sidebar_offset = self.get_title_sidebar_width()
            return page_centre - sidebar_offset / 2
        else:
            return page_centre

    def get_plaster_coord(self):
        """Get the plaster line y coordinate.

        Returns the plaster line y coordinate to allow offsets to
        be calculated when plotting fixtures.

        Returns:
            A float representing the y coordinate in mm.
        """
        centre = self.get_page_dimensions()[1] / 2
        scale = float(self.options['scale'])
        padding = float(self.options['plaster-line-padding']) * 1000 / scale
        return centre + padding

    def get_plot_width_extent(self):
        """Get the min and max coordinates to stay within the plot width, taking
        into account margins and titles.
        Returns a tuple of floats representing the values in mm."""
        width = self.get_page_dimensions()[0]
        margin = float(self.options['margin'])
        min_x = margin
        if self.options['title-block'] == 'sidebar':
            sidebar_width = self.get_title_sidebar_width()
        else:
            sidebar_width = 0
        max_x = width - margin - sidebar_width

        return min_x, max_x

    def get_plot_height_extent(self):
        """Get the min and max coordinates to stay within the plot height"""
        height = self.get_page_dimensions()[1]
        margin = float(self.options['margin'])
        min_y = margin
        max_y = height - margin

        return min_y, max_y

    def get_physical_constraints(self):
        """Get the min and max real-life x and y values that represent the plot area, taking
        into account margins and titles.
        Returns a tuple of floats: min_x, max_x, min_y, max_y representing values in mm"""
        scale = float(self.options['scale'])
        margin = float(self.options['margin'])
        paper_extents = self.get_plot_width_extent()
        min_x = (self.get_centre_coord() - paper_extents[0]) * -1 * scale
        max_x = min_x * -1

        max_y = (self.get_plaster_coord() - margin) * scale
        min_y = (self.get_page_dimensions()[1] - 2 * margin - self.get_plaster_coord()) * scale * -1

        return min_x, max_x, min_y, max_y

    def get_background_image(self):
        """Get the background image from file.

        Returns:
            The first group element of the SVG image file.
        """
        scale = float(self.options['scale'])
        svg_ns = {'ns0': 'http://www.w3.org/2000/svg'}
        xloc = self.get_page_dimensions()[0] / 2
        yloc = self.get_plaster_coord()
        image_file = os.path.expanduser(self.options['background-image'])
        image_tree = ET.parse(image_file)
        image_root = image_tree.getroot()
        image_group = image_root.find('ns0:g', svg_ns)
        image_group.set('transform', 'scale(' + str(1 / scale) + ') '
                                                                 'translate(' + str(xloc * scale) + ' ' +
                        str(yloc * scale) + ')')
        for path in image_group:
            path_class = path.get('class')
            if path.get('class') in reference.usitt_line_weights:
                weight = reference.usitt_line_weights[path_class]
            else:
                weight = 'line-weight-medium'
            path.set('stroke-width',
                     str(float(self.options[weight]) * scale))
            path.set('stroke', '#000000')
            path.set('fill-opacity', '0')

        return image_group

    def get_title_block(self):
        return self.get_title_sidebar()

    def get_title_sidebar_width(self):
        page_dims = self.get_page_dimensions()
        pc_width = page_dims[0] * float(self.options['sidebar-title-width-pc'])
        if pc_width > float(self.options['sidebar-title-max-width']):
            return float(self.options['sidebar-title-max-width'])
        elif pc_width < float(self.options['sidebar-title-min-width']):
            return float(self.options['sidebar-title-min-width'])
        else:
            return pc_width

    def get_title_sidebar(self):
        """Get the title block in vertical form."""

        # Create sidebar group
        sidebar = ET.Element('g')
        # Create sidebar border
        sidebar_width = self.get_title_sidebar_width()
        page_dims = self.get_page_dimensions()
        margin = float(self.options['margin'])
        left_border = page_dims[0] - margin - sidebar_width
        sidebar_box = ET.SubElement(sidebar, 'path')
        sidebar_box.set('d', 'M ' + str(left_border) + ' ' + str(margin) +
                        ' L ' + str(left_border) + ' ' + str(page_dims[1] - margin))
        sidebar_box.set('stroke', 'black')
        sidebar_box.set('stroke-width', str(self.options['line-weight-heavy']))
        # Create title text within HTML foreignObject element (to support text wrapping)
        html_cont = ET.SubElement(sidebar, 'foreignObject')
        html_cont.set('width', str(self.get_title_sidebar_width()))
        html_cont.set('height', str(page_dims[1] - 2 * margin))
        html_cont.set('x', str(left_border))
        html_cont.set('y', str(margin))
        div = ET.SubElement(html_cont, 'div')
        div.set('xmlns', 'http://www.w3.org/1999/xhtml')
        div.set('id', 'parent')
        stylesheet_link = ET.SubElement(div, 'link')
        stylesheet_link.set('xmlns', 'http://www.w3.org/1999/xhtml')
        stylesheet_link.set('href', self.options['style-source'])
        stylesheet_link.set('rel', 'stylesheet')
        # Attempt to match any tags in the config with metadata tags and input these as titles.
        # Note this will not add any headings, only the title text themselves. Add headings
        # using CSS ::before selector in the external style document
        for t in literal_eval(self.options['titles']):
            if t in document.get_parent_metadata_object(self.plot_file)['tags']:
                element = ET.SubElement(div, 'p')
                element.text = document.get_metadata(self.plot_file, t)
                element.set('xmlns', 'http://www.w3.org/1999/xhtml')
                element.set('class', 'title-'+t)

        fixture_types = self.get_plotted_types()
        for fixture_type, symbol in fixture_types.items():
            legend_div = ET.SubElement(div, 'div')
            legend_div.set('class', 'legend')
            parent_svg = ET.SubElement(legend_div, 'svg')
            parent_svg.set('xmlns', 'http://www.w3.org/2000/svg')
            icon = self.get_legend_fixture_icon(symbol)
            # Every icon is given a square SVG bounding box based on a percentage of the width of the sidebar. This is
            # defined with the sidebar-icon-width-factor property. For example, with a setting of 4, the SVG fixture
            # icon will have a width and height of 25% of the width of the sidebar, and the fixture type label will
            # have a width of 75% of the width of the sidebar.
            parent_svg.set('height', str(self.get_title_sidebar_width() / float(self.options['sidebar-icon-width-factor'])))
            parent_svg.append(icon)
            label = ET.SubElement(legend_div, 'p')
            label.text = fixture_type
            icon_pc_width = 100 / float(self.options['sidebar-icon-width-factor'])
            parent_svg.set('width', str(icon_pc_width)+'%')
            label.set('style', 'width:'+str(100-icon_pc_width)+'%')

        return sidebar

    def fixture_will_fit(self, fixture):
        """See if a fixture will fit in the physical contstraints of the plot."""
        constraints = self.get_physical_constraints()
        x = float(fixture['posX']) * 1000
        y = float(fixture['posY']) * 1000

        if constraints[0] <= x <= constraints[1] and constraints[2] <= y <= constraints[3]:
            return True
        else:
            return False

    def render_symbol(self, symbol_name, colour='White'):
        """Generate a symbol from the given symbol name. Finds the appropriate symbol and
        sets correct path colours and line weights according to the document scale. Does
        not apply any transformation so it will need to be scaled and translated before
        inserting into the document."""
        scale = float(self.options['scale'])
        tree = ET.parse(data.get_data('symbol/' + symbol_name + '.svg'))
        root = tree.getroot()
        svg_ns = {'ns0': 'http://www.w3.org/2000/svg'}
        symbol = root.find('ns0:g', svg_ns)
        for path in symbol:
            if path.get('class') == 'outer':
                path.set('fill', colour)
                path.set('stroke-width',
                         str(float(self.options['line-weight-heavy']) * scale))
                path.set('stroke', 'black')
            if path.get('class') == 'weight-override-light':
                path.set('fill', colour)
                path.set('stroke', 'black')
                path.set('stroke-width',
                         str(float(self.options['line-weight-light']) * scale))
            if path.get('class') == 'weight-override-medium':
                path.set('stroke', 'black')
                path.set('fill', colour)
                path.set('stroke-width',
                         str(float(self.options['line-weight-medium']) * scale))
            if path.get('class') == 'weight-override-heavy':
                path.set('stroke', 'black')
                path.set('fill', colour)
                path.set('stroke-width',
                         str(float(self.options['line-weight-heavy']) * scale))

        return symbol

    def get_legend_fixture_icon(self, symbol_name):
        """Translate a fixture icon so it is in the correct place in the legend."""
        scale = float(self.options['scale'])
        width = self.get_title_sidebar_width() / (float(self.options['sidebar-icon-width-factor']) * 2) * scale
        height = width
        symbol = self.render_symbol(symbol_name)
        symbol.set('transform', 'scale( ' + str(1 / scale) + ' ) ' +
                   'translate( ' + str(width) +
                   ' ' + str(height + float(self.options['line-weight-heavy'])) + ')')

        return symbol

    def get_fixture_icon(self, fixture):
        """Return a transformed fixture icon."""
        centre = self.get_centre_coord()
        plaster = self.get_plaster_coord()
        scale = 1 / float(self.options['scale'])
        plot_pos = lambda dim: (float(fixture['pos' + dim]) * 1000)
        rotation = fixture['rotation']
        if self.options.getboolean('colour-fixtures'):
            colour = fixture['colour']
        else:
            colour = 'White'

        # Create the container for all objects which compose the fixture icon and
        # translate to the correct position
        container = ET.Element('g')
        container.set('transform',
                      'translate(' + str(centre + plot_pos('X') * scale) + ' ' +
                      str(plaster - plot_pos('Y') * scale) + ')')

        # Create the additional information notation
        container.append(self.get_fixture_notation_block(fixture))

        # Create the actual fixture symbol itself
        if 'symbol' not in fixture:
            symbol_name = self.options['fallback-symbol']
        else:
            symbol_name = fixture['symbol']
        # Scale and rotational transforms are on the symbol source group
        # translation transforms are on the container group which also
        # contains channel identifiers etc
        symbol = self.render_symbol(symbol_name, colour=colour)
        symbol.set('transform', 'scale( ' + str(scale) + ' ) ' +
                   'rotate(' + str(rotation) + ')')
        container.append(symbol)

        return container

    def get_fixture_beam(self, fixture):
        if self.options.getboolean('beam-source-colour'):
            colour = fixture['colour']
        else:
            colour = 'black'
        beam = ET.Element('path')
        scale = float(self.options['scale'])
        centre = self.get_centre_coord()
        plaster = self.get_plaster_coord()
        startx = (float(fixture['posX']) * 1000) * (1 / scale) + centre
        starty = (float(fixture['posY']) * 1000) * (1 / scale) * -1 + plaster
        endx = (float(fixture['focusX']) * 1000) * (1 / scale) + centre
        endy = (float(fixture['focusY']) * 1000) * (1 / scale) * -1 + plaster
        beam.set('d', 'M ' + str(startx) + ' ' + str(starty) +
                 ' L ' + str(endx) + ' ' + str(endy))
        beam.set('stroke', colour)
        beam.set('stroke-width', self.options['line-weight-light'])
        beam.set('stroke-dasharray', self.options['beam-dasharray'])
        return beam

    def get_fixture_focus_point(self, fixture):
        if self.options.getboolean('focus-point-source-colour'):
            colour = fixture['colour']
        else:
            colour = 'black'
        point = ET.Element('circle')
        scale = float(self.options['scale'])
        centre = self.get_centre_coord()
        plaster = self.get_plaster_coord()
        posx = float(fixture['focusX']) * 1000 * (1 / scale) + centre
        posy = float(fixture['focusY']) * 1000 * (1 / scale) * -1 + plaster
        point.set('cx', str(posx))
        point.set('cy', str(posy))
        point.set('r', str(self.options['focus-point-radius']))
        point.set('fill', colour)

        return point

    def get_fixture_notation_block(self, fixture):
        handle = self.get_fixture_handle_offset(fixture, 'south')
        notation_container_size = float(self.options['channel-notation-radius'])
        notation_spacing = 1.5

        def get_notation_centre(index, inverted=False):
            """Calculate the coordinates of a given notation bounding box centre, by
            index. For example, the first notation object from the fixture will be
            index zero, then 1, 2 etc."""
            if not inverted:
                return handle[0], handle[1] + notation_container_size * (index * notation_spacing + notation_spacing + index)
            else:
                return handle[0], - handle[1] - notation_container_size * (index * notation_spacing + notation_spacing + index)

        def get_relevant_notations():
            """Get the list of required notations in order from fixture outwards. In tuple
            form of shape, text. e.g. [(6, '23'), (0, '1')] Hexagon = 6, circle = 0, etc"""
            ordered = []
            if 'dimmer' not in fixture and 'circuit' in fixture:
                if self.options.getboolean('show-circuit-number'):
                    ordered.append((6, fixture['circuit']))
            if 'circuit' not in fixture and 'dimmer' in fixture:
                if self.options.getboolean('show-dimmer-number'):
                    ordered.append((6, fixture['dimmer']))
            if 'dimmer' in fixture and 'circuit' in fixture:
                if self.options.getboolean('show-circuit-number'):
                    ordered.append((6, fixture['circuit']))
                if self.options.getboolean('show-dimmer-number'):
                    ordered.append((4, fixture['dimmer']))
            if self.options.getboolean('show-channel-number'):
                ordered.append((0, fixture['ref']))
            return ordered

        def is_inverted():
            """Is the fixture inverted i.e. rotated more than 90deg"""
            if -90 <= float(fixture['rotation']) <= 90 or 270 <= float(fixture['rotation']) <= 360:
                return False
            else:
                return True

        notation_group = ET.Element('g')
        notations = get_relevant_notations()
        # Add the connecting line from the centre of the fixture to the distance of the
        # final notation block, if they are enabled
        if self.options.getboolean('notation-connectors'):
            notation_group.append(ET.Element('line', attrib={
                'x1': '0', 'x2': str(get_notation_centre(len(notations) - 1, inverted=is_inverted())[0]),
                'y1': '0', 'y2': str(get_notation_centre(len(notations) - 1, inverted=is_inverted())[1]),
                'stroke-width': self.options['line-weight-light'], 'stroke': 'black'
            }))
        for i, notation in enumerate(notations):
            notation_block = ET.SubElement(notation_group, 'g')
            # generate_polygon gives us the correctly sized shape to put the notation label in, we just need
            # to style and move it to the correct place
            bounding_box = polygon.generate_polygon(float(self.options['channel-notation-radius']), notation[0])
            bounding_centre = get_notation_centre(i, inverted=is_inverted())
            bounding_box.set('fill', 'White')
            bounding_box.set('stroke', 'black')
            bounding_box.set('stroke-width', self.options['line-weight-light'])
            bounding_box.set('transform', 'translate('+str(bounding_centre[0])+' '+str(bounding_centre[1])+')')
            notation_block.append(bounding_box)
            channel_number = ET.SubElement(notation_block, 'text', attrib={
                'text-anchor': 'middle',
                'dominant-baseline': 'central',
                'x': str(bounding_centre[0]),
                'y': str(bounding_centre[1]),
                'class': 'notation'
            })
            channel_number.text = notation[1]
        return notation_group

    def get_fixture_handle_offset(self, fixture, handle_name):
        """Finds a handle in the fixture icon with the specified name.
        Gives coordinates in (x, y) tuple. Returns (0, 0) if handle
        was not found. The coordinates are in actual scaled units for the
        current document so ready to be used."""
        if 'symbol' not in fixture:
            symbol_name = self.options['fallback-symbol']
        else:
            symbol_name = fixture['symbol']
        svg_ns = {'ns0': 'http://www.w3.org/2000/svg'}
        icon = self.render_symbol(symbol_name)
        groups = icon.findall('ns0:g', svg_ns)
        for g in groups:
            if g.get('id') == 'handles':
                handles = g.findall('ns0:polyline', svg_ns)
                for h in handles:
                    if h.get('id') == handle_name:
                        return [float(i) / float(self.options['scale']) for i in h.get('points').split()]
        return 0, 0

    def generate_plot(self):
        self.lighting_plot = self.get_empty_plot()
        root = self.lighting_plot.getroot()
        if self.options.getboolean('page-border'):
            root.append(self.get_page_border())
        try:
            root.append(self.get_background_image())
        except FileNotFoundError:
            pass
        root.append(self.get_centre_line())
        root.append(self.get_plaster_line())
        for fixture in self.fixtures:
            tagger.tag_fixture_all_doc_independent(fixture)
            if self.fixture_will_fit(fixture):
                if self.options.getboolean('show-beams') and 'focusX' in fixture and 'focusY' in fixture:
                    root.append(self.get_fixture_beam(fixture))
                if self.options.getboolean('show-focus-point') and 'focusX' in fixture and 'focusY' in fixture:
                    root.append(self.get_fixture_focus_point(fixture))
                root.append(self.get_fixture_icon(fixture))
        if self.options['title-block'] != 'None':
            root.append(self.get_title_block())


class PlotExtension(InterpreterExtension):

    def __init__(self, interpreter):
        super().__init__(interpreter)
        self.options = self.interpreter.config['plot']
        self.plot = None

    def register_commands(self):
        self.commands.append(NoRefsCommand(('Plot', 'About'), self.plot_about))
        self.commands.append(NoRefsCommand(('Plot', 'Create'), self.plot_create))
        self.commands.append(NoRefsCommand(('Plot', 'Set'), self.plot_set))
        self.commands.append(NoRefsCommand(('Plot', 'Write'), self.plot_write))

    def plot_create(self):
        self.plot = LightingPlot(self.interpreter.file, self.options)
        self.plot.generate_plot()

    def plot_write(self, path):
        self.plot.lighting_plot.write(os.path.expanduser(path))
        with open(path, 'r+') as f:
            header = '<?xml-stylesheet type="text/css" href="'+self.options['style-source']+'" ?>'
            content = f.read()
            f.seek(0, 0)
            f.write(header.rstrip('\r\n') + '\n' + content)

    def plot_set(self, k, v):
        self.options[k] = v

    def plot_about(self):
        self.interpreter.msg.post_output([k + ': ' + self.options[k] for k in self.options])


def register_extension(interpreter):
    PlotExtension(interpreter).register_extension()
