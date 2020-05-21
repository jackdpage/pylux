from pylux.interpreter import InterpreterExtension, NoRefsCommand
from pylux import document, reference
from pylux.lib import data, tagger, polygon, plothelper
import xml.etree.ElementTree as ET
import os
import decimal
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

    def get_plotted_fixtures(self):
        """Return a list of fixtures which are hung and also fit in the plot area."""
        return [i for i in self.get_hung_fixtures() if self.fixture_will_fit(i)]

    def get_plotted_types(self):
        """Return a list of fixture types used which actually managed to fit. Also
        provide symbol tags. Will assume the first fixture
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

    def get_coordinate(self, measurement, dimension):
        """Get a scaled coordinate in the x or y dimension, taking into account
        margins, padding etc. Provide measurement in millimetres."""
        scale = float(self.options['scale'])
        if dimension == 'x':
            return self.get_centre_coord() + measurement / scale
        elif dimension == 'y':
            return self.get_plaster_coord() - measurement / scale

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

    def is_within_bounds(self, coordinate):
        """Given an x, y tuple in millimetres representing a scaled on-paper coordinate, determine
        whether it is within the drawing area or not."""
        constraints = self.get_physical_constraints()
        if constraints[0] <= coordinate[0] <= constraints[1]:
            return True
        elif constraints[2] <= coordinate[1] <= constraints[3]:
            return True
        else:
            return False

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

    def get_structure(self, structure):
        """Get structure SVG element."""
        if 'structure_type' not in structure:
            return None
        elif structure['structure_type'] == 'batten' or structure['structure_type'] == 'architecture':
            if all(i in structure for i in ('startX', 'startY', 'endX', 'endY')):
                element = ET.Element('polyline')
                element.set('stroke', 'black')
                element.set('stroke-width', self.options['line-weight-heavy'])
                element.set('points',
                            str(self.get_coordinate(float(structure['startX'])*1000, 'x')) + ',' +
                            str(self.get_coordinate(float(structure['startY'])*1000, 'y')) + ' ' +
                            str(self.get_coordinate(float(structure['endX'])*1000, 'x')) + ',' +
                            str(self.get_coordinate(float(structure['endY'])*1000, 'y')))
                return element
            else:
                return None

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

    def get_internal_sidebar_width(self):
        """Get the effective available width in the sidebar, once padding has been taken account for"""
        return self.get_title_sidebar_width() - 2 * float(self.options['sidebar-title-padding'])

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
        html_cont.set('width', str(self.get_internal_sidebar_width()))
        html_cont.set('height', str(page_dims[1] - 2 * margin))
        html_cont.set('x', str(left_border + float(self.options['sidebar-title-padding'])))
        html_cont.set('y', str(margin))
        div = ET.SubElement(html_cont, 'div')
        div.set('xmlns', 'http://www.w3.org/1999/xhtml')
        div.set('id', 'parent')
        stylesheet_link = ET.SubElement(div, 'link')
        stylesheet_link.set('xmlns', 'http://www.w3.org/1999/xhtml')
        stylesheet_link.set('href', data.get_data('style/'+self.options['style-source']))
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
        for fixture_type, symbol_name in fixture_types.items():
            legend_div = ET.SubElement(div, 'div')
            legend_div.set('class', 'legend')
            parent_svg = ET.SubElement(legend_div, 'svg')
            parent_svg.set('xmlns', 'http://www.w3.org/2000/svg')
            icon = self.get_legend_fixture_icon(symbol_name)
            parent_svg.set('height', str(self.get_symbol_height(icon)))
            parent_svg.append(icon)
            label = ET.SubElement(legend_div, 'p')
            label.text = fixture_type
            icon_pc_width = self.get_symbol_width(icon) / self.get_internal_sidebar_width() * 100
            parent_svg.set('width', str(icon_pc_width)+'%')
            label.set('style', 'width:'+str(100-icon_pc_width-float(self.options['legend-text-margin']))+'%;margin-left:'+self.options['legend-text-margin']+'%')

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

    def get_original_symbol(self, symbol_name):
        """Get symbol group from the file, unscaled and unformatted."""
        tree = ET.parse(data.get_data('symbol/' + symbol_name + '.svg'))
        root = tree.getroot()
        svg_ns = {'ns0': 'http://www.w3.org/2000/svg'}
        symbol = root.find('ns0:g', svg_ns)
        return symbol

    def render_symbol(self, symbol_name, colour='White'):
        """Generate a symbol from the given symbol name. Finds the appropriate symbol and
        sets correct path colours and line weights according to the document scale. Does
        not apply any transformation so it will need to be scaled and translated before
        inserting into the document."""
        scale = float(self.options['scale'])
        symbol = self.get_original_symbol(symbol_name)
        for path in symbol:
            if path.get('class') == 'outer':
                path.set('fill', colour)
                path.set('stroke-width',
                         str(float(self.options['line-weight-heavy']) * scale))
                path.set('stroke', 'black')
            if path.get('class') == 'weight-override-light':
                path.set('stroke', 'black')
                path.set('stroke-width',
                         str(float(self.options['line-weight-light']) * scale))
            if path.get('class') == 'weight-override-medium':
                path.set('stroke', 'black')
                path.set('stroke-width',
                         str(float(self.options['line-weight-medium']) * scale))
            if path.get('class') == 'weight-override-heavy':
                path.set('stroke', 'black')
                path.set('stroke-width',
                         str(float(self.options['line-weight-heavy']) * scale))

        return symbol

    def get_fixture_symbol_name(self, fixture):
        """Determine the symbol name to be used for a fixture"""
        if 'symbol' not in fixture:
            return self.options['fallback-symbol']
        else:
            return fixture['symbol']

    def get_symbol_width(self, symbol):
        """Get actual scaled width of the symbol based on east and west handles"""
        max_x = self.get_symbol_handle_offset(symbol, 'east')[0]
        min_x = self.get_symbol_handle_offset(symbol, 'west')[0]
        return max_x - min_x + 2 * float(self.options['line-weight-heavy'])

    def get_symbol_height(self, symbol):
        """Get actual scaled height of the symbol based on north and south handles"""
        max_y = self.get_symbol_handle_offset(symbol, 'south')[1]
        min_y = self.get_symbol_handle_offset(symbol, 'north')[1]
        return max_y - min_y + 2 * float(self.options['line-weight-heavy'])

    def get_symbol_north_height(self, symbol):
        """Get the actual scaled height of a symbol between its centre and north handle."""
        return self.get_symbol_handle_offset(symbol, 'north')[1] * -1 + float(self.options['line-weight-heavy'])

    def get_legend_fixture_icon(self, symbol_name):
        """Translate a fixture icon so it is in the correct place in the legend."""
        scale = float(self.options['scale'])
        symbol = self.render_symbol(symbol_name)
        width = self.get_symbol_width(symbol) * scale
        height = self.get_symbol_north_height(symbol) * scale
        # Translate the symbol half its width and height so the top corner of it is flush
        # with the top left corner of the SVG element.
        symbol.set('transform', 'scale( ' + str(1 / scale) + ' ) ' +
                   'translate( ' + str(width / 2) + ' ' + str(height) + ')')

        return symbol

    def get_symbol_handle_offset(self, symbol, handle_name):
        """Finds a handle in the fixture icon with the specified name.
        Gives coordinates in (x, y) tuple. Returns (0, 0) if handle
        was not found. The coordinates are in actual scaled units for the
        current document so ready to be used."""
        svg_ns = {'ns0': 'http://www.w3.org/2000/svg'}
        groups = symbol.findall('ns0:g', svg_ns)
        for g in groups:
            if g.get('id') == 'handles':
                handles = g.findall('ns0:polyline', svg_ns)
                for h in handles:
                    if h.get('id') == handle_name:
                        return [float(i) / float(self.options['scale']) for i in h.get('points').split()]
        fallback_handle = self.options['fallback-handle-'+handle_name]
        return [float(i) / float(self.options['scale']) for i in fallback_handle.split(',')]

    def generate_plot(self):
        self.lighting_plot = self.get_empty_plot()
        canvas = plothelper.Canvas(self.options)
        root = self.lighting_plot.getroot()
        if self.options.getboolean('page-border'):
            root.append(plothelper.PageBorderComponent(canvas).plot_component)
        try:
            root.append(self.get_background_image())
        except FileNotFoundError:
            pass
        root.append(plothelper.CentreLineComponent(canvas).plot_component)
        root.append(plothelper.PlasterLineComponent(canvas).plot_component)
        if self.options.getboolean('draw-structures'):
            for structure in document.get_by_type(self.plot_file, 'structure'):
                try:
                    root.append(self.get_structure(structure))
                except TypeError:
                    pass
        # We have to iterate through the fixtures to create the component list, before adding anything
        # to the actual plot. This is to allow the hitbox plot to be created so that notation and other
        # components can be placed properly.
        fixture_components = []
        for fixture in self.fixtures:
            if self.fixture_will_fit(fixture):
                tagger.tag_fixture_all_doc_independent(fixture)
                fixture_components.append(plothelper.FixtureComponent(fixture, canvas))
        for fixture_component in fixture_components:
            if self.options.getboolean('show-beams'):
                root.append(plothelper.FixtureBeamComponent(fixture_component, canvas).plot_component)
            if self.options.getboolean('show-focus-point'):
                root.append(plothelper.FixtureFocusPointComponent(fixture_component, canvas).plot_component)
            root.append(plothelper.FixtureNotationBlockComponent(fixture_component, canvas).plot_component)
            root.append(fixture_component.plot_component)
            if self.options.getboolean('show-fixture-hitboxes'):
                root.append(fixture_component.hitbox_component.visualisation)
        if self.options.getboolean('show-scale-rule'):
            root.append(plothelper.RulerComponent(canvas).plot_component)
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
            header = '<?xml-stylesheet type="text/css" href="'+data.get_data('style/'+self.options['style-source'])+'" ?>'
            content = f.read()
            f.seek(0, 0)
            f.write(header.rstrip('\r\n') + '\n' + content)

    def plot_set(self, k, v):
        self.options[k] = v

    def plot_about(self):
        self.interpreter.msg.post_output([k + ': ' + self.options[k] for k in self.options])


def register_extension(interpreter):
    PlotExtension(interpreter).register_extension()
