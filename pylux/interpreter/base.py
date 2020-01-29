from pylux.interpreter import RegularCommand, InterpreterExtension
from pylux import document, clihelper
from pylux.lib import printer


class BaseExtension(InterpreterExtension):

    def register_commands(self):
        self.commands.append(RegularCommand(('Cue', 'Create'), self.cue_create))
        self.commands.append(RegularCommand(('Cue', 'Set'), self.cue_set))
        self.commands.append(RegularCommand(('File', 'Write'), self.file_write))
        self.commands.append(RegularCommand(('Fixture', 'Create'), self.fixture_create))
        self.commands.append(RegularCommand(('Fixture', 'Set'), self.fixture_set))
        self.commands.append(RegularCommand(('Fixture', 'Patch'), self.fixture_patch))
        self.commands.append(RegularCommand(('Group', 'About'), self.group_about))
        self.commands.append(RegularCommand(('Group', 'Append'), self.group_append_fixture))
        self.commands.append(RegularCommand(('Group', 'Create'), self.group_create))

    def cue_create(self, refs):
        """Create a blank cue."""
        for ref in refs:
            document.insert_blank_cue(self.interpreter.file, ref)

    def cue_set(self, refs, k, v):
        """Set the value of a cue's tag."""
        for ref in refs:
            document.get_by_ref(self.interpreter.file, 'cue', ref)[k] = v

    def file_write(self, refs, location):
        """Write file to location."""
        document.write_to_file(self.interpreter.file, location)

    def fixture_create(self, refs):
        """Create a blank fixture."""
        for ref in refs:
            document.insert_blank_fixture(self.interpreter.file, ref)

    def fixture_set(self, refs, k, v):
        """Set the value of a fixture's tag."""
        for ref in refs:
            document.get_by_ref(self.interpreter.file, 'fixture', ref)[k] = v

    def fixture_patch(self, refs, univ, addr):
        """Patch the functions of a fixture in a registry."""
        for ref in refs:
            document.safe_address_fixture_by_ref(self.interpreter.file, ref, int(univ), int(addr))

    def group_about(self, refs):
        """Display the contents of a group."""
        for ref in refs:
            grp = document.get_by_ref(self.interpreter.file, 'group', ref)
            self.interpreter.msg.post_output([
                printer.get_generic_text_widget(grp),
                ', '.join([document.get_by_uuid(self.interpreter.file, i)['ref'] for i in grp['fixtures']])])

    def group_create(self, refs):
        """Create an empty group."""
        for ref in refs:
            document.insert_blank_group(self.interpreter.file, ref)

    def group_append_fixture(self, refs, frefs):
        """Append a fixture to a group list."""
        for ref in refs:
            group = document.get_by_ref(self.interpreter.file, 'group', ref)
            for fref in clihelper.safe_resolve_dec_references(self.interpreter.file, 'fixture', frefs):
                document.group_append_fixture_by_ref(self.interpreter.file, group, fref)


def register_extension(interpreter):
    BaseExtension(interpreter).register_extension()
