import urwid
import cli_bridge


COMMAND_OBJECTS = {
    'f': 'File',
    'q': 'Cue',
    'x': 'Fixture'
}
COMMAND_ACTIONS = {
    'c': 'Create',
    'g': 'Get',
    'G': 'GetAll',
    'r': 'Remove',
    's': 'Set'
}
NUMERIC_KEYS = [str(i) for i in range(0, 10)]


class CommandLine(urwid.Edit):
    def __init__(self, command_handler):
        super(CommandLine, self).__init__()
        self.context = ''
        self.autocomplete = True
        self.command_handler = command_handler

    def post_command(self, command):
        self.command_handler(command)

    def set_context(self, context):
        self.context = context
        self.update_caption()

    def enable_autocomplete(self):
        self.autocomplete = True
        self.update_caption()

    def disable_autocomplete(self):
        self.autocomplete = False
        self.update_caption()

    def update_caption(self):
        if self.autocomplete:
            self.set_caption('A ('+self.context+') ')
        else:
            self.set_caption('X ('+self.context+') ')

    def keypress(self, size, key):
        if key == 'enter':
            self.post_command(self.edit_text)
            self.set_edit_text('')
            self.enable_autocomplete()
        elif key == 'B':
            self.disable_autocomplete()
            self.insert_text('BRIDGE_DIRECT_MODE ')
        elif self.autocomplete:
            self.keypress_autocomplete(size, key)
        else:
            return super(CommandLine, self).keypress(size, key)

    def keypress_autocomplete(self, size, key):
        if key in NUMERIC_KEYS and self.edit_text == '':
            return super(CommandLine, self).insert_text(self.context + ' ' + key)
        elif key in COMMAND_OBJECTS:
            if self.edit_text == '':
                self.set_context(COMMAND_OBJECTS[key])
            elif self.edit_text[-1] in NUMERIC_KEYS:
                self.insert_text(' ')
            return super(CommandLine, self).insert_text(COMMAND_OBJECTS[key] + ' ')
        elif key in COMMAND_ACTIONS:
            if self.edit_text != '':
                if self.edit_text[-1] in NUMERIC_KEYS:
                    self.insert_text(' ')
            self.disable_autocomplete()
            return super(CommandLine, self).insert_text(COMMAND_ACTIONS[key] + ' ')
        else:
            return super(CommandLine, self).keypress(size, key)


class CommandHistory(urwid.Text):
    pass


def main(init_globals):

    def post_command(command):
        if 'BRIDGE_DIRECT_MODE' in command:
            command_history.set_text('Sending command to Pylux via Bridge Direct Mode')
            bridge.process_direct_command(command)
        else:
            command_history.set_text(command)

    bridge = cli_bridge.CliBridge(init_globals)

    command_line = CommandLine(post_command)
    command_line.set_context('Fixture')
    command_history = CommandHistory('Launch Program')
    command_pile = urwid.Pile([command_history, command_line])
    loop = urwid.MainLoop(urwid.Frame(urwid.SolidFill(' '), footer=command_pile))
    loop.run()
