import urwid
import cli_bridge
import document
from lib import printer


COMMAND_OBJECTS = {
    'a': 'All',
    'f': 'File',
    'g': 'Group',
    'm': 'Metadata',
    'q': 'Cue',
    'x': 'Fixture'
}
COMMAND_ACTIONS = {
    'c': 'CloneTo',
    'C': 'CompleteFrom',
    'd': 'Display',
    'g': 'Get',
    'G': 'GetAll',
    'n': 'Create',
    'N': 'CreateFrom',
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
            if self.edit_text:
                if self.edit_text[-1] in NUMERIC_KEYS:
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


class ApplicationView:

    def __init__(self, cmd):
        self.history = CommandHistory('Initialise')
        self.footer = urwid.Pile([self.history, cmd])
        self.list_walker = urwid.SimpleFocusListWalker([])
        self.sheet = urwid.ListBox(self.list_walker)

    def update_sheet(self, sheet_list):
        self.list_walker.clear()
        self.list_walker.extend(sheet_list)


class Application:

    def __init__(self, f, conf, post_function):
        self.file = self.initialise_file(f)
        self.config = conf['CONFIG']
        self.cmd = CommandLine(post_function)
        self.view = ApplicationView(self.cmd)
        self.update_context(self.config['curses']['default-context'])

    def initialise_file(self, f):
        s = document.get_string_from_file(f)
        d = document.get_deserialised_document_from_string(s)
        return d

    def _generate_sheet_list(self, context):
        text_widgets = []
        if context == 'All':
            context_objects = self.file
        else:
            context_objects = document.get_by_type(self.file, context.lower())
        for i in context_objects:
            string = printer.get_generic_text_widget(i)
            text_widgets.append(urwid.Text(string))
        return text_widgets

    def update_context(self, context):
        self.cmd.set_context(context)
        sheet_list = self._generate_sheet_list(context)
        self.view.update_sheet(sheet_list)


def main(config):

    def post_command(command):
        app.view.history.set_text(command)
        split_command = command.split()
        if not split_command:
            app.view.history.set_text('Empty command')
        elif split_command[0] == 'BRIDGE_DIRECT_MODE':
            app.view.history.set_text('Sending command to Pylux via Bridge Direct Mode')
            bridge.process_direct_command(command)
        elif split_command[0] == split_command[1] and split_command[0] in COMMAND_OBJECTS.values():
            app.update_context(split_command[0])
        else:
            bridge.process_new_syntax_command(command)

    bridge = cli_bridge.CliBridge(config)
    app = Application('f', config, post_command)
    loop = urwid.MainLoop(urwid.Frame(app.view.sheet, footer=app.view.footer))
    loop.run()
