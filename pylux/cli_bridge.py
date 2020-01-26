# This file essentially runs a non-interactive version of the old cli.py file to act as a bridge between the new
# CLI command structure and the old functions

from pylux.context import editor


MAPPINGS = {
    'Fixture All Display ': ['xl']
}


class CliBridge:

    def __init__(self, global_params):
        self.context = editor.get_context()
        self.context.set_globals(global_params)

    def process_direct_command(self, command):
        inputs = command.split()
        del inputs[0]
        self.context.process(inputs)

    def process_new_syntax_command(self, command):
        if command in MAPPINGS:
            self.context.process(MAPPINGS[command])

    def send_inputs(self, inputs):
        self.context.process(inputs)
