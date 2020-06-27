from pylux.lib import data
import pylux.lib.polygon as polygonhelper
from pylux import reference
import xml.etree.ElementTree as ET
import math
import numpy
import decimal
import os


class Canvas:
    """The Canvas provides the context of the drawing. It does not contain the
    drawing itself. The Canvas gives Components the parameters they need in order
    to render themselves correctly for the drawing. Other components can contribute
    to the canvas to increase the information available to other components, for
    example by registering their hitboxes so other components can render themselves
    without collision."""

    def __init__(self, options):
        self.options = options
        self.scale = float(self.options['scale'])
        self.rscale = 1 / self.scale
        self.centre = self._get_centre_coord()
        self.plaster = self._get_plaster_coord()
        self.hitbox_plot = HitboxPlot(self.get_plot_width_extent(),
                                      self.get_plot_height_extent())
        self.lighting_filter = LightingFilterContainer(self)

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
            return dimensions[1], dimensions[0]

    def get_title_sidebar_width(self):
        page_dims = self.get_page_dimensions()
        pc_width = page_dims[0] * float(self.options['sidebar-title-width-pc'])
        if pc_width > float(self.options['sidebar-title-max-width']):
            return float(self.options['sidebar-title-max-width'])
        elif pc_width < float(self.options['sidebar-title-min-width']):
            return float(self.options['sidebar-title-min-width'])
        else:
            return pc_width

    def _get_centre_coord(self):
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

    def _get_plaster_coord(self):
        """Get the plaster line y coordinate.

        Returns the plaster line y coordinate to allow offsets to
        be calculated when plotting fixtures.

        Returns:
            A float representing the y coordinate in mm.
        """
        centre = self.get_page_dimensions()[1] / 2
        padding = float(self.options['plaster-line-padding']) * 1000 * self.rscale
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

    def get_coordinate(self, coord):
        """From a real-life coordinate, get the scaled coordinate for the plot"""
        return (self._get_centre_coord() + coord[0] * self.rscale,
                self._get_plaster_coord() - coord[1] * self.rscale)

    def get_line_intersection(self, start, end):
        """Given the start and end coordinates of a straight line, return the
        actual start and end coordinates which will allow it to fit within the borders
        of the plot, if it extends over them."""
        # If both x coords are the same, this is a vertical line
        if start[0] == end[0]:
            return (start[0], max(self.get_plot_height_extent()[0], start[1])), \
                   (start[0], min(self.get_plot_height_extent()[1], end[1]))
        # If both y coords are the same, this is a horizontal line
        elif start[1] == end[1]:
            return (max(self.get_plot_width_extent()[0], start[0]), start[1]),\
                   (min(self.get_plot_width_extent()[1], end[0]), start[1])
        # If neither are the same, we need to do some maths
        else:
            # Find line equation in form y = mx + c
            m = (end[1] - start[1]) / (end[0] - start[0])
            c = start[1] - m * start[0]
            y_intercept_left = m * self.get_plot_width_extent()[0] + c
            y_intercept_right = m * self.get_plot_width_extent()[1] + c
            # If y left intercept is out of plot, use x top intercept as start
            if y_intercept_left < self.get_plot_height_extent()[0]:
                adj_start = (self.get_plot_height_extent()[0] - c) / m, self.get_plot_height_extent()[0]
            else:
                adj_start = self.get_plot_width_extent()[0], y_intercept_left
            # If y right intercept is out of plot, use x bottom intercept as end
            if y_intercept_right > self.get_plot_height_extent()[1]:
                adj_end = (self.get_plot_height_extent()[1] - c) / m, self.get_plot_height_extent()[1]
            else:
                adj_end = self.get_plot_width_extent()[1], y_intercept_right
            return adj_start, adj_end


class HitboxPlot:

    def __init__(self, x_range, y_range):
        self.components = []
        self.x_range = x_range
        self.y_range = y_range

    def register_hitbox(self, hitbox_component):
        self.components.append(hitbox_component)

    def does_collide(self, hitbox_component):
        vertices = [(hitbox_component.x_range[0], hitbox_component.y_range[0]),
                    (hitbox_component.x_range[1], hitbox_component.y_range[0]),
                    (hitbox_component.x_range[0], hitbox_component.y_range[1]),
                    (hitbox_component.x_range[1], hitbox_component.y_range[1])]
        # There is a collision if any of the component vertices lie outside of the plot area
        for vertex in vertices:
            if (vertex[0] < self.x_range[0] or vertex[0] > self.x_range[1] or
                    vertex[1] < self.y_range[0] or vertex[1] > self.y_range[1]):
                return True
        for test in self.components:
            # There is a collision if any of the component vertices are in the test hitbox
            for vertex in vertices:
                if (test.x_range[0] <= vertex[0] <= test.x_range[1] and
                        test.y_range[0] <= vertex[1] <= test.y_range[1]):
                    return True
            # There is also a collision if the component straddles the x values one of its y values is within the
            # y range
            if (hitbox_component.x_range[0] < test.x_range[0] and hitbox_component.x_range[1] > test.x_range[1]) and \
                    (test.y_range[0] < hitbox_component.y_range[0] < test.y_range[1] or
                     test.y_range[0] < hitbox_component.y_range[1] < test.y_range[1]):
                return True
            # Similarly there is a collision if the component straddles the y values and one of its x values
            # is within the test x range
            if (hitbox_component.y_range[0] < test.y_range[0] and hitbox_component.y_range[1] > test.y_range[1]) and \
                    (test.x_range[0] < hitbox_component.x_range[0] < test.x_range[1] or
                     test.x_range[0] < hitbox_component.x_range[1] < test.x_range[1]):
                return True
            # Finally, there is a collision if the components' y and x values both straddle the test hitbox (i.e.
            # the test hitbox is within the component)
            if (hitbox_component.x_range[0] < test.x_range[0] and hitbox_component.x_range[1] > test.x_range[1] and
                    hitbox_component.y_range[0] < test.y_range[0] and hitbox_component.y_range[1] > test.y_range[1]):
                return True
        return False


