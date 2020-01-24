# This file essentially runs a non-interactive version of the old cli.py file to act as a bridge between the new
# CLI command structure and the old functions

import context.editor


class CliBridge:

    def __init__(self, global_params):
        self.context = context.editor.get_context()
        self.context.set_globals(global_params)

    def process_direct_command(self, command):
        inputs = command.split()
        del inputs[0]
        self.context.process(inputs)
