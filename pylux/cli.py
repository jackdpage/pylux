import urwid
from pylux import cli_bridge, document, interpreter
from pylux.lib import printer


COMMAND_OBJECTS = {
    'a': 'All',
    'f': 'File',
    'g': 'Group',
    'm': 'Metadata',
    'q': 'Cue',
    'r': 'Registry',
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
PALETTE = [
    ('cue', 'light cyan', 'black', 'bold'),
    ('fixture', 'light green', 'black', 'bold'),
    ('group', 'light magenta', 'black', 'bold'),
    ('metadata', 'light blue', 'black', 'bold'),
    ('registry', 'yellow', 'black', 'bold'),
    ('unlabelled', 'dark red', 'black')
]


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
        self.history = CommandHistory('Application Initialise')
        self.footer = urwid.Pile([self.history, cmd])
        self.fixed_walker = urwid.SimpleFocusListWalker([])
        self.dynamic_walker = urwid.SimpleFocusListWalker([])
        dynamic_sheet = urwid.ListBox(self.dynamic_walker)
        fixed_sheet = urwid.ListBox(self.fixed_walker)
        self.main_content = urwid.Columns([fixed_sheet, dynamic_sheet])

    def update_sheet(self, sheet_list):
        self.fixed_walker.clear()
        self.fixed_walker.extend(sheet_list)

    def update_dynamic_content(self, widget_list):
        self.dynamic_walker.clear()
        self.dynamic_walker.extend(widget_list)


class Application:

    def __init__(self, init_globals, post_function):
        self.file = self.initialise_file(init_globals['FILE'])
        self.config = init_globals['CONFIG']
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


def main(init_globals):

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
            dynamic_output = command_interpreter.process_command(command)
            app.view.update_dynamic_content(dynamic_output)

    bridge = cli_bridge.CliBridge(init_globals)
    app = Application(init_globals, post_command)
    command_interpreter = interpreter.Interpreter(app.file)
    loop = urwid.MainLoop(urwid.Frame(app.view.main_content, footer=app.view.footer), PALETTE)
    loop.run()