class HitboxComponent:
    """A hitbox component is a special component used internally to determine if
    there are collisions between other components. They can also be enabled visually
    in the output if required for debugging purposes."""

    def __init__(self, x1, y1, x2, y2, canvas):
        self._canvas = canvas
        self.x_range = x1, x2
        self.y_range = y1, y2
        self.visualisation = self._get_visualisation()

    def _get_visualisation(self):
        polygon = ET.Element('polygon')
        polygon.set('points',
                    str(self.x_range[0]) + ',' + str(self.y_range[0]) + ' ' +
                    str(self.x_range[0]) + ',' + str(self.y_range[1]) + ' ' +
                    str(self.x_range[1]) + ',' + str(self.y_range[1]) + ' ' +
                    str(self.x_range[1]) + ',' + str(self.y_range[0]))
        polygon.set('fill', 'none')
        polygon.set('stroke-width', self._canvas.options['line-weight-hitbox'])
        polygon.set('stroke', self._canvas.options['hitbox-colour'])
        return polygon


class FixtureComponent:

    def __init__(self, fixture, canvas):
        self.fixture = fixture
        self._canvas = canvas
        self._options = canvas.options
        self.symbol = self._get_rendered_symbol()
        self.plot_component = self._get_transformed_symbol()
        self.hitbox_component = self._get_hitbox()
        self._canvas.hitbox_plot.register_hitbox(self.hitbox_component)

    def _get_symbol_name(self):
        """Get the name of the symbol for this fixture. Will always be that given
        by the symbol tag, if it exists."""
        if 'symbol' not in self.fixture.data:
            return self._options['fallback-symbol']
        else:
            return self.fixture.data['symbol']

    def _get_raw_symbol(self):
        """Get the first top-level group from the symbol file for this fixture, ready
        to be rendered."""
        tree = ET.parse(data.get_data('symbol/' + self._get_symbol_name() + '.svg'))
        root = tree.getroot()
        ns = {'ns0': 'http://www.w3.org/2000/svg'}
        return root.find('ns0:g', ns)

    def get_render_colour(self):
        """Get the appropriate render colour for this fixture. Will always be given
        by the colour tag, unless (as is default) colour-fixtures is disabled, in which
        case it will just be white."""
        if self._options.getboolean('colour-fixtures'):
            return self.fixture.data['colour']
        else:
            return 'White'

    def is_inverted(self):
        """Is the fixture inverted i.e. rotated more than 90deg"""
        if -90 <= float(self.fixture.data['rotation']) <= 90 or 270 <= float(self.fixture.data['rotation']) <= 360:
            return False
        else:
            return True

    def _get_rendered_symbol(self):
        """Render a raw symbol as it will appear at the scaling of the plot. Set
        appropriate line weights, set fill and apply scale transform as necessary."""
        symbol = self._get_raw_symbol()
        colour = self.get_render_colour()
        for path in symbol:
            if path.get('class') == 'outer':
                path.set('fill', colour)
                path.set('stroke', 'black')
                path.set('stroke-width', str(float(self._options['line-weight-heavy']) * self._canvas.scale))
            if path.get('class') == 'weight-override-light':
                path.set('stroke-width', str(float(self._options['line-weight-light']) * self._canvas.scale))
            if path.get('class') == 'weight-override-medium':
                path.set('stroke-width', str(float(self._options['line-weight-medium']) * self._canvas.scale))
            if path.get('class') == 'weight-override-heavy':
                path.set('stroke-width', str(float(self._options['line-weight-heavy']) * self._canvas.scale))
        symbol.set('transform', 'scale(' + str(self._canvas.rscale) + ')')
        return symbol

    def get_x_pos(self):
        """Get the actual point on the canvas that this fixture should be placed."""
        return self._canvas.centre + float(self.fixture.data['posX']) * 1000 * self._canvas.rscale

    def get_y_pos(self):
        """Get the actual point on the canvas that this fixture should be placed."""
        return self._canvas.plaster - float(self.fixture.data['posY']) * 1000 * self._canvas.rscale

    def get_x_focus(self):
        """Get the actual point on the canvas where the fixture is focused. If there is no
        focus point, this will be the same as the fixture position."""
        if 'focusX' in self.fixture.data:
            return self._canvas.centre + float(self.fixture.data['focusX']) * 1000 * self._canvas.rscale
        else:
            return self.get_x_pos()

    def get_y_focus(self):
        """Get the actual point on the canvas where the fixture is focused. If there is no
        focus point, this will be the same as the fixture position."""
        if 'focusY' in self.fixture.data:
            return self._canvas.plaster - float(self.fixture.data['focusY']) * 1000 * self._canvas.rscale
        else:
            return self.get_y_pos()

    def _get_transformed_symbol(self):
        """Translate and rotate the rendered symbol to its plot position."""
        container = ET.Element('g')
        container.set('transform',
                      'translate(' + str(self.get_x_pos()) + ' ' + str(self.get_y_pos()) + ') ' +
                      'rotate(' + str(self.fixture.data['rotation']) + ')')
        container.append(self._get_rendered_symbol())
        return container

    def get_symbol_handle_offset(self, handle_name):
        """Finds a handle in the fixture icon with the specified name.
        Gives coordinates in (x, y) tuple. Returns (0, 0) if handle
        was not found. The coordinates are in actual scaled units for the
        current document so ready to be used."""
        symbol = self._get_raw_symbol()
        svg_ns = {'ns0': 'http://www.w3.org/2000/svg'}
        groups = symbol.findall('ns0:g', svg_ns)
        for g in groups:
            if g.get('id') == 'handles':
                handles = g.findall('ns0:polyline', svg_ns)
                for h in handles:
                    if h.get('id') == handle_name:
                        return [float(i) * self._canvas.rscale for i in h.get('points').split()]
        fallback_handle = self._options['fallback-handle-'+handle_name]
        return [float(i) * self._canvas.rscale for i in fallback_handle.split(',')]

    def _get_hitbox(self):
        """Get hitbox object for this fixture."""
        rotation = math.radians(float(self.fixture.data['rotation']))
        n = self.get_symbol_handle_offset('north')[1] - 0.5 * float(self._canvas.options['line-weight-heavy'])
        e = self.get_symbol_handle_offset('east')[0] + 0.5 * float(self._canvas.options['line-weight-heavy'])
        s = self.get_symbol_handle_offset('south')[1] + 0.5 * float(self._canvas.options['line-weight-heavy'])
        w = self.get_symbol_handle_offset('west')[0] - 0.5 * float(self._canvas.options['line-weight-heavy'])
        unrotated_hitbox = numpy.array([[w, e, e, w], [n, n, s, s]])
        rotation_matrix = numpy.array([[math.cos(rotation), -math.sin(rotation)],
                                       [math.sin(rotation), math.cos(rotation)]])
        rotated_hitbox = rotation_matrix.dot(unrotated_hitbox)
        return HitboxComponent(
            self.get_x_pos() + min(rotated_hitbox[0]), self.get_y_pos() + min(rotated_hitbox[1]),
            self.get_x_pos() + max(rotated_hitbox[0]), self.get_y_pos() + max(rotated_hitbox[1]),
            self._canvas
        )


