from pylux.interpreter import InterpreterExtension, NoRefsCommand, Noun, Verb
import inspect


class HelpExtension(InterpreterExtension):

    def register_commands(self):
        self.commands.append(NoRefsCommand((Noun.PROGRAM, Verb.HELP), self.help_command))

    def help_command(self, command_name=None):
        """Get the usage and synopsis for a command. Omit command_name to retrieve a list of all available commands."""
        if not command_name:
            self.post_output([[str(len(self.interpreter.commands)), ' available commands:']])
            for command in self.interpreter.commands:
                self.post_output([['[', command.function.__module__, '] ',
                                 command.trigger[0], ' ', command.trigger[1]]])
            return
        trigger = tuple(command_name.split(' '))
        if trigger in self.interpreter.triggers:
            command = self.interpreter.triggers[trigger]
            self.post_output(['Usage:'])
            self.post_output([[command.trigger[0], ('required', ' refs '), command.trigger[1]] +
                             [('required', ' ' + p) for p in command.req_params] +
                             [('optional', ' ' + p) for p in command.opt_params]], indentation=1)
            self.post_output(['Synopsis:'])
            try:
                self.post_output([inspect.cleandoc(inspect.getdoc(command.function))], indentation=1)
            # If the docstring is empty, the cleandoc function above will raise an
            # AttributeError when it attempts to parse the docstring, so we can
            # catch this to indicate that no synopsis was provided.
            except AttributeError:
                self.post_output(['No synopsis provided'], indentation=1)
        elif trigger in self.interpreter.noref_triggers:
            command = self.interpreter.noref_triggers[trigger]
            # NoRef commands require slightly different handling for usage as they
            # will not contain the required refs section of the command. Other
            # than that, the method for showing its help page is identical to
            # that of a RegularCommand above.
            self.post_output(['Usage:'])
            self.post_output([[command.trigger[0], ' ', command.trigger[1]] +
                             [('required', ' ' + p) for p in command.req_params] +
                             [('optional', ' ' + p) for p in command.opt_params]], indentation=1)
            self.post_output(['Synopsis:'])
            try:
                self.post_output([inspect.cleandoc(inspect.getdoc(command.function))], indentation=1)
            except AttributeError:
                self.post_output(['No synopsis provided'], indentation=1)
        else:
            self.post_feedback('Error: Command {0} does not exist'.format(command_name))


def register_extension(interpreter):
    HelpExtension(interpreter).register_extension()