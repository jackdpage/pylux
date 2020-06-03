from pylux import interpreter, document
from pylux.lib import exception
from ast import literal_eval


class MessageBus:

    def __init__(self, config):
        self.config = config

    def post_feedback(self, lines):
        pass

    def post_output(self, lines, **kwargs):
        for l in lines:
            print(self.get_pretty_line(l))

    def get_pretty_line(self, l):
        if type(l) == str:
            return l
        s = ''
        for i in l:
            if type(i) == str:
                s += i
            elif type(i) == tuple:
                colour = self.config['fallback-colours'].get(i[0], '0')
                s = s + '\033[' + colour + 'm' + i[1] + '\033[m'
        return s


class Application:

    def __init__(self, init_globals):
        self.file = self.initialise_file(init_globals['FILE'])
        self.config = init_globals['CONFIG']
        self.message_bus = MessageBus(self.config)

    def initialise_file(self, f):
        s = document.get_string_from_file(f)
        d = document.get_deserialised_document_from_string(s)
        return d


def main(init_globals):

    def post_command(cmd):
        command_interpreter.process_command(cmd)

    app = Application(init_globals)
    command_interpreter = interpreter.Interpreter(app.file, app.message_bus, app.config)
    for ext in literal_eval(app.config['interpreter']['default-extensions']):
        try:
            command_interpreter.register_extension(ext)
        except (exception.DependencyError, ModuleNotFoundError):
            print('One or more dependencies for {0} were missing. Aborting load'.format(ext))
    while True:
        cmd = input('[pylux] ')
        post_command(cmd)
