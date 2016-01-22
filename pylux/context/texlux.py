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

"""Generate LaTeX documentation.

TeXlux uses a Jinja2 template to generate documentation from the 
plot file in the LaTeX format, which can then be processed to create 
PDF files.
"""

from jinja2 import Environment, FileSystemLoader
import os
import pylux.plot as plot
import pylux.clihelper as clihelper
from pylux import get_data


class Report:

    def __init__(self):
        self.environment = Environment(loader=FileSystemLoader(get_data('template')))

    def generate(self, template):
        template = self.environment.get_template(template)
        cue_list = sorted(plot.CueList(GLOBALS['PLOT_FILE']).cues,
                          key=lambda cue: cue.key)
        fixture_list = plot.FixtureList(GLOBALS['PLOT_FILE']).fixtures
        self.content = template.render(cues=cue_list, fixtures=fixture_list)


def process_input(inputs):
    functions_dict = {
        'rn': report_new,
        'rN': report_new_print,
        'rw': report_write}

    

    if inputs[0] == 'rn':
        report = Report()
        report.generate(inputs[1]+'.tex')
        print('Report saved internally, ready to save to file.')

    if inputs[0] == '


def set_globals(globals_dict):
    global GLOBALS
    GLOBALS = globals_dict
