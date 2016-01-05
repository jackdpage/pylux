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
            symbol_name = fixture.data['symbol']
            posX = fixture.data['posX']
            posY = fixture.data['posY']
            rotation = fixture.data['rotation']
            colour = fixture.data['colour']
            symbol = plot.FixtureSymbol('/usr/share/pylux/symbol/'+
                symbol_name+'.svg')
            symbol.prepare(posX, posY, rotation, colour)
            image_plot.append(symbol.image_group)
        return image_plot


def run_pylux_extension(plot_file):
    plot = ImagePlot(plot_file)
    image = plot.create_plot()
    output_tree = ET.ElementTree(image)
    output_tree.write('/home/jack/Projects/pylux/tests/imagetest.svg')