class FixtureBeamComponent:

    def __init__(self, fixture_component, canvas):
        self._fixture_component = fixture_component
        self._canvas = canvas
        self.plot_component = self._get_fixture_beam()

    def _get_fixture_beam(self):
        if self._canvas.options.getboolean('beam-source-colour'):
            colour = self._fixture_component.get_render_colour()
        else:
            colour = 'black'
        line = ET.Element('line')
        line.set('x1', str(self._fixture_component.get_x_pos()))
        line.set('y1', str(self._fixture_component.get_y_pos()))
        line.set('x2', str(self._fixture_component.get_x_focus()))
        line.set('y2', str(self._fixture_component.get_y_focus()))
        line.set('stroke', colour)
        line.set('stroke-width', self._canvas.options['line-weight-light'])
        line.set('stroke-dasharray', self._canvas.options['beam-dasharray'])
        return line


class FixtureFocusPointComponent:

    def __init__(self, fixture_component, canvas):
        self._fixture_component = fixture_component
        self._canvas = canvas
        self._notation_items = []
        self.plot_component = self._get_focus_point()

    def _get_focus_point(self):
        if self._canvas.options.getboolean('focus-point-source-colour'):
            colour = self._fixture_component.get_render_colour()
        else:
            colour = 'black'
        circle = ET.Element('circle')
        circle.set('cx', str(self._fixture_component.get_x_focus()))
        circle.set('cy', str(self._fixture_component.get_y_focus()))
        circle.set('r', str(self._canvas.options['focus-point-radius']))
        circle.set('fill', colour)
        return circle


class FilterIncidencePlane:

    def __init__(self, canvas):
        self._canvas = canvas
        self.plot_component = self._get_plot_component()

    def _get_plot_component(self):
        g = ET.Element('g', attrib={'filter': 'url(#lx-render)'})
        g.append(ET.Element('rect', attrib={
            'x': str(self._canvas.get_plot_width_extent()[0]),
            'y': str(self._canvas.get_plot_height_extent()[0]),
            'width': str(self._canvas.get_plot_width_extent()[1] -
                         self._canvas.get_plot_width_extent()[0]),
            'height': str(self._canvas.get_plot_height_extent()[1] -
                          self._canvas.get_plot_height_extent()[0]),
            'fill': self._canvas.options['incidence-plane-colour']
        }))
        return g


