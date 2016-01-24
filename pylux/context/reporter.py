# reporter.py is part of Pylux
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

"""Generate text reports from Jinja templates.

Reporter uses a Jinja2 template to generate documentation from the 
plot file. It was made primarily for LaTeX documentation but could 
just as easily be used for other formats.
"""

from jinja2 import Environment, FileSystemLoader
import os
import pylux.plot as plot
import pylux.clihelper as clihelper
from pylux import get_data
from pylux.context.context import Context


class Report:

    def __init__(self, plot_file):
        self.environment = Environment(lstrip_blocks=True, trim_blocks=True, 
                                loader=FileSystemLoader(get_data('template/')))
        self.plot_file = plot_file

    def find_template(self, template):
        all_templates = os.listdir(get_data('template'))
        discovered = {}
        for template_file in all_templates:
            if template_file.split('.')[0] == template:
                discovered[template_file.split('.')[1]] = template_file
        return discovered
        

    def generate(self, template):
        template = self.environment.get_template(template)
        cue_list = sorted(plot.CueList(self.plot_file).cues,
                          key=lambda cue: cue.key)
        fixture_list = plot.FixtureList(self.plot_file).fixtures
        metadata_list = plot.Metadata(self.plot_file).meta
        self.content = template.render(cues=cue_list, fixtures=fixture_list,
                                       meta=metadata_list)


class ReporterContext(Context):

    def __init__(self):
        self.name = 'reporter'
        self.init_commands()
        self.register('rn', self.report_new, 1)
        self.register('rg', self.report_get, 1)
        self.register('rw', self.report_write, 1)

    def report_new(self, parsed_input):
        self.report = Report(self.plot_file)
        possible_templates = self.report.find_template(parsed_input[0])
        if len(possible_templates) == 0:
            print('Error: No templates with that name')
        elif len(possible_templates) == 1:
            self.report.generate(possible_templates.iteritems()[0])
        else:
            print('The template you entered has '+
                  str(len(possible_templates))+' matches: ')
            print(possible_templates)
            using_template = input('Choose an extension to continue: ')
            self.report.generate(possible_templates[using_template])
            
    def report_get(self, parsed_input):
        print(self.report.content)

    def report_write(self, parsed_input):
        with open(os.path.expanduser(parsed_input[0]), 'w') as outfile:
            outfile.write(self.report.content)


def get_context():
    return ReporterContext()
