from pylux import clihelper, document
from pylux.lib import exception, data
from importlib import import_module
import os.path
import inspect
import pylux.lib.keyword as kw
from collections import OrderedDict


class RegularCommand:
    def __init__(self, syntax, function, check_refs=True):
        self.trigger = syntax
        self.function = function
        self.check_refs = check_refs
        # Get the parameters of the function through live inspection and
        # turn it into a static ordered dict. Then pop out the first entry
        # (which will be refs, which is not considered a
        # parameter for a RegularCommand. popitem(False) removes the first
        # from the OrderedDict
        parameters = OrderedDict(inspect.signature(function).parameters)

        parameters.popitem(False)
        self.parameters = [k for k, v in parameters.items()]
        self.opt_params = [k for k, v in parameters.items() if v.default is not v.empty]
        self.req_params = [k for k, v in parameters.items() if v.default is v.empty]


class NoRefsCommand:
    def __init__(self, syntax, function):
        self.trigger = syntax
        self.function = function
        # This is the same as the RegularCommand, except we are expecting one fewer arguments due to the lack of refs
        parameters = OrderedDict(inspect.signature(function).parameters)
        self.parameters = [k for k, v in parameters.items()]
        self.opt_params = [k for k, v in parameters.items() if v.default is not v.empty]
        self.req_params = [k for k, v in parameters.items() if v.default is v.empty]


class InterpreterExtension:
    def __init__(self, interpreter: 'Interpreter'):
        self.interpreter = interpreter
        self.file = interpreter.file
        self.post_feedback = interpreter.msg.post_feedback
        self.post_output = interpreter.msg.post_output
        self.config = interpreter.config
        self.commands = []
        self.register_commands()

    def register_commands(self):
        pass

    def register_extension(self):
        for command in self.commands:
            self.interpreter.register_command(command)


class MessageBus:
    def __init__(self):
        self.clients = []

    def post_feedback(self, msg):
        for client in self.clients:
            client.post_feedback(msg)

    def post_output(self, msg, **kwargs):
        for client in self.clients:
            client.post_output(msg, **kwargs)

    def subscribe_client(self, client):
        self.clients.append(client)