class LightingFilterContainer:

    def __init__(self, canvas):
        self._canvas = canvas
        self.plot_component = self._get_empty_component()
        self.filters = []

    def _get_empty_component(self):
        defs = ET.Element('defs')
        defs.append(ET.Element('filter', attrib={'id': 'lx-render'}))
        return defs

    def add_filter(self, fixture_component):
        if not self.filters:
            parent_filter = None
        else:
            parent_filter = self.filters[-1]
        specular_component = BeamSpecularFilterComponent(fixture_component, self._canvas)
        composite_component = BeamCompositeFilterComponent(specular_component, parent_filter, self._canvas)
        self.filters.append(composite_component)
        self.plot_component.find('filter').append(specular_component.plot_component)
        self.plot_component.find('filter').append(composite_component.plot_component)


class BeamSpecularFilterComponent:

    def __init__(self, fixture_component, canvas):
        self._fixture_component = fixture_component
        self._canvas = canvas
        self.result_id = 'specular-'+str(self._fixture_component.fixture.ref)
        if self._canvas.options.getboolean('colour-beam-pools'):
            self.colour = self._fixture_component.fixture.data['colour']
        else:
            self.colour = 'White'
        self.plot_component = self._get_specular_component()

    def _get_specular_component(self):
        specular_component = ET.Element('feSpecularLighting', attrib={
            'lighting-color': self.colour,
            'specularExponent': self._fixture_component.fixture.data.get('beam_focus',
                                                                    self._canvas.options['default-beam-focus']),
            'specularConstant': self._canvas.options['surface-reflectivity'],
            'result': self.result_id
        })
        specular_component.append(ET.Element('feSpotLight', attrib={
            'x': str(self._fixture_component.get_x_pos()),
            'y': str(self._fixture_component.get_y_pos()),
            'z': '100',
            'pointsAtX': str(self._fixture_component.get_x_focus()),
            'pointsAtY': str(self._fixture_component.get_y_focus()),
            'limitingConeAngle': str(self._fixture_component.fixture.data.get('beam_angle',
                                                                         self._canvas.options['default-beam-angle']))
        }))
        return specular_component


class BeamCompositeFilterComponent:

    def __init__(self, filter_component, link, canvas):
        """feComposite component combining filter and link. Leave link empty to use
        SourceGraphic. Link is another BeamCompositeFilterComponent"""
        self._filter_component = filter_component
        self.result_id = 'composite-'+filter_component.result_id
        if not link:
            self._link = 'SourceGraphic'
            if canvas.options.getboolean('render-incidence-plane'):
                self._k2 = '1'
            else:
                self._k2 = '0'
        else:
            self._link = link.result_id
            self._k2 = '1'
        self.plot_component = self._get_plot_component()

    def _get_plot_component(self):
        fe_composite = ET.Element('feComposite', attrib={
            'in': self._link,
            'in2': self._filter_component.result_id,
            'result': self.result_id,
            'k1': '0',
            'k2': self._k2,
            'k3': '1',
            'k4': '0',
            'operator': 'arithmetic'
        })
        return fe_composite


