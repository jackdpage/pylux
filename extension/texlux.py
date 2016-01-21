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

"""Generate LaTeX documentation.

TeXlux uses a Jinja2 template to generate documentation from the 
plot file in the LaTeX format, which can then be processed to create 
PDF files.
"""

from jinja2 import Environment, FileSystemLoader
import os
import plot
import clihelper


class Report:

    def __init__(self):
        self.environment = Environment(loader=FileSystemLoader('/usr/share/pylux/template'))

    def generate(self, template):
        template = self.environment.get_template(template)
        print(template.render(cues=sorted(plot.CueList(PLOT_FILE).cues, 
                                          key=lambda cue: cue.key)))


def main():
    while True:
        inputs = input('command').split(' ')
        if inputs[0] == 'dog':
            report = Report()
            report.generate(inputs[1]+'.tex')

if __name__ == 'pyext':
    main()
