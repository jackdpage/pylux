#!/usr/bin/python3

# texlux.py is part of Pylux
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
from __init__ import __version__


def init():
    """Initialise the argument and config parsers."""
    # Initiate the argument parser
    parser = argparse.ArgumentParser(prog='texlux',
       description='Generate LaTeX reports from Pylux plots')
    parser.add_argument('-v', '--version', action='version', 
        version='%(prog)s '+__version__)
    parser.add_argument('file', help='Pylux plot file to process') 
    parser.add_argument('template', help='LaTeX template to use')
    parser.add_argument('-t', '--title', dest='title', 
        help='title for the document', default='Pylux Report')
    global LAUNCH_ARGS
    LAUNCH_ARGS = parser.parse_args()


class Report:
    """Create a LaTeX report."""

    def __init__(self, title, project_file, template):
        self.file = project_file
        self.meta = plotter.MetaManager(self.file)
        self.fixtures = self.file.root.find('fixtures')
        self.title = title
        self.template = template

    def generate_header(self):
        self.header = ('\\documentclass{'+self.template+'}\n'
            '\\def\\tab{\\hspace*{3ex}}\n'
            '\\begin{document}\n'
            '\\hfil{\\Huge\\bf '+LAUNCH_ARGS.title+'}\\hfill\n'
            '\\bigskip\\break\n'
            '\\hrule\n')
        document_header_items = [('Production', 'production'),
                                 ('Designer', 'designer'),
                                 ('Venue', 'venue'),
                                 ('Board Operator', 'board_operator'),
                                 ('Director', 'director'),
                                 ('Followspot Operator', 'spot_operator')]
        side = True
        for header_item in document_header_items:
            if self.meta.get(header_item[1]) != None:
                self.header = (self.header+'{\\bf '+
                    header_item[0]+': } '+self.meta.get(header_item[1]))
                if side == True:
                    self.header = self.header+' \\hfill '
                elif side == False:
                    self.header = self.header+' \\\\\n'
                side = not side

    def generate_dimmer_report(self):
        self.report = '\\begin{reportTable}\n\n'
        no_dimmer = []

        def add_fixture(fixture):
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
            self.report = (self.report+'\\fixture{'+olid+'}{'+str(dmx)+'}{'+
                str(circuit)+'}{'+power+'}\n')

        dimmer_list = plotter.get_data_list(self.file, 'dimmer')
        if len(dimmer_list) == 0:
            print('You\'re not using any dimmers, why are you trying to '
                'create a dimmer report?')
            sys.exit()
        for dimmer in plotter.get_data_list(self.file, 'dimmer'):
            self.report = self.report+'\\dimmer{'+dimmer+'}\n\n'
            for fixture in self.fixtures:
                try:
                    if fixture.find('dimmer').text == dimmer:
                        add_fixture(fixture)
                except AttributeError:
                    no_dimmer.append(fixture)
            self.report = self.report+'\\subtotal\n\n'
        no_dimmer = list(set(no_dimmer))
        if len(no_dimmer) < 0:
            print('% '+str(len(no_dimmer))+' fixtures with no dimmer')
            self.report = self.report+'\\dimmer{None}\n\n'
            for fixture in no_dimmer:
                add_fixture(fixture)

    def generate_footer(self):
        self.footer = '\\end{reportTable}\n\\end{document}'

def main():
    init()
    PROJECT_FILE = plotter.FileManager()
    PROJECT_FILE.load(LAUNCH_ARGS.file)
    output = Report(LAUNCH_ARGS.title, PROJECT_FILE, LAUNCH_ARGS.template)
    output.generate_header()
    report_templates = {'dimmer': output.generate_dimmer_report}
    try:
        report_templates[LAUNCH_ARGS.template]()
    except KeyError:
        print('No template with that name found, exiting...')
        sys.exit()
    output.generate_footer()
    print(output.header+output.report+output.footer)

if __name__ == '__main__':
    main()
