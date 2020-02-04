from pylux.interpreter import RegularCommand, InterpreterExtension, NoRefsCommand
from pylux import document, clihelper
from pylux.lib import printer, data


class BaseExtension(InterpreterExtension):

    def register_commands(self):
        self.commands.append(RegularCommand(('Cue', 'About'), self.cue_about))
        self.commands.append(RegularCommand(('Cue', 'Create'), self.cue_create, check_refs=False))
        self.commands.append(RegularCommand(('Cue', 'Display'), self.cue_display))
        self.commands.append(RegularCommand(('Cue', 'Query'), self.cue_query))
        self.commands.append(RegularCommand(('Cue', 'Remove'), self.cue_remove))
        self.commands.append(RegularCommand(('Cue', 'Set'), self.cue_set))
        self.commands.append(RegularCommand(('Cue', 'SetIntens'), self.cue_setintens))
        self.commands.append(NoRefsCommand(('File', 'Write'), self.file_write))
        self.commands.append(RegularCommand(('Filter', 'Create'), self.filter_create, check_refs=False))
        self.commands.append(RegularCommand(('Filter', 'Remove'), self.filter_remove))
        self.commands.append(RegularCommand(('Fixture', 'About'), self.fixture_about))
        self.commands.append(RegularCommand(('Fixture', 'Create'), self.fixture_create, check_refs=False))
        self.commands.append(RegularCommand(('Fixture', 'CreateFrom'), self.fixture_createfrom, check_refs=False))
        self.commands.append(RegularCommand(('Fixture', 'CompleteFrom'), self.fixture_completefrom))
        self.commands.append(RegularCommand(('Fixture', 'CopyTo'), self.fixture_clone))
        self.commands.append(RegularCommand(('Fixture', 'Display'), self.fixture_display))
        self.commands.append(RegularCommand(('Fixture', 'Patch'), self.fixture_patch))
        self.commands.append(RegularCommand(('Fixture', 'Remove'), self.fixture_remove))
        self.commands.append(RegularCommand(('Fixture', 'Set'), self.fixture_set))
        self.commands.append(RegularCommand(('Fixture', 'Unpatch'), self.fixture_unpatch))
        self.commands.append(RegularCommand(('Group', 'About'), self.group_about))
        self.commands.append(RegularCommand(('Group', 'Append'), self.group_append_fixture))
        self.commands.append(RegularCommand(('Group', 'Create'), self.group_create, check_refs=False))
        self.commands.append(RegularCommand(('Group', 'Display'), self.group_display))
        self.commands.append(RegularCommand(('Group', 'Query'), self.group_query))
        self.commands.append(RegularCommand(('Group', 'Remove'), self.group_remove))
        self.commands.append(RegularCommand(('Group', 'Set'), self.group_set))
        self.commands.append(RegularCommand(('Registry', 'About'), self.registry_about))
        self.commands.append(RegularCommand(('Registry', 'Create'), self.registry_create, check_refs=False))
        self.commands.append(RegularCommand(('Registry', 'Display'), self.registry_display))
        self.commands.append(RegularCommand(('Registry', 'Query'), self.registry_query))
        self.commands.append(RegularCommand(('Registry', 'Remove'), self.registry_remove))

    def cue_about(self, refs):
        """Show the intensities of fixtures in a cue."""
        for r in refs:
            cue = document.get_by_ref(self.interpreter.file, 'cue', r)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(cue)])
            for l in cue['levels']:
                func = document.get_function_by_uuid(self.interpreter.file, l)
                if func['param'] == 'Intens':
                    fix = document.get_function_parent(self.interpreter.file, func)
                    self.interpreter.msg.post_output([[printer.get_generic_ref(fix), ' ', str(cue['levels'][l])]])

    def cue_create(self, refs):
        """Create a blank cue."""
        for ref in refs:
            document.insert_blank_cue(self.interpreter.file, ref)

    def cue_display(self, refs):
        """Show a single-line summary of a cue."""
        for r in refs:
            cue = document.get_by_ref(self.interpreter.file, 'cue', r)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(cue)])

    def cue_query(self, refs):
        """As for Cue About, except also show levels of NIPs."""
        for r in refs:
            cue = document.get_by_ref(self.interpreter.file, 'cue', r)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(cue)])
            for l in cue['levels']:
                func = document.get_function_by_uuid(self.interpreter.file, l)
                fix = document.get_function_parent(self.interpreter.file, func)
                self.interpreter.msg.post_output([[printer.get_generic_ref(fix), ':'] +
                                                  printer.get_generic_text_widget(func) +
                                                  [': ', str(cue['levels'][l])]])

    def cue_remove(self, refs):
        """Remove a cue."""
        for r in refs:
            document.remove_by_ref(self.interpreter.file, 'cue', r)

    def cue_set(self, refs, k, v):
        """Set the value of a cue's tag."""
        for ref in refs:
            document.get_by_ref(self.interpreter.file, 'cue', ref)[k] = v

    def cue_setintens(self, refs, fix_refs, level):
        """Set the level of a fixture's Intens function in a cue."""
        frefs = clihelper.safe_resolve_dec_references(self.interpreter.file, 'fixture', fix_refs)
        for r in refs:
            cue = document.get_by_ref(self.interpreter.file, 'cue', r)
            for fref in frefs:
                fix = document.get_by_ref(self.interpreter.file, 'fixture', fref)
                intens_func = document.find_fixture_intens(fix)
                if intens_func:
                    cue['levels'][intens_func['uuid']] = level

    def file_write(self, location):
        """Write file to location."""
        document.write_to_file(self.interpreter.file, location)

    def filter_create(self, refs, k, v):
        """Create a new filter with given parameters."""
        for r in refs:
            document.insert_filter_with_params(self.interpreter.file, r, k, v)

    def filter_remove(self, refs):
        """Remove a filter."""
        for r in refs:
            document.remove_by_ref(self.interpreter.file, 'filter', r)

    def fixture_about(self, refs):
        """Display data tags and DMX functions of a fixture."""
        for ref in refs:
            f = document.get_by_ref(self.interpreter.file, 'fixture', ref)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(f)])
            self.interpreter.msg.post_output([str(len(f))+' Data Tags:'])
            self.interpreter.msg.post_output(['    '+str(k)+': '+str(f[k])
                                              for k in sorted(f)
                                              if k not in self.interpreter.config['cli']['ignore-about-tags']])
            try:
                if len(f['personality']):
                    self.interpreter.msg.post_output([str(len(f['personality']))+' DMX Functions:'])
                    for func in f['personality']:
                        self.interpreter.msg.post_output([['    ']+printer.get_generic_text_widget(func)])
            except KeyError:
                pass

    def fixture_clone(self, refs, dest):
        """Clone a fixture to a destination(s)"""
        dests = clihelper.resolve_references(dest)
        for dest in dests:
            document.insert_duplicate_fixture_by_ref(self.interpreter.file, refs[0], dest)

    def fixture_completefrom(self, refs, template):
        """Compare an existing fixture with a template file and add any tags which are missing. If there is no
        personality then the entire template file personality will be added. If there are conflicting personalities
        then the existing fixture personality is maintained."""
        template_file = data.get_data('fixture/' + template + '.json')
        if not template_file:
            self.interpreter.msg.post_feedback(['Template {0} does not exist, reverting to fallback.'.format(template)])
            template_file = data.get_data('fixture/' + self.interpreter.config['editor']['fallback-template'] + '.json')
        for r in refs:
            fix = document.get_by_ref(self.interpreter.file, 'fixture', r)
            document.complete_fixture_from_json_template(fix, template_file)

    def fixture_create(self, refs):
        """Create a blank fixture."""
        for r in refs:
            document.insert_blank_fixture(self.interpreter.file, r)

    def fixture_createfrom(self, refs, template):
        template_file = data.get_data('fixture/'+template+'.json')
        if not template_file:
            self.interpreter.msg.post_feedback(['Template {0} does not exist, reverting to fallback.'.format(template)])
            template_file = data.get_data('fixture/'+self.interpreter.config['editor']['fallback-template']+'.json')
        for r in refs:
            document.insert_fixture_from_json_template(self.interpreter.file, r, template_file)

    def fixture_display(self, refs):
        """Display a single-line summary of a fixture."""
        for r in refs:
            fix = document.get_by_ref(self.interpreter.file, 'fixture', r)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(fix)])

    def fixture_patch(self, refs, univ, addr):
        """Patch the functions of a fixture in a registry."""
        for ref in refs:
            document.safe_address_fixture_by_ref(self.interpreter.file, ref, int(univ), int(addr))

    def fixture_remove(self, refs):
        """Remove a fixture."""
        for r in refs:
            document.remove_by_ref(self.interpreter.file, 'fixture', r)

    def fixture_set(self, refs, k, v):
        """Set the value of a fixture's tag."""
        for r in refs:
            document.get_by_ref(self.interpreter.file, 'fixture', r)[k] = v

    def fixture_unpatch(self, refs):
        """Remove all of a fixture's functions from all registries."""
        for r in refs:
            document.unpatch_fixture_by_ref(self.interpreter.file, r)

    def group_about(self, refs):
        """Display the contents of a group."""
        for r in refs:
            grp = document.get_by_ref(self.interpreter.file, 'group', r)
            self.interpreter.msg.post_output([
                printer.get_generic_text_widget(grp),
                ', '.join([document.get_by_uuid(self.interpreter.file, i)['ref'] for i in grp['fixtures']])])

    def group_append_fixture(self, refs, frefs):
        """Append a fixture to a group list."""
        for r in refs:
            group = document.get_by_ref(self.interpreter.file, 'group', r)
            for fref in clihelper.safe_resolve_dec_references(self.interpreter.file, 'fixture', frefs):
                document.group_append_fixture_by_ref(self.interpreter.file, group, fref)

    def group_create(self, refs):
        """Create an empty group."""
        for r in refs:
            document.insert_blank_group(self.interpreter.file, r)

    def group_display(self, refs):
        """Print a single-line summary of a group."""
        for r in refs:
            grp = document.get_by_ref(self.interpreter.file, 'group', r)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(grp)])

    def group_query(self, refs):
        """Show the used fixtures in a group, and also give a summary of each fixture."""
        for r in refs:
            grp = document.get_by_ref(self.interpreter.file, 'group', r)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(grp)])
            fixtures = ''
            for fix_uuid in grp['fixtures']:
                self.interpreter.msg.post_output([['    ', printer.get_generic_text_widget(
                    document.get_by_uuid(self.interpreter.file, fix_uuid)
                )]])

    def group_remove(self, refs):
        """Remove a group."""
        for r in refs:
            document.remove_by_ref(self.interpreter.file, 'group', r)

    def group_set(self, refs, k, v):
        """Set arbitrary data tags for a group."""
        for r in refs:
            grp = document.get_by_ref(self.interpreter.file, 'group', r)
            grp[k] = v

    def registry_about(self, refs):
        """Show a summary of the used addresses in a registry but don't provide any further information."""
        for r in refs:
            reg = document.get_by_ref(self.interpreter.file, 'registry', r)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(reg)])
            table = []
            current_row = ['   ']
            width = int(self.interpreter.config['cli']['registry-summary-width'])
            for i in range(0, width):
                current_row += [' ', str(format(i, '02d'))]
            for i in range(1, 514):
                if i % width == 1 or i == 513:
                    table.append(current_row)
                    current_row = [str(format(i, '03d')), '  ']
                if str(i) in reg['table'] or i in reg['table']:
                    current_row.append(('error', '#  '))
                else:
                    current_row.append(('success', '-  '))
            self.interpreter.msg.post_output(table)

    def registry_create(self, refs):
        """Insert a blank registry."""
        for r in refs:
            document.insert_blank_registry(self.interpreter.file, r)

    def registry_display(self, refs):
        """Display a single-line summary of a registry."""
        for r in refs:
            reg = document.get_by_ref(self.interpreter.file, 'registry', r)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(reg)])

    def registry_query(self, refs):
        """Show all used addresses in a registry and the functions they are occupied by."""
        for r in refs:
            reg = document.get_by_ref(self.interpreter.file, 'registry', r)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(reg)])
            t = {int(i): reg['table'][i] for i in reg['table']}
            for k, v in sorted(t.items()):
                func = document.get_function_by_uuid(self.interpreter.file, v)
                f = document.get_function_parent(self.interpreter.file, func)
                self.interpreter.msg.post_output([['DMX', str(format(k, '03d')), ': '] +
                               printer.get_generic_text_widget(f) + [' ('] +
                               printer.get_generic_text_widget(func) + [')']])

    def registry_remove(self, refs):
        """Remove a registry. This will break any patching if the registry is not empty."""
        for r in refs:
            document.remove_by_ref(self.interpreter.file, 'registry', r)


def register_extension(interpreter):
    BaseExtension(interpreter).register_extension()