class FixtureNotationBlockComponent:

    def __init__(self, fixture_component, canvas):
        self.fixture_component = fixture_component
        self.canvas = canvas
        self._used_notation = self._get_used_notations()
        self._radius = float(self.canvas.options['channel-notation-radius'])
        self._spacing = float(self.canvas.options['channel-notation-spacing'])
        self._centres = self._calculate_centres()
        self.item_components = []
        self.plot_component = self._get_fixture_notation_block()

    def _get_used_notations(self):
        """Get the list of required notations in order from fixture outwards. In tuple
        form of shape, text. e.g. [(6, '23'), (0, '1')] Hexagon = 6, circle = 0, etc"""
        ordered = []
        if 'dimmer' not in self.fixture_component.fixture.data and 'circuit' in self.fixture_component.fixture.data:
            if self.canvas.options.getboolean('show-circuit-number'):
                ordered.append((6, self.fixture_component.fixture.data['circuit']))
        if 'circuit' not in self.fixture_component.fixture.data and 'dimmer' in self.fixture_component.fixture.data:
            if self.canvas.options.getboolean('show-dimmer-number'):
                ordered.append((6, self.fixture_component.fixture.data['dimmer']))
        if 'dimmer' in self.fixture_component.fixture.data and 'circuit' in self.fixture_component.fixture.data:
            if self.canvas.options.getboolean('show-circuit-number'):
                ordered.append((6, self.fixture_component.fixture.data['circuit']))
            if self.canvas.options.getboolean('show-dimmer-number'):
                ordered.append((4, self.fixture_component.fixture.data['dimmer']))
        if self.canvas.options.getboolean('show-channel-number'):
            ordered.append((0, str(self.fixture_component.fixture.ref)))
        return ordered

    def _rotate_point(self, p, r, c=(0, 0)):
        """Rotate a point by r degrees about centre c"""
        unrotated_point = numpy.array([[p[0] - c[0]], [p[1] - c[1]]])
        rotation_matrix = numpy.array([[math.cos(math.radians(r)),
                                        -math.sin(math.radians(r))],
                                       [math.sin(math.radians(r)),
                                        math.cos(math.radians(r))]])
        rotated_point = rotation_matrix.dot(unrotated_point)
        return rotated_point[0][0] + c[0], rotated_point[1][0] + c[1]

    def _apply_crude_rotation(self, centre):
        """Centres are calculated assuming that the fixture is pointing in the zero (north)
        direction. However, it is quite possible that it will be inverted or pointing in some
        other intermediary direction, so we need to rotate these centres with the fixture. Rather
        than rotating by the exact rotation of the fixture, we rotate either 0 or 180 degrees.
        This way, where there is a line of fixtures with slightly differing rotations, their
        notations will line up, which looks a lot nicer. The exception is if a fixture is
        rotated exactly 90 degrees, in which case it is probably on a boom or similar, so the
        notation will also be rotated exactly 90 degrees."""
        rotation = float(self.fixture_component.fixture.data['rotation'])
        if 90 < rotation < 270:
            r = 180
        elif rotation == 90:
            r = 90
        elif rotation == 270 or rotation == -90:
            r = 270
        else:
            r = 0
        return self._rotate_point(centre, r, (self.fixture_component.get_x_pos(),
                                              self.fixture_component.get_y_pos()))

    def _reverse_crude_rotation(self, centre):
        """Apply the reverse of the crude rotation. This is done because in actual fact, centres
        are calculated based on the fixture pointing in a zero direction, and then rotated.
        Therefore we want to make sure the origin we are starting from is the origin as if it
        had not been rotated."""
        rotation = float(self.fixture_component.fixture.data['rotation'])
        if 90 < rotation < 270:
            r = 180
        elif rotation == 90:
            r = 270
        elif rotation == 270 or rotation == -90:
            r = 90
        else:
            r = 0
        return self._rotate_point(centre, r, (self.fixture_component.get_x_pos(),
                                              self.fixture_component.get_y_pos()))

    def _generate_hitbox_from_centre(self, centre):
        """Create a hitbox object from a centre coordinate."""
        return HitboxComponent(centre[0] - self._radius, centre[1] - self._radius,
                               centre[0] + self._radius, centre[1] + self._radius,
                               self.canvas)

    def _calculate_centres(self):
        """Calculates where the notation items should be without colliding with existing features and following
        the placement hierarchy."""
        # The functions which are used to calculate an (unrotated centre) from an origin, o, in
        # preference order. These differ slightly for the first item in the notation block (first
        # order placements)
        first_order_placements = [
            lambda o: (o[0], o[1] + 2 * self._radius + self._spacing),
            lambda o: (o[0] + 2 * self._radius + self._spacing,
                       o[1] + 2 * self._radius + self._spacing),
            lambda o: (o[0] - 2 * self._radius + self._spacing,
                       o[1] + 2 * self._radius + self._spacing)
        ]
        second_order_placements = [
            lambda o: (o[0], o[1] + 2 * self._radius + self._spacing),
            lambda o: (o[0] + (2 * self._radius + self._spacing) / math.sqrt(2),
                       o[1] + (2 * self._radius + self._spacing) / math.sqrt(2)),
            lambda o: (o[0] - (2 * self._radius + self._spacing) / math.sqrt(2),
                       o[1] + (2 * self._radius + self._spacing) / math.sqrt(2)),
            lambda o: (o[0] + 2 * self._radius + self._spacing, o[1]),
            lambda o: (o[0] - 2 * self._radius - self._spacing, o[1])
        ]
        # We have a preference order of origin handles to use. If the notation block can't be placed
        # from one using the standard rules, the next origin handle will be attempted (S, E, W, N)
        origin_preference = [
            (self.fixture_component.get_x_pos(), self.fixture_component.get_y_pos() +
             self.fixture_component.get_symbol_handle_offset('south')[1] - self._radius),
            (self.fixture_component.get_x_pos() + self.fixture_component.get_symbol_handle_offset('east')[0] -
             self._radius, self.fixture_component.get_y_pos()),
            (self.fixture_component.get_x_pos() + self.fixture_component.get_symbol_handle_offset('west')[0] +
             self._radius, self.fixture_component.get_y_pos()),
            (self.fixture_component.get_x_pos(), self.fixture_component.get_y_pos() +
             self.fixture_component.get_symbol_handle_offset('north')[1] + self._radius)
        ]
        # Additional rotation needs to be applied so that the placement functions match up with the
        # handle being used (all placement functions are written for the south handle only) Index matches
        # the origin in origin_preference
        handle_rotation_offset = [0, 90, -90, 180]
        n_items = len(self._used_notation)
        centres = []
        fixture_centre = (self.fixture_component.get_x_pos(), self.fixture_component.get_y_pos())
        # Start with the south handle
        origin_handle_index = 0
        origin = origin_preference[origin_handle_index]
        while len(centres) < n_items:
            if len(centres) == 0:
                placement_functions = first_order_placements
            else:
                placement_functions = second_order_placements
            for f in placement_functions:
                # We create a 'ghost origin' which is the origin as if we were using the south handle. This way we can
                # use the same functions for all handles
                ghost_origin = self._rotate_point(origin, handle_rotation_offset[origin_handle_index], fixture_centre)
                # Then we rotate back by the handle rotation offset and then finally by a crude rotation if the fixture
                # is flipped or at 90 degrees
                c = self._apply_crude_rotation(self._rotate_point(f(ghost_origin),
                                                                  -1 * handle_rotation_offset[origin_handle_index],
                                                                  fixture_centre))
                if not self.canvas.hitbox_plot.does_collide(self._generate_hitbox_from_centre(c)):
                    centres.append(c)
                    origin = self._reverse_crude_rotation(c)
                    break
                # If this is the last option in the placement functions, we are going to have to
                # start all over again with a different handle as the origin
                elif placement_functions.index(f) == len(placement_functions) - 1:
                    if origin_handle_index < len(origin_preference) - 1:
                        centres = []
                        origin_handle_index += 1
                        origin = origin_preference[origin_handle_index]
                    # If there are no remaining handles or placement functions then we're
                    # pretty much screwed. We'll just have to give what we've got
                    else:
                        centres.append(c)
                        origin = self._reverse_crude_rotation(c)
        for c in centres:
            self.canvas.hitbox_plot.register_hitbox(self._generate_hitbox_from_centre(c))
        return centres

    def _get_notation_item(self, n):
        """Get the nth notation item component"""
        return FixtureNotationItemComponent(self._used_notation[n][0], self._used_notation[n][1],
                                            self._centres[n], self.canvas)

    def _get_fixture_notation_block(self):
        group = ET.Element('g')
        for notation in self._used_notation:
            self.item_components.append(self._get_notation_item(self._used_notation.index(notation)))
        group.append(FixtureNotationConnectorComponent(self).plot_component)
        for component in self.item_components:
            group.append(component.plot_component)
        return group


