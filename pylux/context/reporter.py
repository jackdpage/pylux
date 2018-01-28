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
from jinja2.exceptions import TemplateSyntaxError
import os
from lib import data, tagger
from context.context import Context, Command
import document

class Report:

    def __init__(self, plot_file):
        print(data.list_data('template/'))
        self.environment = Environment(lstrip_blocks=True, trim_blocks=True, 
                                loader=FileSystemLoader(os.path.normpath(os.path.expanduser('~/Documents/GitHub/pylux/pylux/content/template'))))
        self.plot_file = plot_file

    def generate(self, template, options):
        """Generate a report.

        Args
            template: full name, including extension of the template
            options: dict of options
        """
        def is_hung(fixture):
            return True if 'pos' in fixture else False

        def is_dimmer(fixture):
            if 'is_dimmer' in fixture.data:
                if fixture.data['is_dimmer'] == 'True':
                    return True
                else:
                    return False
            else:
                return False

        template = self.environment.get_template(template)
        # Create cues list
        cues = document.get_by_type(self.plot_file, 'cue')
        # Create fixtures list
        fixtures = document.get_by_type(self.plot_file, 'fixture')
        for fixture in fixtures:
            tagger.tag_fixture_all(fixture)
        fixture_list = sorted(fixtures, key=lambda fix: int(fix['ref']))
        # Create hung fixtures list
        hung_fixtures = []
        for fixture in fixture_list:
            if is_hung(fixture):
                hung_fixtures.append(fixture)
        hung_fixtures.sort(key=lambda fix: int(fix['ref']))
        # Create metadata list
        metadata = {i['metadata-key']: i['metadata-value'] for i in document.get_by_type(self.plot_file, 'metadata')}
        # Render template
        self.content = template.render(cues=cues, fixtures=fixture_list,
                                       metadata=metadata, hung=hung_fixtures,
                                       options=options)

class ReporterContext(Context):

    def __init__(self):
        self.name = 'reporter'
        super().__init__()

        self.templates = []

        self.register(Command('rg', self.report_generate, [
            ('template', True, 'The Jinja template to create a report from.'), 
            ('options', False, 'Optional arguments the template offers.')]))
        self.register(Command('rd', self.report_dump, [])) 
        self.register(Command('rw', self.report_write, [
            ('path', True, 'The path to write the file to.')]))
        
        self.register(Command('tl', self.template_list, []))

    def post_init(self):
        pass

####
#template list
#report generate
#report dump
#report write (to file)
#report list
####

    def template_list(self, parsed_input):
        '''List the templates installed on this system.'''
        self.interface.open('TMP')
        templates = data.list_data('template')
        for template in templates:
            s = template[1]+' ('+template[0]+')'
            self.templates.append((s, template, 'TMP'))

    def report_generate(self, parsed_input):
        '''Create a new report from a template in a temporary buffer.'''

        def get_options(parsed_input):
            if len(parsed_input) > 1:
                options = {}
                options_input = parsed_input[1].split(';')
                for option in options_input:
                    option_name = option.split('=')[0]
                    option_values = option.split('=')[1].split(',')
                    options[option.split('=')[0]] = option.split('=')[1]
                return options

        self.report = Report(self.plot_file)
        options = get_options(parsed_input)
        template = parsed_input[0]
        if template != None:
            try:
                self.report.generate(template, options)
            except TemplateSyntaxError:
                self.log(30, 'Template not configured properly.')

    def report_dump(self, parsed_input):
        '''Print the contents of the report buffer.'''
        print(self.report.content)

    def report_write(self, parsed_input):
        '''Save the report buffer to a file.'''
        with open(os.path.expanduser(parsed_input[0]), 'w') as outfile:
            outfile.write(self.report.content)


def get_context():
    return ReporterContext()
