#!/usr/bin/python3

# genlux.py is part of Pylux
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

import xml.etree.ElementTree as ET
import uuid
import argparse
import os
import configparser
import os.path
import sys
import plotter


def main():
    PROJECT_FILE = plotter.FileManager()
    PROJECT_FILE.load(plotter.LAUNCH_ARGS.file)
    META = plotter.MetaManager(PROJECT_FILE)
    FIXTURES = PROJECT_FILE.root.find('fixtures')
    
    # LaTeX stuff that is needed before any customisation
    latex_header = ('\\documentclass{genlux}\n'
                    '\\def\\tab{\\hspace*{3ex}}\n'
                    '\\begin{document}\n'
                    '\\hfil{\\Huge\\bf Pylux Dimmer Report}\\hfill\n'
                    '\\bigskip\\break\n'
                    '\\hrule\n')
    # A list of the meta fields included in the header
    document_header_items = [('Production', 'production'),
                             ('Designer', 'designer'),
                             ('Venue', 'venue'),
                             ('Board Operator', 'board_operator'),
                             ('Director', 'director'),
                             ('Followspot Operator', 'spot_operator')]
    # For each meta, check if it has a value, then add to LaTeX output
    document_header = ""
    side = True
    for header_item in document_header_items:
        if META.get(header_item[1]) != None:
            document_header = (document_header+'{\\bf '+header_item[0]+
                               ': } '+META.get(header_item[1]))
            if side == True:
                document_header = document_header+' \\hfill '
            elif side == False:
                document_header = document_header+' \\\\\n'
            side = not side
    # Generate the dimmer report section
    dimmer_report = '\\begin{reportTable}\n\n'
    # this is hard coded at the moment because the infrastructure does not
    # exist in plotter.py
    dimmer_report = dimmer_report+'\\dimmer{1}\n\n'
    for fixture in FIXTURES:
        uuid = fixture.get('uuid')
        olid = fixture.get('olid')
        try:
            dmx = fixture.find('dmx_start_address').text
        except AttributeError:
            dmx = None
            print('% Couldn\'t get DMX start address for '+uuid)
        try:
            circuit = fixture.find('circuit').text
        except AttributeError:
            circuit = None
            print('% Couldn\'t get circuit number for '+uuid)
        try:
            power = fixture.find('power').text
        except AttributeError:
            power = '0'
            print('% Couldn\'t get power for '+uuid+', using zero instead')
        dimmer_report = (dimmer_report+'\\fixture{'+olid+'}{'+str(dmx)+
                         '}{'+str(circuit)+'}{'+power+'}\n')
    # LaTeX stuff that ends it all off
    latex_footer = '\\end{reportTable}\n\\end{document}' 
    print(latex_header+document_header+dimmer_report+latex_footer)

if __name__ == '__main__':
    main()