class FixtureNotationItemComponent:

    def __init__(self, vertices, text, centre, canvas):
        self._canvas = canvas
        self._radius = float(self._canvas.options['channel-notation-radius'])
        self._spacing = float(self._canvas.options['channel-notation-spacing'])
        self._vertices = vertices
        self._text = text
        self.centre = centre
        self.plot_component = self._get_notation_item()

    def _get_hitbox_component(self):
        return HitboxComponent(self.centre[0] - self._radius, self.centre[1] - self._radius,
                               self.centre[0] + self._radius, self.centre[1] + self._radius,
                               self._canvas)

    def _get_notation_item(self):
        group = ET.Element('g')
        bounding_box = polygonhelper.generate_polygon(self._radius, self._vertices)
        bounding_box.set('fill', 'White')
        bounding_box.set('stroke', 'black')
        bounding_box.set('stroke-width', self._canvas.options['line-weight-light'])
        bounding_box.set('transform', 'translate(' + str(self.centre[0]) + ' ' + str(self.centre[1]) + ')')
        group.append(bounding_box)
        channel_number = ET.SubElement(group, 'text', attrib={
            'text-anchor': 'middle',
            'dominant-baseline': 'central',
            'x': str(self.centre[0]),
            'y': str(self.centre[1]),
            'class': 'notation'
        })
        channel_number.text = self._text
        return group


class FixtureNotationConnectorComponent:

    def __init__(self, notation_block):
        self._notation_block = notation_block
        self._fixture_component = self._notation_block.fixture_component
        self.plot_component = self._get_connector()

    def _get_connector(self):
        polyline = ET.Element('polyline')
        points = [(self._fixture_component.get_x_pos(), self._fixture_component.get_y_pos())]
        for notation in self._notation_block.item_components:
            points.append(notation.centre)
        polyline.set('points', ' '.join([str(i[0]) + ',' + str(i[1]) for i in points]))
        polyline.set('stroke-width', self._notation_block.canvas.options['line-weight-light'])
        polyline.set('stroke', 'black')
        polyline.set('fill', 'none')
        return polyline


class FixtureAdditionalTextComponent:

    def __init__(self, fixture_component, canvas):
        self._fixture_component = fixture_component
        self._canvas = canvas
        self.plot_component = self._get_plot_component()

    def _get_plot_component(self):
        text = ET.Element('text', attrib={
            'text-anchor': 'middle',
            'x': str(self._fixture_component.get_x_pos()),
            'y': str(self._fixture_component.get_y_pos() +
                     self._fixture_component.get_symbol_handle_offset('north')[1] -
                     float(self._canvas.options['channel-notation-spacing'])),
            'class': 'notation-additional'
        })
        if 'gel' in self._fixture_component.fixture.data:
            text.text = self._fixture_component.fixture.data['gel']
        return text


