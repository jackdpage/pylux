from pylux import clihelper, document, _ROOT
from pylux.lib import exception
from importlib import import_module
import os.path


class RegularCommand:
    def __init__(self, syntax, function, check_refs=True):
        self.trigger = syntax
        self.function = function
        self.check_refs = check_refs
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
        self.register_commands()

    def register_commands(self):
        self.register_command(NoRefsCommand(('File', 'Write'), self.file_write))
        self.register_command(NoRefsCommand(('File', 'WriteTo'), self.file_writeto))
        self.register_command(NoRefsCommand(('Program', 'Quit'), self.program_abort))
        self.register_command(NoRefsCommand(('Program', 'WriteAndQuit'), self.program_exit))
        self.register_command(NoRefsCommand(('Program', 'ReloadConfig'), self.reload_config))

    def file_write(self):
        document.write_to_file(self.file, self.config['main']['load_file'])
        self.msg.post_feedback('Saved to '+self.config['main']['load_file'])

    def file_writeto(self, location):
        self.config['main']['load_file'] = location
        self.msg.post_feedback('Set default save location to '+location)
        self.file_write()

    def program_abort(self):
        raise exception.ProgramExit

    def program_exit(self):
        self.file_write()
        self.program_abort()

    def reload_config(self):
        self.config.read([os.path.join(_ROOT, 'default.conf')])

    def _get_init_keywords(self):
        """Get all the keywords which could be the first keyword of a command."""
        init_keywords = []
        for t in {**self.triggers, **self.noref_triggers}:
            if t[0] not in init_keywords:
                init_keywords.append(t[0])
        return init_keywords

    def _get_noref_keyword_2(self, keyword_1):
        """Get all the keywords which could be the second keyword of a norefs command, given
        the first keyword of the command."""
        keywords = []
        for t in self.noref_triggers:
            if t[0] == keyword_1:
                keywords.append(t[1])
        return keywords

    def _get_ref_keyword_2(self, keyword_1):
        """Get all the keywords which could be the second keyword of a refs command (after
        the refs field), given the first keyword of the commond."""
        keywords = []
        for t in self.triggers:
            if t[0] == keyword_1:
                keywords.append(t[1])
        return keywords

    def get_expected_input(self, partial_command):
        """Return a list of expected next keywords based on a partial command and the registered commands."""
        n = len(partial_command.split())
        if n == 0:
            return self._get_init_keywords()
        elif n == 1:
            return self._get_noref_keyword_2(partial_command.split()[0])
        elif n == 2:
            return self._get_ref_keyword_2(partial_command.split()[0])
        else:
            return None

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
                    action = keywords[2]
                    trigger = (obj, action)
                    command = self.triggers[trigger]
                    if command.check_refs:
                        refs = clihelper.safe_resolve_dec_references_with_filters(self.file, obj.lower(), keywords[1])
                    else:
                        refs = clihelper.resolve_references(keywords[1])
                    if len(keywords) > 3:
                        parameters = keywords[3:]
                    else:
                        parameters = []
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
