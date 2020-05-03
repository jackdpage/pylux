from pylux import interpreter, document


class MessageBus:

    def post_feedback(self, lines):
        pass

    def post_output(self, lines):
        for l in lines:
            print(l)


class Application:

    def __init__(self, init_globals):
        self.file = self.initialise_file(init_globals['FILE'])
        self.config = init_globals['CONFIG']
        self.message_bus = MessageBus()

    def initialise_file(self, f):
        s = document.get_string_from_file(f)
        d = document.get_deserialised_document_from_string(s)
        return d


def main(init_globals):

    def post_command(cmd):
        command_interpreter.process_command(cmd)

    app = Application(init_globals)
    command_interpreter = interpreter.Interpreter(app.file, app.message_bus, app.config)
    command_interpreter.register_extension('base')
    command_interpreter.register_extension('eos')
    command_interpreter.register_extension('report')
    command_interpreter.register_extension('plot')
    while True:
        cmd = input('[pylux] ')
        post_command(cmd)
