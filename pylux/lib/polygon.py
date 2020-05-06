import xml.etree.ElementTree as ET
import math


def generate_polygon(r, n):
    """Create n-sided polygon to fit in circle radius r, centre 0,0."""
    if n == 0:
        return generate_circle(r)
    elif n == 4:
        return generate_tetragon(r)
    elif n == 6:
        return generate_hexagon(r)
    else:
        raise Exception('cant do that bye')


def generate_circle(r):
    shape = ET.Element('circle')
    shape.set('r', str(r))
    shape.set('cx', '0')
    shape.set('cy', '0')
    return shape


def generate_tetragon(r):
    shape = ET.Element('rect')
    shape.set('width', str(math.sqrt(2) * r))
    shape.set('height', str(math.sqrt(2) * r))
    shape.set('x', str(math.sqrt(2) * -0.5 * r))
    shape.set('y', str(math.sqrt(2) * -0.5 * r))
    return shape


def generate_hexagon(r):
    shape = ET.Element('polygon')
    points = [
        (-r, 0),
        (-r * 0.5, r * math.cos(math.pi / 6)),
        (r * 0.5, r * math.cos(math.pi / 6)),
        (r, 0),
        (r * 0.5, -r * math.cos(math.pi / 6)),
        (-r * 0.5, -r * math.cos(math.pi / 6))
    ]
    points_str = ' '.join([','.join(map(str, i)) for i in points])
    shape.set('points', points_str)
    return shape
