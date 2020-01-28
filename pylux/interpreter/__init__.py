from pylux import clihelper, document
from pylux.lib import printer
from importlib import import_module


class RegularCommand:
    def __init__(self, syntax, function):
        self.trigger = syntax
        self.function = function
        # Parmeters are any function vars after the first one (refs) up to the number of arguments
        if function.__code__.co_argcount > 2:
            self.parameters = [i for i in function.__code__.co_varnames[2:function.__code__.co_argcount] if i]
        else:
            self.parameters = []


class InterpreterExtension:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.commands = []
        self.register_commands()

    def register_commands(self):
        pass

    def register_extension(self):
        for command in self.commands:
            self.interpreter.register_command(command)


class Interpreter:
    def __init__(self, file, message_bus, config):
        self.file = file
        self.msg = message_bus
        self.config = config
        self.commands = []
        self.triggers = {}

    def process_command(self, command):
        self.msg.post_feedback(command)
        keywords = command.split()
        obj = keywords[0]
        refs = keywords[1]
        if refs != 'All':
            refs = clihelper.resolve_references(keywords[1])
        action = keywords[2]
        trigger = (obj, action)
        if len(keywords) > 3:
            parameters = keywords[3:]
        else:
            parameters = []

        if trigger in self.triggers:
            command = self.triggers[trigger]
            # Find out how many parameters the command is expecting, if we have a different number to that, assume
            # that all over that amount are combined to one multi-word parameter
            n = len(command.parameters)
            if n != 0:
                args = []
                for i in range(0, n-1):
                    args.append(parameters[i])
                args.append(' '.join(parameters[(n-1):]))
            else:
                args = []
            self.triggers[trigger].function(refs, *args)

        if action == 'Display' and refs == 'All':
            self.display_all(obj)

    def register_command(self, command):
        self.commands.append(command)
        self.triggers[command.trigger] = command

    def register_extension(self, name, pkg='pylux.interpreter'):
        module = import_module('.'+name, pkg)
        module.register_extension(self)

    def display_all(self, obj):
        lines = []
        if obj == 'All':
            objects = self.file
        else:
            objects = document.get_by_type(self.file, obj.lower())
        for i in objects:
            s = printer.get_generic_text_widget(i)
            lines.append(s)
        self.msg.post_output(lines)
