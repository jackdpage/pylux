from ast import literal_eval
from pylux.interpreter import RegularCommand, InterpreterExtension, NoRefsCommand
from pylux import clihelper, document
from pylux.lib import printer, exception
import decimal
from decimal import Decimal


class BaseExtension(InterpreterExtension):

    def register_commands(self):
        self.commands.append(RegularCommand(('Cue', 'About'), self.cue_about))
        self.commands.append(RegularCommand(('Cue', 'CopyTo'), self.cue_clone))
        self.commands.append(RegularCommand(('Cue', 'Create'), self.cue_create, check_refs=False))
        self.commands.append(RegularCommand(('Cue', 'Display'), self.cue_display))
        self.commands.append(RegularCommand(('Cue', 'Label'), self.cue_label))
        self.commands.append(RegularCommand(('Cue', 'Query'), self.cue_query))
        self.commands.append(RegularCommand(('Cue', 'Remove'), self.cue_remove))
        self.commands.append(RegularCommand(('Cue', 'Set'), self.cue_set))
        self.commands.append(RegularCommand(('Cue', 'SetIntens'), self.cue_setintens))
        self.commands.append(RegularCommand(('Filter', 'CopyTo'), self.filter_clone))
        self.commands.append(RegularCommand(('Filter', 'Create'), self.filter_create, check_refs=False))
        self.commands.append(RegularCommand(('Filter', 'Remove'), self.filter_remove))
        self.commands.append(RegularCommand(('Fixture', 'About'), self.fixture_about))
        self.commands.append(RegularCommand(('Fixture', 'Create'), self.fixture_create, check_refs=False))
        self.commands.append(RegularCommand(('Fixture', 'CopyTo'), self.fixture_clone))
        self.commands.append(RegularCommand(('Fixture', 'Display'), self.fixture_display))
        self.commands.append(RegularCommand(('Fixture', 'Fan'), self.fixture_fan))
        self.commands.append(RegularCommand(('Fixture', 'Patch'), self.fixture_patch))
        self.commands.append(RegularCommand(('Fixture', 'Remove'), self.fixture_remove))
        self.commands.append(RegularCommand(('Fixture', 'Set'), self.fixture_set))
        self.commands.append(RegularCommand(('Fixture', 'Unpatch'), self.fixture_unpatch))
        self.commands.append(RegularCommand(('Group', 'About'), self.group_about))
        self.commands.append(RegularCommand(('Group', 'Append'), self.group_append_fixture))
        self.commands.append(RegularCommand(('Group', 'CopyTo'), self.group_clone))
        self.commands.append(RegularCommand(('Group', 'Create'), self.group_create, check_refs=False))
        self.commands.append(RegularCommand(('Group', 'Display'), self.group_display))
        self.commands.append(RegularCommand(('Group', 'Query'), self.group_query))
        self.commands.append(RegularCommand(('Group', 'Remove'), self.group_remove))
        self.commands.append(RegularCommand(('Group', 'Label'), self.group_label))
        self.commands.append(NoRefsCommand(('Metadata', 'About'), self.metadata_about))
        self.commands.append(NoRefsCommand(('Metadata', 'Set'), self.metadata_set))
        self.commands.append(RegularCommand(('AllPalette', 'About'), self.palette_all_about))
        self.commands.append(RegularCommand(('AllPalette', 'CopyTo'), self.palette_all_clone))
        self.commands.append(RegularCommand(('AllPalette', 'Create'), self.palette_all_create, check_refs=False))
        self.commands.append(RegularCommand(('AllPalette', 'Display'), self.palette_all_display))
        self.commands.append(RegularCommand(('AllPalette', 'Remove'), self.palette_all_remove))
        self.commands.append(RegularCommand(('AllPalette', 'Label'), self.palette_all_label))
        self.commands.append(RegularCommand(('BeamPalette', 'About'), self.palette_beam_about))
        self.commands.append(RegularCommand(('BeamPalette', 'CopyTo'), self.palette_beam_clone))
        self.commands.append(RegularCommand(('BeamPalette', 'Create'), self.palette_beam_create, check_refs=False))
        self.commands.append(RegularCommand(('BeamPalette', 'Display'), self.palette_beam_display))
        self.commands.append(RegularCommand(('BeamPalette', 'Remove'), self.palette_beam_remove))
        self.commands.append(RegularCommand(('BeamPalette', 'Label'), self.palette_beam_label))
        self.commands.append(RegularCommand(('ColourPalette', 'About'), self.palette_colour_about))
        self.commands.append(RegularCommand(('ColourPalette', 'CopyTo'), self.palette_colour_clone))
        self.commands.append(RegularCommand(('ColourPalette', 'Create'), self.palette_colour_create, check_refs=False))
        self.commands.append(RegularCommand(('ColourPalette', 'Display'), self.palette_colour_display))
        self.commands.append(RegularCommand(('ColourPalette', 'Remove'), self.palette_colour_remove))
        self.commands.append(RegularCommand(('ColourPalette', 'Label'), self.palette_colour_label))
        self.commands.append(RegularCommand(('FocusPalette', 'About'), self.palette_focus_about))
        self.commands.append(RegularCommand(('FocusPalette', 'CopyTo'), self.palette_focus_clone))
        self.commands.append(RegularCommand(('FocusPalette', 'Create'), self.palette_focus_create, check_refs=False))
        self.commands.append(RegularCommand(('FocusPalette', 'Display'), self.palette_focus_display))
        self.commands.append(RegularCommand(('FocusPalette', 'Remove'), self.palette_focus_remove))
        self.commands.append(RegularCommand(('FocusPalette', 'Label'), self.palette_focus_label))
        self.commands.append(RegularCommand(('IntensityPalette', 'About'), self.palette_intensity_about))
        self.commands.append(RegularCommand(('IntensityPalette', 'CopyTo'), self.palette_intensity_clone))
        self.commands.append(RegularCommand(('IntensityPalette', 'Create'), self.palette_intensity_create, check_refs=False))
        self.commands.append(RegularCommand(('IntensityPalette', 'Display'), self.palette_intensity_display))
        self.commands.append(RegularCommand(('IntensityPalette', 'Remove'), self.palette_intensity_remove))
        self.commands.append(RegularCommand(('IntensityPalette', 'Label'), self.palette_intensity_label))
        self.commands.append(RegularCommand(('Registry', 'About'), self.registry_about))
        self.commands.append(RegularCommand(('Registry', 'Create'), self.registry_create, check_refs=False))
        self.commands.append(RegularCommand(('Registry', 'Display'), self.registry_display))
        self.commands.append(RegularCommand(('Registry', 'Query'), self.registry_query))
        self.commands.append(RegularCommand(('Registry', 'Remove'), self.registry_remove))
        self.commands.append(RegularCommand(('Structure', 'About'), self.structure_about))
        self.commands.append(RegularCommand(('Structure', 'Create'), self.structure_create, check_refs=False))
        self.commands.append(RegularCommand(('Structure', 'CopyTo'), self.structure_clone))
        self.commands.append(RegularCommand(('Structure', 'Display'), self.structure_display))
        self.commands.append(RegularCommand(('Structure', 'Fan'), self.structure_fan))
        self.commands.append(RegularCommand(('Structure', 'Label'), self.structure_label))
        self.commands.append(RegularCommand(('Structure', 'Set'), self.structure_set))
        self.commands.append(RegularCommand(('Structure', 'Remove'), self.structure_remove))

    def _base_about(self, refs, obj_type):
        for r in refs:
            obj = self.file.get_by_ref(obj_type, r)
            self.post_output([obj.get_text_widget()])
            if not hasattr(obj, 'data'):
                self.post_output(['No data dictionary present'])
                continue
            self.post_output([str(len(obj.data))+' Data Tags:'])
            self.post_output(
                [str(k)+': '+str(v) for k, v in sorted(obj.data.items()) if k not in
                 literal_eval(self.interpreter.config['cli']['ignore-about-tags'])],
                indentation=1)

    def _base_clone(self, refs, obj_type, dest):
        """Copy range to single (expanded to range) or copy single to range. If given a single source and single
        destination, just copy the object. If single source and range of destinations, copy the source to all
        destinations as determined by resolve_references. If range source and single destination, copy the first in
        the source to the destination point, then increment at the same intervals from the source and destination."""
        dest_refs = clihelper.resolve_references(dest)
        if len(refs) > 1 and len(dest_refs) > 1:
            self.post_feedback(exception.ERROR_MSG_OVERLAPPING_RANGE)
        elif len(refs) == 1 and len(dest_refs) >= 1:
            src_obj = self.file.get_by_ref(obj_type, refs[0])
            for dest_ref in dest_refs:
                try:
                    self.file.duplicate_object(src_obj, dest_ref)
                except exception.ObjectAlreadyExistsError as e:
                    self.post_feedback(exception.ERROR_MSG_EXISTING_OBJECT.format(e.obj_type, e.ref))
        elif len(refs) > 1 and len(dest_refs) == 1:
            for r in refs:
                dest_ref = str(decimal.Decimal(dest_refs[0])
                               + decimal.Decimal(r)
                               - decimal.Decimal(refs[0]))
                src_obj = self.file.get_by_ref(obj_type, r)
                try:
                    self.file.duplicate_object(src_obj, dest_ref)
                except exception.ObjectAlreadyExistsError as e:
                    self.post_feedback(exception.ERROR_MSG_EXISTING_OBJECT.format(e.obj_type, e.ref))

    def _base_create(self, refs, obj_type, **kwargs):
        """Create new objects."""
        for r in refs:
            if self.file.get_by_ref(obj_type, r):
                self.post_feedback(exception.ERROR_MSG_EXISTING_OBJECT.format(obj_type, str(r)))
                continue
            self.file.insert_object(obj_type(ref=Decimal(r), **kwargs))

    def _base_display(self, refs, obj_type):
        """Print a single-line summary of a range of objects."""
        for r in refs:
            obj = self.file.get_by_ref(obj_type, r)
            self.post_output([obj.get_text_widget()])

    def _base_fan(self, refs, obj_type, k, v_0, v_n):
        """Apply values to object key linearly from v_0 to v_n."""
        if obj_type.__base__ is not document.ArbitraryDataObject:
            self.post_feedback([obj_type.command_str + ' does not support arbitrary data tags'])
            return
        try:
            v_0 = float(v_0)
            v_n = float(v_n)
        except ValueError:
            self.post_feedback(
                'Values could not be applied. Fan requires numerical start and end values.')
            return
        v_i = v_0
        incr = (v_n - v_0) / (len(refs) - 1)
        for r in refs:
            self.file.get_by_ref(obj_type, r).data[k] = str(v_i)
            v_i += incr

    def _base_label(self, refs, obj_type, label):
        """Set the label attribute for an object."""
        for r in refs:
            obj = self.file.get_by_ref(obj_type, r)
            obj.label = label

    def _base_levels_query(self, refs, obj_type, nips=True):
        """See the stored level values of all parameter types. Works with objects that
        use the levels key. Set nips to False to only show intensity values."""
        for r in refs:
            obj = self.file.get_by_ref(obj_type, r)
            if not hasattr(obj, 'levels'):
                self.post_feedback([obj_type.command_str + ' does not support levels query'])
                continue
            self.post_output([obj.get_text_widget()])
            for level in obj.levels:
                func = self.file.get_function_by_uuid(level.function)
                fix = self.file.get_function_parent(func)
                if func.parameter == self.interpreter.config['cli']['dimmer-attribute-name'] or nips:
                    level_str = printer.get_pretty_level_string(
                        str(level.value), doc=self.file,
                        show_labels=self.interpreter.config['cli'].getboolean('show-reference-labels'),
                        raw_data=self.interpreter.config['cli'].getboolean('show-raw-data'), function=func)
                    self.post_output([
                        [printer.get_generic_ref(fix), ':'] +
                        func.get_text_widget() + [': ', level_str]])

    def _base_remove(self, refs, obj_type):
        """Remove an object from the document."""
        for r in refs:
            self.file.remove_object(self.file.get_by_ref(obj_type, r))

    def _base_set(self, refs, obj_type, k, v=None):
        """Set an arbitrary data tag to a value."""
        if obj_type.__base__ is not document.ArbitraryDataObject:
            self.post_feedback([
                obj_type.command_str + ' does not support arbitrary data tags'
            ])
            return
        if not v:
            for r in refs:
                self.file.get_by_ref(obj_type, r).data.pop(k, None)
        else:
            for r in refs:
                self.file.get_by_ref(obj_type, r).data[k] = v

    def cue_about(self, refs):
        """Show stored intensity data for a cue."""
        return self._base_levels_query(refs, document.Cue, nips=False)

    def cue_clone(self, refs, dest):
        """Clone a cue."""
        return self._base_clone(refs, document.Cue, dest)

    def cue_create(self, refs):
        """Create a blank cue."""
        return self._base_create(refs, document.Cue)

    def cue_display(self, refs):
        """Show a single line summary of a cue."""
        return self._base_display(refs, document.Cue)

    def cue_label(self, refs, label):
        """Label a cue."""
        return self._base_label(refs, document.Cue, label)

    def cue_query(self, refs):
        """Show stored intensity and non-intensity data for a cue."""
        return self._base_levels_query(refs, document.Cue)

    def cue_remove(self, refs):
        """Remove a cue."""
        return self._base_remove(refs, document.Cue)

    def cue_set(self, refs, k, v=None):
        """Set an arbitrary data tag in a cue."""
        return self._base_set(refs, document.Cue, k, v)

    def cue_setintens(self, refs, fix_refs, level):
        """Set the level of a fixture's Intens function in a cue."""
        frefs = clihelper.safe_resolve_dec_references_with_filters(self.file, document.Fixture, fix_refs)
        for r in refs:
            cue = self.file.get_by_ref(document.Cue, r)
            for fref in frefs:
                fix = self.file.get_by_ref(document.Fixture, fref)
                intens_func = fix.get_dimmer_function()
                if intens_func:
                    cue.levels[intens_func['uuid']] = level

    def filter_clone(self, refs, dest):
        """Clone a filter."""
        return self._base_clone(refs, document.Filter, dest)

    def filter_create(self, refs, key, value):
        """Create a new filter with given parameters."""
        return self._base_create(refs, document.Filter, key=key, value=value)

    def filter_remove(self, refs):
        """Remove a filter."""
        return self._base_remove(refs, document.Filter)

    def fixture_about(self, refs):
        """Display data tags and DMX functions of a fixture."""
        for r in refs:
            fix = self.file.get_by_ref(document.Fixture, r)
            self.post_output([fix.get_text_widget()])
            self.post_output([str(len(fix.data))+' Data Tags:'])
            ignored_tags = literal_eval(self.interpreter.config['cli']['ignore-about-tags'])
            self.post_output(
                [str(k)+': '+str(v) for k, v in sorted(fix.data.items()) if
                 k not in ignored_tags], indentation=1)
            if not fix.functions:
                continue
            self.post_output([[str(len(fix.functions)), ' DMX Functions:']])
            for func in fix.functions:
                self.post_output([func.get_text_widget()], indentation=1)

    def fixture_clone(self, refs, dest):
        """Clone a fixture to a destination(s)"""
        return self._base_clone(refs, document.Fixture, dest)

    def fixture_create(self, refs):
        """Create a blank fixture."""
        return self._base_create(refs, document.Fixture)

    def fixture_display(self, refs):
        """Show a single line summary of a fixture."""
        return self._base_display(refs, document.Fixture)

    def fixture_fan(self, refs, k, v_0, v_n):
        """Set tags across a range of fixtures to a range of values."""
        return self._base_fan(refs, document.Fixture, k, v_0, v_n)

    def fixture_patch(self, refs, univ, addr=None):
        """Patch the functions of a fixture in a registry. Omit address 
        to patch automatically from first available address."""
        reg = self.file.get_by_ref(document.Registry, Decimal(univ))
        try:
            addr = int(addr)
        except TypeError:
            pass
        if not reg:
            self.registry_create([Decimal(univ)])
            self.file.get_by_ref(document.Registry, Decimal(univ))
        for r in refs:
            fix = self.file.get_by_ref(document.Fixture, r)
            try:
                reg.patch_fixture(fix, addr)
            except exception.InsufficientAvailableChannels:
                self.post_feedback(exception.ERROR_MSG_UNIVERSE_SPACE.format(str(univ)))
                return
            if addr:
                addr += fix.dmx_size()

    def fixture_remove(self, refs):
        """Remove a fixture."""
        self.fixture_unpatch(refs)
        return self._base_remove(refs, document.Fixture)

    def fixture_set(self, refs, k, v=None):
        """Set an arbitrary data tag in a fixture."""
        return self._base_set(refs, document.Fixture, k, v)

    def fixture_unpatch(self, refs):
        """Remove all of a fixture's functions from all registries."""
        for r in refs:
            fix = self.file.get_by_ref(document.Fixture, r)
            self.file.unpatch_fixture_from_all(fix)

    def group_about(self, refs):
        """Display the contents of a group."""
        for r in refs:
            grp = self.file.get_by_ref(document.Group, r)
            self.post_output([
                grp.get_text_widget(),
                ', '.join([str(i.ref) for i in grp.fixtures])])

    def group_append_fixture(self, refs, frefs):
        """Append a fixture to a group list."""
        for r in refs:
            group = self.file.get_by_ref(document.Group, r)
            for fref in clihelper.safe_resolve_dec_references_with_filters(self.file, document.Fixture, frefs):
                fix = self.file.get_by_ref(document.Fixture, fref)
                group.append_fixture(fix)

    def group_clone(self, refs, dest):
        """Clone a group."""
        return self._base_clone(refs, document.Group, dest)

    def group_create(self, refs):
        """Create an empty group."""
        return self._base_create(refs, document.Group)

    def group_display(self, refs):
        """Show a single line summary of a group."""
        return self._base_display(refs, document.Group)

    def group_query(self, refs):
        """Show the used fixtures in a group, and also give a summary of each fixture."""
        for r in refs:
            grp = self.file.get_by_ref(document.Group, r)
            self.post_output([grp.get_text_widget()])
            for fix in grp.fixtures:
                self.post_output([fix.get_text_widget()], indentation=1)

    def group_remove(self, refs):
        """Remove a group."""
        return self._base_remove(refs, document.Group)

    def group_label(self, refs, label):
        """Set the label of a group."""
        return self._base_label(refs, document.Group, label)

    def metadata_about(self):
        """Show the values of all stored metadata."""
        self.post_output([str(len(self.file.metadata)) + ' Metadata Tags:'])
        for k, v in self.file.metadata.items():
            self.post_output([printer.get_metadata_string(k, v)])

    def metadata_set(self, k, v=None):
        """Set the value of a metadata tag. If no value is given, delete the tag."""
        if v:
            self.file.metadata[k] = v
        else:
            del self.file.metadata[k]

    def palette_all_clone(self, refs, dest):
        """Clone an all palette."""
        return self._base_clone(refs, document.AllPalette, dest)

    def palette_beam_clone(self, refs, dest):
        """Clone a beam palette."""
        return self._base_clone(refs, document.BeamPalette, dest)

    def palette_colour_clone(self, refs, dest):
        """Clone a colour palette."""
        return self._base_clone(refs, document.ColourPalette, dest)

    def palette_focus_clone(self, refs, dest):
        """Clone a focus palette."""
        return self._base_clone(refs, document.FocusPalette, dest)

    def palette_intensity_clone(self, refs, dest):
        """Clone an intensity palette."""
        return self._base_clone(refs, document.IntensityPalette, dest)

    def palette_all_create(self, refs):
        """Create an empty all palette (preset)."""
        return self._base_create(refs, document.AllPalette)

    def palette_beam_create(self, refs):
        """Create an empty beam palette."""
        return self._base_create(refs, document.BeamPalette)

    def palette_colour_create(self, refs):
        """Create an empty colour palette."""
        return self._base_create(refs, document.ColourPalette)

    def palette_focus_create(self, refs):
        """Create an empty focus palette."""
        return self._base_create(refs, document.FocusPalette)

    def palette_intensity_create(self, refs):
        """Create an empty intensity palette."""
        return self._base_create(refs, document.IntensityPalette)

    def palette_all_display(self, refs):
        """Show a single line summary of an all palette."""
        return self._base_display(refs, document.AllPalette)

    def palette_beam_display(self, refs):
        """Show a single line summary of a beam palette."""
        return self._base_display(refs, document.BeamPalette)

    def palette_colour_display(self, refs):
        """Show a single line summary of a colour palette."""
        return self._base_display(refs, document.ColourPalette)

    def palette_focus_display(self, refs):
        """Show a single line summary of a focus palette."""
        return self._base_display(refs, document.FocusPalette)

    def palette_intensity_display(self, refs):
        """Show a single line summary of an intensity palette."""
        return self._base_display(refs, document.IntensityPalette)

    def palette_all_about(self, refs):
        """Show the stored values in an all palette."""
        return self._base_levels_query(refs, document.AllPalette)

    def palette_beam_about(self, refs):
        """Show the stored values in a beam palette."""
        return self._base_levels_query(refs, document.BeamPalette)

    def palette_colour_about(self, refs):
        """Show the stored values in a colour palette."""
        return self._base_levels_query(refs, document.ColourPalette)

    def palette_focus_about(self, refs):
        """Show the stored values in a focus palette."""
        return self._base_levels_query(refs, document.FocusPalette)

    def palette_intensity_about(self, refs):
        """Show the stored values in an intensity palette."""
        return self._base_levels_query(refs, document.IntensityPalette)

    def palette_all_remove(self, refs):
        """Remove an all palette."""
        return self._base_remove(refs, document.AllPalette)

    def palette_beam_remove(self, refs):
        """Remove a beam palette."""
        return self._base_remove(refs, document.BeamPalette)

    def palette_colour_remove(self, refs):
        """Remove a colour palette."""
        return self._base_remove(refs, document.ColourPalette)

    def palette_focus_remove(self, refs):
        """Remove a focus palette."""
        return self._base_remove(refs, document.FocusPalette)

    def palette_intensity_remove(self, refs):
        """Remove an intensity palette."""
        return self._base_remove(refs, document.IntensityPalette)

    def palette_all_label(self, refs, label):
        """Set the label of an all palette."""
        return self._base_label(refs, document.AllPalette, label)

    def palette_beam_label(self, refs, label):
        """Set the label of a beam palette."""
        return self._base_label(refs, document.BeamPalette, label)

    def palette_colour_label(self, refs, label):
        """Set the label of a colour palette."""
        return self._base_label(refs, document.ColourPalette, label)

    def palette_focus_label(self, refs, label):
        """Set the label of a focus palette."""
        return self._base_label(refs, document.FocusPalette, label)

    def palette_intensity_label(self, refs, label):
        """Set the label of an intensity palette."""
        return self._base_label(refs, document.IntensityPalette, label)

    def registry_about(self, refs):
        """Show a summary of the used addresses in a registry but do not provide any further information."""
        for r in refs:
            reg = self.file.get_by_ref(document.Registry, r)
            self.post_output([reg.get_text_widget()])
            table = []
            current_row = ['   ']
            width = int(self.interpreter.config['cli']['registry-summary-width'])
            for i in range(0, width):
                current_row += [' ', str(format(i, '02d'))]
            for i in range(1, 514):
                if i % width == 1 or i == 513:
                    table.append(current_row)
                    current_row = [str(format(i, '03d')), '  ']
                if str(i) in reg.table or i in reg.table:
                    current_row.append(('error', '#  '))
                else:
                    current_row.append(('success', '-  '))
            self.post_output(table)

    def registry_create(self, refs):
        """Insert a blank registry."""
        return self._base_create(refs, document.Registry)

    def registry_display(self, refs):
        """Display a single-line summary of a registry."""
        return self._base_display(refs, document.Registry)

    def registry_query(self, refs):
        """Show all used addresses in a registry and the functions they are occupied by."""
        for r in refs:
            reg = self.file.get_by_ref(document.Registry, r)
            self.post_output([reg.get_text_widget()])
            for addr, uuid in sorted(reg.table.items()):
                func = self.file.get_function_by_uuid(uuid)
                fix = self.file.get_function_parent(func)
                self.post_output([['DMX', str(format(addr, '03d')), ': '] +
                                  fix.get_text_widget() + [' ('] +
                                  func.get_text_widget() + [')']])

    def registry_remove(self, refs):
        """Remove a registry."""
        return self._base_remove(refs, document.Registry)

    def structure_about(self, refs):
        """Show the stored data tags of a structure."""
        return self._base_about(refs, document.Structure)

    def structure_clone(self, refs, dest):
        """Clone a structure."""
        return self._base_clone(refs, document.Structure, dest)

    def structure_create(self, refs, structure_type=None):
        """Insert a blank structure object."""
        return self._base_create(refs, document.Structure,
                                 structure_type=structure_type)

    def structure_display(self, refs):
        """Display a single-line summary of a structure."""
        return self._base_display(refs, document.Structure)

    def structure_fan(self, refs, k, v_0, v_n):
        """Set tags across a range of fixtures to a range of values."""
        return self._base_fan(refs, document.Structure, k, v_0, v_n)

    def structure_label(self, refs, label):
        """Set the label of a structure."""
        return self._base_label(refs, document.Structure, label)

    def structure_remove(self, refs):
        """Remove a structure."""
        return self._base_remove(refs, document.Structure)

    def structure_set(self, refs, k, v=None):
        """Set an arbitrary data tag in a structure."""
        return self._base_set(refs, document.Structure, k, v)


def register_extension(interpreter):
    BaseExtension(interpreter).register_extension()