class RulerComponent:

    def __init__(self, canvas):
        self._canvas = canvas
        self.plot_component = self._get_ruler()

    def _get_ruler(self):
        container = ET.Element('g', attrib={'class': 'rule'})
        # Generate a list of points the rule contains
        major_increments = []
        minor_increments = []
        i = 0
        while (i + 1) * decimal.Decimal(self._canvas.options['scale-rule-major-increment']) <= decimal.Decimal(
                self._canvas.options['scale-rule-major-length']):
            major_increments.append(i * decimal.Decimal(self._canvas.options['scale-rule-major-increment']))
            i += 1
        i = 0
        while (i + 1) * decimal.Decimal(self._canvas.options['scale-rule-minor-increment']) <= decimal.Decimal(
                self._canvas.options['scale-rule-minor-length']):
            minor_increments.append(
                -1 * i * decimal.Decimal(self._canvas.options['scale-rule-minor-increment']) - decimal.Decimal(
                    self._canvas.options['scale-rule-minor-increment']))
            i += 1
        if minor_increments:
            minor_width = abs(float(minor_increments[-1])) * 1000 * self._canvas.rscale
        else:
            minor_width = 0
        if major_increments:
            major_width = (float(major_increments[-1]) + float(self._canvas.options['scale-rule-major-increment'])) * 1000 * self._canvas.rscale
        else:
            major_width = 0
        total_width = minor_width + major_width
        # Create bounding box around the scale with the decorative border. This is required over putting
        # the border on individual ticks as otherwise it will make black ticks look larger than white ticks.
        container.append(ET.Element('rect', attrib={
            'x': str(-1 * minor_width),
            # Calculate total rule width
            'width': str(total_width),
            'y': str(-1 * float(self._canvas.options['scale-rule-thickness']) -
                     float(self._canvas.options['line-weight-light'])),
            'height': self._canvas.options['scale-rule-thickness'],
            'stroke': 'black',
            'stroke-width': self._canvas.options['line-weight-light'],
            'fill': 'white',
        }))
        # Label at the zero position needs to be added manually as it won't be added through any of the tick
        # iterations
        zero_val = ET.SubElement(container, 'text', attrib={
            'x': '0', 'y': str(-1 * float(self._canvas.options['scale-rule-label-padding']) -
                               float(self._canvas.options['scale-rule-thickness']) -
                               2 * float(self._canvas.options['line-weight-light']))})
        zero_val.text = '0'
        scale_label = ET.SubElement(container, 'text', attrib={
            'x': str(total_width / 2 - minor_width), 'y': str(-1 * float(self._canvas.options['scale-rule-label-padding']) -
                                                              float(self._canvas.options['scale-rule-thickness']) -
                                                              2 * float(self._canvas.options['line-weight-light']) -
                                                              float(self._canvas.options['scale-text-padding']))})
        scale_label.text = 'SCALE 1:' + self._canvas.options['scale']
        unit_label = ET.SubElement(container, 'text', attrib={
            'x': str(total_width - minor_width + float(self._canvas.options['scale-text-padding'])),
            'y': str(-1 * float(self._canvas.options['scale-rule-label-padding']) -
                     float(self._canvas.options['scale-rule-thickness']) -
                     2 * float(self._canvas.options['line-weight-light'])),
            'class': 'units-label'
        })
        unit_label.text = self._canvas.options['scale-rule-units']

        def add_scale_tick(start_point, filled, m):
            """Add minor or major tick (according to m) at a starting point. Minor ticks assumed to be
            in negative direction."""
            scale_bar = ET.SubElement(container, 'rect')
            scale_bar.set('x', str(float(start_point) * 1000 * self._canvas.rscale))
            scale_bar.set('width',
                          str(float(self._canvas.options['scale-rule-' + m + '-increment']) * 1000 * self._canvas.rscale))
            scale_bar.set('y',
                          str(-1 * float(self._canvas.options['scale-rule-thickness']) -
                              float(self._canvas.options['line-weight-light'])))
            scale_bar.set('height', self._canvas.options['scale-rule-thickness'])
            if filled:
                scale_bar.set('fill', 'black')
            else:
                scale_bar.set('fill', 'white')
            tick_label = ET.SubElement(container, 'text')
            # For minor labels, the label will be at the left-point (start_point) of the tick. For major labels,
            # the label will be at the right-point (start_point + increment) of the tick
            if m == 'minor':
                tick_label.set('x', str(float(start_point) * 1000 * self._canvas.rscale))
                tick_label.text = str(abs(start_point))
            else:
                tick_label.set('x', str(
                    ((float(start_point) +
                      float(self._canvas.options['scale-rule-major-increment'])) * 1000 * self._canvas.rscale)))
                tick_label.text = str(start_point + decimal.Decimal(self._canvas.options['scale-rule-major-increment']))
            tick_label.set('y', str(-1 * float(self._canvas.options['scale-rule-label-padding']) -
                                    float(self._canvas.options['scale-rule-thickness']) -
                                    2 * float(self._canvas.options['line-weight-light'])))

        # Add major increments, starting with a filled one
        increment_filled = True
        for i in major_increments:
            add_scale_tick(i, increment_filled, 'major')
            increment_filled = not increment_filled
        # Add minor increments, starting with an unfilled one
        increment_filled = False
        for i in minor_increments:
            add_scale_tick(i, increment_filled, 'minor')
            increment_filled = not increment_filled
        container.set('transform', 'translate(' +
                      str(self._canvas.get_plot_width_extent()[0] + minor_width +
                          float(self._canvas.options['scale-rule-padding'])) + ' ' +
                      str(self._canvas.get_plot_height_extent()[1] -
                          float(self._canvas.options['scale-rule-padding'])) + ')')
        return container


