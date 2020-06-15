from ast import literal_eval
import urwid
from pylux import document
from pylux.lib import autocomplete, printer, exception
import sys


NUMERIC_KEYS = [str(i) for i in range(0, 10)]


class CommandLine(urwid.Edit):
    def __init__(self, config):
        super(CommandLine, self).__init__()
        self.context = ''
        self.config = config
        self.command_handler = None
        self.keymapper = None

    def bind(self, command_interpreter, command_handler):
        """Attaches the command line to the interpreter and handler function. Now the
        keymapper can be initialised as it relies on access to the interpreter."""
        self.command_handler = command_handler
        self.keymapper = autocomplete.Keymapper(command_interpreter, self.config)

    def post_command(self, command):
        self.command_handler(command)

    def set_context(self, context):
        self.context = context
        self.update_caption()

    def enable_autocomplete(self):
        self.keymapper.enable()
        self.update_caption()

    def disable_autocomplete(self):
        self.keymapper.disable()
        self.update_caption()

    def toggle_autocomplete(self):
        self.keymapper.toggle()
        self.update_caption()

    def update_caption(self):
        if self.keymapper:
            if self.keymapper.enabled:
                self.set_caption('A ('+self.context+') ')
            else:
                self.set_caption('X ('+self.context+') ')
        else:
            self.set_caption('N (' + self.context + ') ')

    def keypress(self, size, key):
        if key == 'enter':
            self.post_command(self.edit_text)
            self.set_edit_text('')
            self.enable_autocomplete()
        elif key == self.config['cli']['autocomplete-toggle-key']:
            self.toggle_autocomplete()
        elif self.keymapper.enabled:
            self.keypress_autocomplete(size, key)
        else:
            return super(CommandLine, self).keypress(size, key)

    def keypress_autocomplete(self, size, key):
        if not self.edit_text.split():
            if key in [str(i) for i in range(0, 10)]:
                self.insert_text(self.context+' ')
        keymap = self.keymapper.get_keymap(self.edit_text)
        if keymap:
            if key in keymap:
                return super(CommandLine, self).insert_text(keymap[key])
            else:
                return super(CommandLine, self).keypress(size, key)
        else:
            return super(CommandLine, self).keypress(size, key)


class CommandHistory(urwid.Text):

    def __init__(self, markup):
        super(CommandHistory, self).__init__(markup)
        self.history = []

    def add_to_history(self, text):
        self.history.append(text)
        self.set_text(text)


class MessageBus:

    def __init__(self, history, output_pane, config):
        self.history = history
        self.output = output_pane
        self.config = config
        self.clear_flag = False

    def post_feedback(self, lines):
        self.history.add_to_history(lines)

    def clear_output(self):
        self.clear_flag = True

    def post_output(self, lines, indentation=0, **kwargs):
        indentation_str = ' ' * indentation * int(self.config['cli']['indentation-amount'])
        if self.clear_flag:
            self.output.clear()
            self.clear_flag = False
        for l in lines:
            if type(l) == list:
                l.insert(0, indentation_str)
            elif type(l) == str:
                l = indentation_str + l
            self.output.append(urwid.Text(l))


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


class Application:

    def __init__(self, interpreter):
        self.file = interpreter.file
        self.config = interpreter.config
        self.cmd = CommandLine(self.config)
        self.view = ApplicationView(self.cmd)
        self.message_bus = MessageBus(self.view.history, self.view.dynamic_walker, self.config)

    def bind(self, command_interpreter, post_function):
        self.cmd.bind(command_interpreter, post_function)
        self.update_context(self.config['cli']['default-context'])

    def _generate_sheet_list(self, context):
        text_widgets = []
        if context in document.COMMAND_STR_MAP:
            context_objects = self.file.get_by_type(
                document.COMMAND_STR_MAP[context]
            )
        else:
            context_objects = []
        for obj in context_objects:
            text_widgets.append(urwid.Text(obj.get_text_widget()))
        return text_widgets

    def _generate_history_list(self):
        text_widgets = []
        for i in self.message_bus.history.history:
            text_widgets.append(urwid.Text(i))
        return text_widgets

    def update_context(self, context):
        self.cmd.set_context(context)
        sheet_list = self._generate_sheet_list(context)
        self.view.update_sheet(sheet_list)

    def update_view(self):
        self.view.update_sheet(self._generate_sheet_list(self.cmd.context))

    def display_history(self):
        self.view.update_sheet(self._generate_history_list())


def main(interpreter):

    def post_command(command):
        split_command = command.split()
        if not split_command:
            app.view.history.set_text('Empty command')
        elif split_command == ['CommandHistory']:
            app.display_history()
        elif len(split_command) == 1:
            interpreter.process_command(command)
        elif (split_command[0] == split_command[1] and len(split_command) == 2):
            app.update_context(split_command[0])
        else:
            app.message_bus.clear_output()
            interpreter.process_command(command)
            app.update_view()

    def generate_palette():
        palette = []
        conf_options = app.config['cli-colours']
        for c in conf_options:
            palette.append((c, conf_options[c], 'default', 'bold'))
        return palette

    app = Application(interpreter)
    interpreter.subscribe_client(app.message_bus)
    app.bind(interpreter, post_command)
    palette = generate_palette()
    loop = urwid.MainLoop(urwid.Frame(app.view.main_content, footer=app.view.footer), palette)
    try:
        loop.run()
    except exception.ProgramExit:
        sys.exit()
