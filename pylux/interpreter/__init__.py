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


class NoRefsCommand:
    def __init__(self, syntax, function):
        self.trigger = syntax
        self.function = function
        # This is the same as the RegularCommand, except we are expecting one fewer arguments due to the lack of refs
        if function.__code__.co_argcount > 1:
            self.parameters = [i for i in function.__code__.co_varnames[1:function.__code__.co_argcount] if i]
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
        self.noref_triggers = {}

    def command_failed(self, posted_command):
        self.msg.post_feedback(['Error: Invalid command '+posted_command])

    def process_command(self, posted_command):

        def calculate_params(n, params):
            """Based on the command given, determine how many parameters are expected. Then shrink the number of
            parameters we were given on the command line to this number. This is done by combining all end
            parameters into one multi-word parameter with spaces."""
            if n != 0:
                args = []
                for i in range(0, n - 1):
                    args.append(params[i])
                args.append(' '.join(params[(n - 1):]))
            else:
                args = []
            return args

        self.msg.post_feedback(posted_command)
        keywords = posted_command.split()
        if len(keywords) < 2:
            self.command_failed(posted_command)
        else:
            obj = keywords[0]

            # If the first two keywords are in noref_triggers then this is a command with no references
            if (obj, keywords[1]) in self.noref_triggers:
                action = keywords[1]
                trigger = (obj, action)
                if len(keywords) > 2:
                    parameters = keywords[2:]
                else:
                    parameters = []
                command = self.noref_triggers[trigger]
                args = calculate_params(len(command.parameters), parameters)
                command.function(*args)

            # If the first and third keywords are in triggers, then the second keyword will be the references
            elif len(keywords) > 2:
                if (obj, keywords[2]) in self.triggers:
                    refs = keywords[1]
                    action = keywords[2]
                    trigger = (obj, action)
                    if refs != 'All':
                        refs = clihelper.safe_resolve_dec_references(self.file, obj.lower(), keywords[1])
                    else:
                        refs = [i['ref'] for i in document.get_by_type(self.file, obj.lower())]
                    if len(keywords) > 3:
                        parameters = keywords[3:]
                    else:
                        parameters = []
                    command = self.triggers[trigger]
                    args = calculate_params(len(command.parameters), parameters)
                    command.function(refs, *args)
                else:
                    self.command_failed(posted_command)

            # Otherwise, the command doesn't exist
            else:
                self.command_failed(posted_command)

    def register_command(self, command):
        self.commands.append(command)
        if command.__class__ == RegularCommand:
            self.triggers[command.trigger] = command
        elif command.__class__ == NoRefsCommand:
            self.noref_triggers[command.trigger] = command

    def register_extension(self, name, pkg='pylux.interpreter'):
        module = import_module('.'+name, pkg)
        module.register_extension(self)
