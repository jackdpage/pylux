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

import os
import plot
import clihelper

class Report:
    """Create a LaTeX report."""

    def __init__(self, title, plot_file, template):
        self.plot_file = plot_file
        self.meta = plot.Metadata(self.plot_file)
        self.fixtures = plot.FixtureList(self.plot_file)
        self.title = title
        self.template = template

    def generate_header(self):
        self.header = ('\\documentclass{'+self.template+'}\n'
            '\\def\\tab{\\hspace*{3ex}}\n'
            '\\begin{document}\n'
            '\\hfil{\\Huge\\bf '+self.title+'}\\hfill\n'
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
            try:
                self.header = (self.header+'{\\bf '+
                    header_item[0]+': } '+self.meta.meta[header_item[1]])
                if side == True:
                    self.header = self.header+' \\hfill '
                elif side == False:
                    self.header = self.header+' \\\\\n'
                side = not side
            except KeyError:
                print('No meta value for '+header_item[1])

    def generate_dimmer_report(self):
        self.report = '\\begin{reportTable}\n\n'
        no_dimmer = []

        def add_fixture(fixture):
            uuid = fixture.uuid
            olid = fixture.olid
            try:
                fix_type = fixture.data['type']
            except KeyError:
                fix_type = olid
                print('Couldn\'t get fixture type for '+uuid)
            try:
                dmx = fixture.data['dmx_start_address']
            except KeyError:
                dmx = None
                print('Couldn\'t get DMX start address for '+uuid)
            try:
                circuit = fixture.data['circuit']
            except KeyError:
                circuit = None
                print('Couldn\'t get circuit number for '+uuid)
            try:
                power = fixture.data['power']
            except KeyError:
                power = '0'
                print('Couldn\'t get power for '+uuid+', using zero instead')
            self.report = (self.report+'\\fixture{'+fix_type+'}{'+str(dmx)+'}{'+
                str(circuit)+'}{'+power+'}\n')

        for fixture in self.fixtures.fixtures:
            if 'dimmer' not in fixture.data:
                no_dimmer.append(fixture)

        dimmer_list = self.fixtures.get_data_values('dimmer')
        if len(dimmer_list) == 0:
            print('You\'re not using any dimmers, why are you trying to '
                'create a dimmer report?')
        for dimmer in dimmer_list:
            self.report = self.report+'\\dimmer{'+dimmer+'}\n\n'
            for fixture in self.fixtures.fixtures:
                try:
                    if fixture.data['dimmer'] == dimmer:
                        add_fixture(fixture)
                except KeyError:
                    pass
            self.report = self.report+'\\subtotal\n\n'
        no_dimmer = list(set(no_dimmer))
        if len(no_dimmer) > 0:
            print(str(len(no_dimmer))+' fixtures with no dimmer')
            self.report = self.report+'\\dimmer{None}\n\n'
            for fixture in no_dimmer:
                add_fixture(fixture)

    def generate_footer(self):
        self.footer = '\\end{reportTable}\n\\end{document}'

def run_pylux_extension(plot_file):
    prompt = '(pylux:texlux) ' 
    while True:
        user_input = input(prompt)
        inputs = []
        for i in user_input.split(' '):
            inputs.append(i)
        
        if inputs[0] == 'rn':
            report = Report(clihelper.resolve_input(inputs, 3)[-1],
                 plot_file, inputs[1])
            report.generate_header()
            report.generate_dimmer_report()
            report.generate_footer()
            with open(os.path.expanduser(inputs[2]), 'w') as output_file:
                output_file.write(report.header)
                output_file.write(report.report)
                output_file.write(report.footer)

        elif inputs[0] == '::' or inputs[0] == 'q':
            break

        else:
            print('That command doesn\'t exist!')
