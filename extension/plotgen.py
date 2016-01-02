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


class ImagePlot:

    def __init__(self, plot_file):    
        self.fixtures = plot.FixtureList(plot_file)

    def create_plot(self):
        image_plot = ET.Element('svg')
        for fixture in self.fixtures.fixtures:
            symbol_file = '/usr/share/pylux/symbol/'+fixture.olid+'.svg'
            symbol_tree = ET.parse(symbol_file)
            symbol_root = symbol_tree.getroot()
            symbol_image = symbol_root.find('g')
            locationX = float(fixture.data['posX'])*1000
            locationY = float(fixture.data['posY'])*1000
            rotation = math.degrees(float(fixture.data['rotation']))
            symbol_image.set('transform', 'rotate('+str(rotation)+') translate('+str(locationX)+' '+str(locationY)+')')
            image_plot.append(symbol_image)
        return image_plot


def run_pylux_extension(plot_file):
    plot = ImagePlot(plot_file)
    image = plot.create_plot()
    output_tree = ET.ElementTree(image)
    output_tree.write('/home/jack/Projects/pylux/tests/imagetest.svg')
