from pylux.interpreter import InterpreterExtension, RegularCommand, NoRefsCommand, Noun, Verb
from pylux import document, clihelper
from pylux.lib import tagger, data
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateSyntaxError
import os.path


class Report:

    def __init__(self, file):
        self.environment = Environment(lstrip_blocks=True, trim_blocks=True,
                                       loader=FileSystemLoader([i+'/template' for i in data.LOCATIONS.values()]))
        self.file = file
        self.content = None

    def generate(self, template, options):
        """Generate a report.

        Args
            template: full name, including extension of the template
            options: dict of options
        """
        def is_hung(f):
            return True if 'posX' in f.data and 'posY' in f.data else False

        template = self.environment.get_template(template)

        fixtures = [i for i in self.file.get_by_type(document.Fixture)]
        for fixture in fixtures:
            tagger.tag_fixture_all(self.file, fixture)
        fixtures = clihelper.refsort(fixtures)
        hung_fixtures = [i for i in fixtures if is_hung(i)]
        # Render template
        self.content = template.render(cues=self.file.get_by_type(document.Cue), fixtures=fixtures,
                                       metadata=self.file.metadata, hung=hung_fixtures,
                                       options=options)


class ReportExtension(InterpreterExtension):

    def __init__(self, interpreter):
        super().__init__(interpreter)
        self.report = None

    def register_commands(self):
        self.commands.append(NoRefsCommand((Noun.REPORT, Verb.CREATE), self.report_create))
        self.commands.append(NoRefsCommand((Noun.REPORT, Verb.WRITE), self.report_write))

    def report_create(self, template, options=''):

        def get_options(user_input):
            option_dict = {}
            if len(user_input) > 1:
                for option in user_input[1].split(';'):
                    option_dict[option.split('=')[0]] = option.split('=')[1]
            return option_dict

        self.report = Report(self.file)
        if template:
            try:
                self.report.generate(template, get_options(options))
            except TemplateSyntaxError:
                self.interpreter.msg.post_feedback(['Error: Report template not configured properly'])

    def report_write(self, path):
        if self.report:
            with open(os.path.expanduser(path), 'w') as f:
                f.write(self.report.content)


def register_extension(interpreter):
    ReportExtension(interpreter).register_extension()
