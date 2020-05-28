from ast import literal_eval
from pylux.interpreter import RegularCommand, InterpreterExtension, NoRefsCommand
from pylux import document, clihelper
from pylux.lib import printer, data, constant, exception
import decimal


class BaseExtension(InterpreterExtension):

    def register_commands(self):
        self.commands.append(RegularCommand(('Cue', 'About'), self.cue_about))
        self.commands.append(RegularCommand(('Cue', 'CopyTo'), self.cue_clone))
        self.commands.append(RegularCommand(('Cue', 'Create'), self.cue_create, check_refs=False))
        self.commands.append(RegularCommand(('Cue', 'Display'), self.cue_display))
        self.commands.append(RegularCommand(('Cue', 'Query'), self.cue_query))
        self.commands.append(RegularCommand(('Cue', 'Remove'), self.cue_remove))
        self.commands.append(RegularCommand(('Cue', 'Set'), self.cue_set))
        self.commands.append(RegularCommand(('Cue', 'SetIntens'), self.cue_setintens))
        self.commands.append(NoRefsCommand(('File', 'Write'), self.file_write))
        self.commands.append(RegularCommand(('Filter', 'CopyTo'), self.filter_clone))
        self.commands.append(RegularCommand(('Filter', 'Create'), self.filter_create, check_refs=False))
        self.commands.append(RegularCommand(('Filter', 'Remove'), self.filter_remove))
        self.commands.append(RegularCommand(('Fixture', 'About'), self.fixture_about))
        self.commands.append(RegularCommand(('Fixture', 'Create'), self.fixture_create, check_refs=False))
        self.commands.append(RegularCommand(('Fixture', 'CreateFromJson'), self.fixture_createfrom_json, check_refs=False))
        self.commands.append(RegularCommand(('Fixture', 'CompleteFrom'), self.fixture_completefrom))
        self.commands.append(RegularCommand(('Fixture', 'CopyTo'), self.fixture_clone))
        self.commands.append(RegularCommand(('Fixture', 'Display'), self.fixture_display))
        self.commands.append(RegularCommand(('Fixture', 'Patch'), self.fixture_patch))
        self.commands.append(RegularCommand(('Fixture', 'Remove'), self.fixture_remove))
        self.commands.append(RegularCommand(('Fixture', 'Set'), self.fixture_set))
        self.commands.append(RegularCommand(('Fixture', 'Unpatch'), self.fixture_unpatch))
        self.commands.append(RegularCommand(('Fixture', 'UpdateFrom'), self.fixture_updatefrom))
        self.commands.append(RegularCommand(('Group', 'About'), self.group_about))
        self.commands.append(RegularCommand(('Group', 'Append'), self.group_append_fixture))
        self.commands.append(RegularCommand(('Group', 'CopyTo'), self.group_clone))
        self.commands.append(RegularCommand(('Group', 'Create'), self.group_create, check_refs=False))
        self.commands.append(RegularCommand(('Group', 'Display'), self.group_display))
        self.commands.append(RegularCommand(('Group', 'Query'), self.group_query))
        self.commands.append(RegularCommand(('Group', 'Remove'), self.group_remove))
        self.commands.append(RegularCommand(('Group', 'Set'), self.group_set))
        self.commands.append(NoRefsCommand(('Metadata', 'About'), self.metadata_about))
        self.commands.append(NoRefsCommand(('Metadata', 'Set'), self.metadata_set))
        self.commands.append(RegularCommand(('AllPalette', 'About'), self.palette_all_about))
        self.commands.append(RegularCommand(('AllPalette', 'CopyTo'), self.palette_all_clone))
        self.commands.append(RegularCommand(('AllPalette', 'Create'), self.palette_all_create, check_refs=False))
        self.commands.append(RegularCommand(('AllPalette', 'Display'), self.palette_all_display))
        self.commands.append(RegularCommand(('AllPalette', 'Remove'), self.palette_all_remove))
        self.commands.append(RegularCommand(('AllPalette', 'Set'), self.palette_all_set))
        self.commands.append(RegularCommand(('BeamPalette', 'About'), self.palette_beam_about))
        self.commands.append(RegularCommand(('BeamPalette', 'CopyTo'), self.palette_beam_clone))
        self.commands.append(RegularCommand(('BeamPalette', 'Create'), self.palette_beam_create, check_refs=False))
        self.commands.append(RegularCommand(('BeamPalette', 'Display'), self.palette_beam_display))
        self.commands.append(RegularCommand(('BeamPalette', 'Remove'), self.palette_beam_remove))
        self.commands.append(RegularCommand(('BeamPalette', 'Set'), self.palette_beam_set))
        self.commands.append(RegularCommand(('ColourPalette', 'About'), self.palette_colour_about))
        self.commands.append(RegularCommand(('ColourPalette', 'CopyTo'), self.palette_colour_clone))
        self.commands.append(RegularCommand(('ColourPalette', 'Create'), self.palette_colour_create, check_refs=False))
        self.commands.append(RegularCommand(('ColourPalette', 'Display'), self.palette_colour_display))
        self.commands.append(RegularCommand(('ColourPalette', 'Remove'), self.palette_colour_remove))
        self.commands.append(RegularCommand(('ColourPalette', 'Set'), self.palette_colour_set))
        self.commands.append(RegularCommand(('FocusPalette', 'About'), self.palette_focus_about))
        self.commands.append(RegularCommand(('FocusPalette', 'CopyTo'), self.palette_focus_clone))
        self.commands.append(RegularCommand(('FocusPalette', 'Create'), self.palette_focus_create, check_refs=False))
        self.commands.append(RegularCommand(('FocusPalette', 'Display'), self.palette_focus_display))
        self.commands.append(RegularCommand(('FocusPalette', 'Remove'), self.palette_focus_remove))
        self.commands.append(RegularCommand(('FocusPalette', 'Set'), self.palette_focus_set))
        self.commands.append(RegularCommand(('IntensityPalette', 'About'), self.palette_intensity_about))
        self.commands.append(RegularCommand(('IntensityPalette', 'CopyTo'), self.palette_intensity_clone))
        self.commands.append(RegularCommand(('IntensityPalette', 'Create'), self.palette_intensity_create, check_refs=False))
        self.commands.append(RegularCommand(('IntensityPalette', 'Display'), self.palette_intensity_display))
        self.commands.append(RegularCommand(('IntensityPalette', 'Remove'), self.palette_intensity_remove))
        self.commands.append(RegularCommand(('IntensityPalette', 'Set'), self.palette_intensity_set))
        self.commands.append(RegularCommand(('Registry', 'About'), self.registry_about))
        self.commands.append(RegularCommand(('Registry', 'Create'), self.registry_create, check_refs=False))
        self.commands.append(RegularCommand(('Registry', 'Display'), self.registry_display))
        self.commands.append(RegularCommand(('Registry', 'Query'), self.registry_query))
        self.commands.append(RegularCommand(('Registry', 'Remove'), self.registry_remove))
        self.commands.append(RegularCommand(('Structure', 'About'), self.structure_about))
        self.commands.append(RegularCommand(('Structure', 'Create'), self.structure_create, check_refs=False))
        self.commands.append(RegularCommand(('Structure', 'CopyTo'), self.structure_clone))
        self.commands.append(RegularCommand(('Structure', 'Display'), self.structure_display))
        self.commands.append(RegularCommand(('Structure', 'Set'), self.structure_set))
        self.commands.append(RegularCommand(('Structure', 'Remove'), self.structure_remove))

    def _base_about(self, refs, obj_type):
        for ref in refs:
            obj = document.get_by_ref(self.interpreter.file, obj_type[0], ref)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(obj)])
            self.interpreter.msg.post_output([str(len(obj))+' Data Tags:'])
            self.interpreter.msg.post_output(['    '+str(k)+': '+str(obj[k])
                                              for k in sorted(obj)
                                              if k not in literal_eval(self.interpreter.config['cli']['ignore-about-tags'])])

    def _base_clone(self, refs, obj_type, dest):
        """Copy range to single (expanded to range) or copy single to range. If given a single source and single
        destination, just copy the object. If single source and range of destinations, copy the source to all
        destinations as determined by resolve_references. If range source and single destination, copy the first in
        the source to the destination point, then increment at the same intervals from the source and destination."""
        dest_refs = clihelper.resolve_references(dest)
        if len(refs) > 1 and len(dest_refs) > 1:
            self.interpreter.msg.post_feedback(
                'Cannot copy one range to another. Provide a single source or destination start point only.')
        elif len(refs) == 1 and len(dest_refs) >= 1:
            src_obj = document.get_by_ref(self.interpreter.file, obj_type[0], refs[0])
            for dest_ref in dest_refs:
                try:
                    document.insert_duplicate_object(self.interpreter.file, obj_type, src_obj, dest_ref)
                except exception.ObjectAlreadyExistsError as e:
                    self.interpreter.msg.post_feedback(
                        '{0} {1} already exists. Won\'t overwrite existing object'.format(e.obj_type, e.ref))
        elif len(refs) > 1 and len(dest_refs) == 1:
            for r in refs:
                dest_ref = str(decimal.Decimal(dest_refs[0]) + decimal.Decimal(r) - decimal.Decimal(refs[0]))
                src_obj = document.get_by_ref(self.interpreter.file, obj_type[0], r)
                try:
                    document.insert_duplicate_object(self.interpreter.file, obj_type, src_obj, dest_ref)
                except exception.ObjectAlreadyExistsError as e:
                    self.interpreter.msg.post_feedback(
                        '{0} {1} already exists. Won\'t overwrite existing object'.format(e.obj_type, e.ref))

    def _base_create(self, refs, obj_type, **kwargs):
        """Create new objects."""
        for r in refs:
            document.insert_blank_object(self.interpreter.file, obj_type, r, **kwargs)

    def _base_display(self, refs, obj_type):
        """Print a single-line summary of a range of objects."""
        for r in refs:
            obj = document.get_by_ref(self.interpreter.file, obj_type[0], r)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(obj)])

    def _base_levels_query(self, refs, obj_type, nips=True):
        """See the stored level values of all parameter types. Works with objects that
        use the levels key. Set nips to False to only show intensity values."""
        for r in refs:
            obj = document.get_by_ref(self.interpreter.file, obj_type[0], r)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(obj)])
            for l in obj['levels']:
                func = document.get_function_by_uuid(self.interpreter.file, l)
                fix = document.get_function_parent(self.interpreter.file, func)
                if func['param'] == self.interpreter.config['dimmer-attribute-name'] or nips:
                    self.interpreter.msg.post_output([[printer.get_generic_ref(fix), ':'] +
                                                      printer.get_generic_text_widget(func) + [': ',
                                                      printer.get_pretty_level_string(str(obj['levels'][l]))]])

    def _base_remove(self, refs, obj_type):
        """Remove an object from the document."""
        for r in refs:
            document.remove_by_ref(self.interpreter.file, obj_type[0], r)

    def _base_set(self, refs, obj_type, k, v):
        """Set an arbitrary data tag to a value."""
        for r in refs:
            document.get_by_ref(self.interpreter.file, obj_type[0], r)[k] = v

    def cue_about(self, refs):
        """Show stored intensity data for a cue."""
        return self._base_levels_query(refs, constant.CUE_TYPE, nips=False)

    def cue_clone(self, refs, dest):
        """Clone a cue."""
        return self._base_clone(refs, constant.CUE_TYPE, dest)

    def cue_create(self, refs):
        """Create a blank cue."""
        return self._base_create(refs, constant.CUE_TYPE)

    def cue_display(self, refs):
        """Show a single line summary of a cue."""
        return self._base_display(refs, constant.CUE_TYPE)

    def cue_query(self, refs):
        """Show stored intensity and non-intensity data for a cue."""
        return self._base_levels_query(refs, constant.CUE_TYPE)

    def cue_remove(self, refs):
        """Remove a cue."""
        return self._base_remove(refs, constant.CUE_TYPE)

    def cue_set(self, refs, k, v):
        """Set an arbitrary data tag in a cue."""
        return self._base_set(refs, constant.CUE_TYPE, k, v)

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

    def filter_clone(self, refs, dest):
        """Clone a filter."""
        return self._base_clone(refs, constant.FILTER_TYPE, dest)

    def filter_create(self, refs, k, v):
        """Create a new filter with given parameters."""
        return self._base_create(refs, constant.FILTER_TYPE, k=k, v=v)

    def filter_remove(self, refs):
        """Remove a filter."""
        return self._base_remove(refs, constant.FILTER_TYPE)

    def fixture_about(self, refs):
        """Display data tags and DMX functions of a fixture."""
        for ref in refs:
            f = document.get_by_ref(self.interpreter.file, 'fixture', ref)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(f)])
            self.interpreter.msg.post_output([str(len(f))+' Data Tags:'])
            self.interpreter.msg.post_output(['    '+str(k)+': '+str(f[k])
                                              for k in sorted(f)
                                              if k not in literal_eval(self.interpreter.config['cli']['ignore-about-tags'])])
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
        return self._base_create(refs, constant.FIXTURE_TYPE)

    def fixture_createfrom_json(self, refs, template):
        """Create a fixture from a template file."""
        template_file = data.get_data('fixture/'+template+'.json')
        if not template_file:
            self.interpreter.msg.post_feedback(['Template {0} does not exist, reverting to fallback.'.format(template)])
            template_file = data.get_data('fixture/'+self.interpreter.config['editor']['fallback-template']+'.json')
        for r in refs:
            document.insert_fixture_from_json_template(self.interpreter.file, r, template_file)

    def fixture_display(self, refs):
        """Show a single line summary of a fixture."""
        return self._base_display(refs, constant.FIXTURE_TYPE)

    def fixture_patch(self, refs, univ, addr):
        """Patch the functions of a fixture in a registry."""
        for ref in refs:
            document.safe_address_fixture_by_ref(self.interpreter.file, ref, int(univ), int(addr))

    def fixture_remove(self, refs):
        """Remove a fixture."""
        self.fixture_unpatch(refs)
        return self._base_remove(refs, constant.FIXTURE_TYPE)

    def fixture_set(self, refs, k, v):
        """Set an arbitrary data tag in a fixture."""
        return self._base_set(refs, constant.FIXTURE_TYPE, k, v)

    def fixture_unpatch(self, refs):
        """Remove all of a fixture's functions from all registries."""
        for r in refs:
            document.unpatch_fixture_by_ref(self.interpreter.file, r)

    def fixture_updatefrom(self, refs, template):
        """Update a fixture from a template file, overwriting existing tags."""
        template_file = data.get_data('fixture/'+template+'.json')
        if not template_file:
            self.interpreter.msg.post_feedback(['Template {0} does not exist, aborting'.format(template)])
        else:
            for r in refs:
                fix = document.get_by_ref(self.interpreter.file, 'fixture', r)
                document.update_fixture_from_json_template(fix, template_file)

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

    def group_clone(self, refs, dest):
        """Clone a group."""
        return self._base_clone(refs, constant.GROUP_TYPE, dest)

    def group_create(self, refs):
        """Create an empty group."""
        return self._base_create(refs, constant.GROUP_TYPE)

    def group_display(self, refs):
        """Show a single line summary of a group."""
        return self._base_display(refs, constant.GROUP_TYPE)

    def group_query(self, refs):
        """Show the used fixtures in a group, and also give a summary of each fixture."""
        for r in refs:
            grp = document.get_by_ref(self.interpreter.file, 'group', r)
            self.interpreter.msg.post_output([printer.get_generic_text_widget(grp)])
            for fix_uuid in grp['fixtures']:
                self.interpreter.msg.post_output([['    ', printer.get_generic_text_widget(
                    document.get_by_uuid(self.interpreter.file, fix_uuid)
                )]])

    def group_remove(self, refs):
        """Remove a group."""
        return self._base_remove(refs, constant.GROUP_TYPE)

    def group_set(self, refs, k, v):
        """Set an arbitrary data tag in a group."""
        return self._base_set(refs, constant.GROUP_TYPE, k, v)

    def metadata_about(self):
        """Show the values of all stored metadata."""
        m = document.get_parent_metadata_object(self.interpreter.file)
        self.interpreter.msg.post_output(['{0} Metadata Tags:'.format(str(len(m['tags'])))])
        for k, v in m['tags'].items():
            self.interpreter.msg.post_output([printer.get_metadata_string(k, v)])

    def metadata_set(self, k, v=None):
        """Set the value of a metadata tag. If no value is given, delete the tag."""
        if v:
            document.set_metadata(self.interpreter.file, k, v)
        else:
            document.remove_metadata(self.interpreter.file, k)

    def palette_all_clone(self, refs, dest):
        """Clone an all palette."""
        return self._base_clone(refs, constant.ALL_PALETTE_TYPE, dest)

    def palette_beam_clone(self, refs, dest):
        """Clone a beam palette."""
        return self._base_clone(refs, constant.BEAM_PALETTE_TYPE, dest)

    def palette_colour_clone(self, refs, dest):
        """Clone a colour palette."""
        return self._base_clone(refs, constant.COLOUR_PALETTE_TYPE, dest)

    def palette_focus_clone(self, refs, dest):
        """Clone a focus palette."""
        return self._base_clone(refs, constant.FOCUS_PALETTE_TYPE, dest)

    def palette_intensity_clone(self, refs, dest):
        """Clone an intensity palette."""
        return self._base_clone(refs, constant.INTENSITY_PALETTE_TYPE, dest)

    def palette_all_create(self, refs):
        """Create an empty all palette (preset)."""
        return self._base_create(refs, constant.ALL_PALETTE_TYPE)

    def palette_beam_create(self, refs):
        """Create an empty beam palette."""
        return self._base_create(refs, constant.BEAM_PALETTE_TYPE)

    def palette_colour_create(self, refs):
        """Create an empty colour palette."""
        return self._base_create(refs, constant.COLOUR_PALETTE_TYPE)

    def palette_focus_create(self, refs):
        """Create an empty focus palette."""
        return self._base_create(refs, constant.FOCUS_PALETTE_TYPE)

    def palette_intensity_create(self, refs):
        """Create an empty intensity palette."""
        return self._base_create(refs, constant.INTENSITY_PALETTE_TYPE)

    def palette_all_display(self, refs):
        """Show a single line summary of an all palette."""
        return self._base_display(refs, constant.ALL_PALETTE_TYPE)

    def palette_beam_display(self, refs):
        """Show a single line summary of a beam palette."""
        return self._base_display(refs, constant.BEAM_PALETTE_TYPE)

    def palette_colour_display(self, refs):
        """Show a single line summary of a colour palette."""
        return self._base_display(refs, constant.COLOUR_PALETTE_TYPE)

    def palette_focus_display(self, refs):
        """Show a single line summary of a focus palette."""
        return self._base_display(refs, constant.FOCUS_PALETTE_TYPE)

    def palette_intensity_display(self, refs):
        """Show a single line summary of an intensity palette."""
        return self._base_display(refs, constant.INTENSITY_PALETTE_TYPE)

    def palette_all_about(self, refs):
        """Show the stored values in an all palette."""
        return self._base_levels_query(refs, constant.ALL_PALETTE_TYPE)

    def palette_beam_about(self, refs):
        """Show the stored values in a beam palette."""
        return self._base_levels_query(refs, constant.BEAM_PALETTE_TYPE)

    def palette_colour_about(self, refs):
        """Show the stored values in a colour palette."""
        return self._base_levels_query(refs, constant.COLOUR_PALETTE_TYPE)

    def palette_focus_about(self, refs):
        """Show the stored values in a focus palette."""
        return self._base_levels_query(refs, constant.FOCUS_PALETTE_TYPE)

    def palette_intensity_about(self, refs):
        """Show the stored values in an intensity palette."""
        return self._base_levels_query(refs, constant.INTENSITY_PALETTE_TYPE)

    def palette_all_remove(self, refs):
        """Remove an all palette."""
        return self._base_remove(refs, constant.ALL_PALETTE_TYPE)

    def palette_beam_remove(self, refs):
        """Remove a beam palette."""
        return self._base_remove(refs, constant.BEAM_PALETTE_TYPE)

    def palette_colour_remove(self, refs):
        """Remove a colour palette."""
        return self._base_remove(refs, constant.COLOUR_PALETTE_TYPE)

    def palette_focus_remove(self, refs):
        """Remove a focus palette."""
        return self._base_remove(refs, constant.FOCUS_PALETTE_TYPE)

    def palette_intensity_remove(self, refs):
        """Remove an intensity palette."""
        return self._base_remove(refs, constant.INTENSITY_PALETTE_TYPE)

    def palette_all_set(self, refs, k, v):
        """Set an arbitrary data tag in an all palette."""
        return self._base_set(refs, constant.ALL_PALETTE_TYPE, k, v)

    def palette_beam_set(self, refs, k, v):
        """Set an arbitrary data tag in a beam palette."""
        return self._base_set(refs, constant.BEAM_PALETTE_TYPE, k, v)

    def palette_colour_set(self, refs, k, v):
        """Set an arbitrary data tag in a colour palette."""
        return self._base_set(refs, constant.COLOUR_PALETTE_TYPE, k, v)

    def palette_focus_set(self, refs, k, v):
        """Set an arbitrary data tag in a focus palette."""
        return self._base_set(refs, constant.FOCUS_PALETTE_TYPE, k, v)

    def palette_intensity_set(self, refs, k, v):
        """Set an arbitrary data tag in an intensity palette."""
        return self._base_set(refs, constant.INTENSITY_PALETTE_TYPE, k, v)

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
        return self._base_create(refs, constant.REGISTRY_TYPE)

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
        """Remove a registry."""
        return self._base_remove(refs, constant.REGISTRY_TYPE)

    def structure_about(self, refs):
        """Show the stored data tags of a structure."""
        return self._base_about(refs, constant.STRUCTURE_TYPE)

    def structure_clone(self, refs, dest):
        """Clone a structure."""
        return self._base_clone(refs, constant.STRUCTURE_TYPE, dest)

    def structure_create(self, refs, structure_type):
        """Insert a blank structure object."""
        return self._base_create(refs, constant.STRUCTURE_TYPE, structure_type=structure_type)

    def structure_display(self, refs):
        """Display a single-line summary of a structure."""
        return self._base_display(refs, constant.STRUCTURE_TYPE)

    def structure_remove(self, refs):
        """Remove a structure."""
        return self._base_remove(refs, constant.STRUCTURE_TYPE)

    def structure_set(self, refs, k, v):
        """Set an arbitrary data tag in a structure."""
        return self._base_set(refs, constant.STRUCTURE_TYPE, k, v)


def register_extension(interpreter):
    BaseExtension(interpreter).register_extension()