class StructureComponent:

    def __init__(self, canvas, structure):
        self._canvas = canvas
        self.structure = structure
        self.plot_component = self._get_plot_component()

    def _get_plot_component(self):
        if 'structure_type' not in self.structure.data:
            return ET.Element('g')
        elif self.structure.data['structure_type'] in ['batten', 'architecture']:
            if all(i in self.structure.data for i in ('startX', 'startY', 'endX', 'endY')):
                start = self._canvas.get_coordinate((float(self.structure.data['startX']) * 1000,
                                                     float(self.structure.data['startY']) * 1000))
                end = self._canvas.get_coordinate((float(self.structure.data['endX']) * 1000,
                                                   float(self.structure.data['endY']) * 1000))
                corrected_points = self._canvas.get_line_intersection(start, end)
                polyline = ET.Element('polyline')
                polyline.set('stroke', 'black')
                polyline.set('stroke-width', self._canvas.options['line-weight-heavy'])
                polyline.set('points', ' '.join([','.join(map(str, i)) for i in corrected_points]))
                return polyline
            else:
                return ET.Element('g')
        else:
            return ET.Element('g')


class CentreLineComponent:

    def __init__(self, canvas):
        self._canvas = canvas
        self.plot_component = self._get_plot_component()

    def _get_plot_component(self):
        if self._canvas.options.getboolean('centre-line-extend'):
            y_values = (0, self._canvas.get_page_dimensions()[1])
        else:
            y_values = self._canvas.get_plot_height_extent()
        centre_line = ET.Element('line')
        centre_line.set('x1', str(self._canvas.centre))
        centre_line.set('x2', str(self._canvas.centre))
        centre_line.set('y1', str(y_values[0]))
        centre_line.set('y2', str(y_values[1]))
        centre_line.set('stroke', 'black')
        centre_line.set('stroke-width', str(self._canvas.options['line-weight-medium']))
        centre_line.set('stroke-dasharray', self._canvas.options['centre-line-dasharray'])
        return centre_line


class PlasterLineComponent:

    def __init__(self, canvas):
        self._canvas = canvas
        self.plot_component = self._get_plaster()

    def _get_plaster(self):
        if self._canvas.options.getboolean('plaster-line-extend'):
            x_values = (0, self._canvas.get_page_dimensions()[0])
        else:
            x_values = self._canvas.get_plot_width_extent()
        plaster_line = ET.Element('line')
        plaster_line.set('x1', str(x_values[0]))
        plaster_line.set('x2', str(x_values[1]))
        plaster_line.set('y1', str(self._canvas.plaster))
        plaster_line.set('y2', str(self._canvas.plaster))
        plaster_line.set('stroke', 'black')
        plaster_line.set('stroke-width', str(self._canvas.options['line-weight-medium']))
        plaster_line.set('stroke-dasharray', self._canvas.options['plaster-line-dasharray'])
        return plaster_line


class BackgroundImageComponent:

    def __init__(self, canvas):
        self._canvas = canvas
        self.plot_component = self._get_plot_component()

    def _get_plot_component(self):
        svg_ns = {'ns0': 'http://www.w3.org/2000/svg'}
        image_file = os.path.expanduser(self._canvas.options['background-image'])
        image_tree = ET.parse(image_file)
        image_root = image_tree.getroot()
        image_group = image_root.find('ns0:g', svg_ns)
        image_group.set('transform', 'translate(' + str(self._canvas.centre) + ' ' +
                                     str(self._canvas.plaster) + ')' +
                                     'scale(' + str(self._canvas.rscale) + ') ')
        for path in image_group:
            path_class = path.get('class')
            if path.get('class') in reference.usitt_line_weights:
                weight = reference.usitt_line_weights[path_class]
            else:
                weight = 'line-weight-medium'
            path.set('stroke-width',
                     str(float(self._canvas.options[weight]) * self._canvas.scale))
            path.set('stroke', '#000000')
            path.set('fill-opacity', '0')

        return image_group


class PageBorderComponent:

    def __init__(self, canvas):
        self._canvas = canvas
        self.plot_component = self._get_plot_component()

    def _get_plot_component(self):
        margin = float(self._canvas.options['margin'])
        paper = self._canvas.get_page_dimensions()
        points = [(margin, margin), (paper[0] - margin, margin),
                  (paper[0] - margin, paper[1] - margin), (margin, paper[1] - margin)]
        border = ET.Element('polygon')
        border.set('points', ' '.join([','.join(map(str, i)) for i in points]))
        border.set('fill', 'white')
        border.set('stroke', 'black')
        border.set('stroke-width', self._canvas.options['line-weight-heavy'])
        return border


class PageMaskingComponent:

    def __init__(self, canvas):
        self._canvas = canvas
        self.plot_component = self._get_plot_component()

    def _get_plot_component(self):
        group = ET.Element('g')
        paper = self._canvas.get_page_dimensions()
        adj_margin = float(self._canvas.options['margin']) - float(self._canvas.options['line-weight-heavy']) / 2
        group.append(ET.Element('rect', attrib={'x': '0', 'y': '0', 'width': str(paper[0]),
                                                'height': str(adj_margin), 'fill': 'white'}))
        group.append(ET.Element('rect', attrib={'x': '0', 'y': '0', 'width': str(adj_margin),
                                                'height': str(paper[1]), 'fill': 'white'}))
        group.append(ET.Element('rect', attrib={'x': str(paper[0] - adj_margin), 'y': '0', 'width': str(adj_margin),
                                                'height': str(paper[1]), 'fill': 'white'}))
        group.append(ET.Element('rect', attrib={'x': '0', 'y': str(paper[1] - adj_margin), 'width': str(paper[0]),
                                                'height': str(adj_margin), 'fill': 'white'}))
        return group