class Interpreter:
    def __init__(self, file: 'document.Document', config):
        self.file = file
        self.msg = MessageBus()
        self.config = config
        self.commands = []
        self.triggers = {}
        self.extension = {}
        self.noref_triggers = {}
        self.register_commands()

    def subscribe_client(self, client):
        """Subscribe a client to the message bus of this interpreter instance.
        The client class must have both a post_feedback and post_output
        method in order to handle responses."""
        self.msg.subscribe_client(client)

    def register_commands(self):
        self.register_command(NoRefsCommand((kw.FILE, kw.WRITE), self.file_write))
        self.register_command(NoRefsCommand((kw.FILE, kw.WRITE_TO), self.file_writeto))
        self.register_command(NoRefsCommand((kw.PROGRAM, kw.EXIT), self.program_abort))
        self.register_command(NoRefsCommand((kw.PROGRAM, kw.WRITE_EXIT), self.program_exit))
        self.register_command(NoRefsCommand((kw.PROGRAM, kw.RELOAD_CONFIG), self.reload_config))

    def file_write(self):
        """Save changes to the default write location. If no write location has been
        set since opening the program, this will be the same as the load location."""
        self.file.write_file(self.config['main']['load_file'])
        self.msg.post_feedback('Saved to '+self.config['main']['load_file'])

    def file_writeto(self, location):
        """Change the default write location and then save the file there. Any future
        saves using File Write will also save to this location."""
        self.config['main']['load_file'] = location
        self.msg.post_feedback('Set default save location to '+location)
        self.file_write()

    def program_abort(self):
        """Exit the program immediately without saving changes to disk."""
        raise exception.ProgramExit

    def program_exit(self):
        """Save changes to the default write location, then exit the program."""
        self.file_write()
        self.program_abort()

    def reload_config(self):
        """Refresh the configuration by reloading all configuration files.
        Configuration files named config.ini will be loaded in the following order, with latter files
        being preferred to earlier files where options clash:
            built-in defaults => /usr/share/pylux => ~/.pylux => ./content
        Settings changed on a per-file basis will not be affected."""
        self.config.read([os.path.join(data.LOCATIONS[i], 'config.ini') for i in reversed(data.PRIORITY)])

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

    def _get_completed_noun(self, partial_noun):
        """Given the start of a valid noun, return the list of completed nouns
        it could be."""
        potential = []
        # At the moment, the best way of getting a list of all potential
        # nouns is to look for items in the Noun dict with str values.
        # This is going to change because this is an awful method
        for noun in kw.NOUNS:
            if noun.startswith(partial_noun):
                potential.append(noun.lstrip(partial_noun))
        return potential

    def get_expected_input(self, partial_command, check_partial=False):
        """Return a list of expected next keywords based on a partial command and the registered commands."""
        keywords = partial_command.split()
        n = len(keywords)
        if n == 0:
            return self._get_init_keywords()
        elif n == 1:
            # This checks if the the first keyword is an entire valid noun, or just
            # a partial one. In the case of a valid noun, we can send the verb list
            # for NoRef commands. For a partial noun, we can send the potential
            # complete nouns
            if keywords[0] in kw.NOUNS:
                return self._get_noref_keyword_2(keywords[0])
            elif check_partial:
                return self._get_completed_noun(keywords[0])
        elif n == 2:
            return self._get_ref_keyword_2(partial_command.split()[0])
        else:
            return None

    def command_failed(self, posted_command):
        self.msg.post_feedback(['Error: Invalid command '+posted_command])

    def bad_parameters(self, command):
        self.msg.post_feedback(['Error: '+command.trigger[0]+' '+command.trigger[1] +
                                ' requires at least '+str(len(command.req_params))+' parameters'])

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
        # No commands have fewer than two words
        if len(keywords) < 2:
            self.command_failed(posted_command)
            return
        # If the first two keywords are in noref_triggers then this is a command with no references
        elif (keywords[0], keywords[1]) in self.noref_triggers:
            obj = keywords[0]
            action = keywords[1]
            trigger = (obj, action)
            command = self.noref_triggers[trigger]
            if len(keywords) > 2:
                parameters = keywords[2:]
            else:
                parameters = []
            # If the number of parameter keywords is fewer than the required parameters,
            # then the command cannot be fulfilled
            if len(parameters) < len(command.req_params):
                self.bad_parameters(command)
            # If the number of parameter keywords is greater than the required parameters,
            # then the optional parameter must have been supplied too, so calculate the
            # parameters in case this is a multi-word one
            elif len(parameters) > len(command.req_params):
                args = calculate_params(len(command.parameters), parameters)
                command.function(*args)
            # If the number of parameter keywords is equal to the required parameters, we
            # can just pass the parameters straight into the function
            elif len(parameters) == len(command.req_params):
                command.function(*parameters)
            return
        # If the first and third keywords are in triggers, then the second keyword will be the references
        elif len(keywords) > 2:
            if (keywords[0], keywords[2]) in self.triggers:
                obj = keywords[0]
                action = keywords[2]
                trigger = (obj, action)
                command = self.triggers[trigger]
                # If the check_refs flag is true, the refs argument (arg2) is a
                # list of Python objects representing the matched document objects.
                # If the check_refs flag is false, the refs argument is a list of
                # Decimals matched in the given range.
                if command.check_refs:
                    try:
                        refs = clihelper.match_objects(keywords[1], self.file, document.COMMAND_STR_MAP[obj])
                    except exception.ReferenceSyntaxError as e:
                        self.msg.post_feedback('Syntax error: '+e.message)
                        return
                    if not refs:
                        self.msg.post_feedback('Error: No valid objects in given range')
                        return
                else:
                    refs = clihelper.resolve_references(keywords[1])
                if len(keywords) > 3:
                    parameters = keywords[3:]
                else:
                    parameters = []
                # If the number of parameter keywords is fewer than the required parameters,
                # then the command cannot be fulfilled
                if len(parameters) < len(command.req_params):
                    self.bad_parameters(command)
                # If the number of parameter keywords is greater than the required parameters,
                # then the optional parameter must have been supplied too, so calculate the
                # parameters in case this is a multi-word one
                elif len(parameters) > len(command.req_params):
                    args = calculate_params(len(command.parameters), parameters)
                    command.function(refs, *args)
                # If the number of parameter keywords is equal to the required parameters, we
                # can just pass the parameters straight into the function
                elif len(parameters) == len(command.req_params):
                    command.function(refs, *parameters)
                return
            else:
                self.command_failed(posted_command)
                return
        # Otherwise, the command doesn't exist
        else:
            self.command_failed(posted_command)

    def call_internal(self, trigger, *args):
        """Call a command from another extension."""
        if trigger in self.triggers:
            self.triggers[trigger].function(*args)
        elif trigger in self.noref_triggers:
            self.noref_triggers[trigger].function(*args)

    def register_command(self, command):
        self.commands.append(command)
        if command.__class__ == RegularCommand:
            self.triggers[command.trigger] = command
        elif command.__class__ == NoRefsCommand:
            self.noref_triggers[command.trigger] = command

    def register_extension(self, name, pkg='pylux.interpreter'):
        module = import_module('.'+name, pkg)
        module.register_extension(self)
