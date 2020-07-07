from ast import literal_eval
from pylux.interpreter import RegularCommand, InterpreterExtension, NoRefsCommand
from pylux import clihelper, document
from pylux.lib import printer, exception
import pylux.lib.keyword as kw
import decimal
from decimal import Decimal


class BaseExtension(InterpreterExtension):

    def register_commands(self):
        self.commands.append(RegularCommand((kw.CUE, kw.ABOUT), self.cue_about))
        self.commands.append(RegularCommand((kw.CUE, kw.CLONE), self.cue_clone))
        self.commands.append(RegularCommand((kw.CUE, kw.CREATE), self.cue_create, check_refs=False))
        self.commands.append(RegularCommand((kw.CUE, kw.DISPLAY), self.cue_display))
        self.commands.append(RegularCommand((kw.CUE, kw.LABEL), self.cue_label))
        self.commands.append(RegularCommand((kw.CUE, kw.QUERY), self.cue_query))
        self.commands.append(RegularCommand((kw.CUE, kw.REMOVE), self.cue_remove))
        self.commands.append(RegularCommand((kw.CUE, kw.SET), self.cue_set))
        self.commands.append(RegularCommand((kw.FILTER, kw.CLONE), self.filter_clone))
        self.commands.append(RegularCommand((kw.FILTER, kw.CREATE), self.filter_create, check_refs=False))
        self.commands.append(RegularCommand((kw.FILTER, kw.REMOVE), self.filter_remove))
        self.commands.append(RegularCommand((kw.FIXTURE, kw.ABOUT), self.fixture_about))
        self.commands.append(RegularCommand((kw.FIXTURE, kw.CREATE), self.fixture_create, check_refs=False))
        self.commands.append(RegularCommand((kw.FIXTURE, kw.CLONE), self.fixture_clone))
        self.commands.append(RegularCommand((kw.FIXTURE, kw.DISPLAY), self.fixture_display))
        self.commands.append(RegularCommand((kw.FIXTURE, kw.FAN), self.fixture_fan))
        self.commands.append(RegularCommand((kw.FIXTURE, kw.PATCH), self.fixture_patch))
        self.commands.append(RegularCommand((kw.FIXTURE, kw.REMOVE), self.fixture_remove))
        self.commands.append(RegularCommand((kw.FIXTURE, kw.SET), self.fixture_set))
        self.commands.append(RegularCommand((kw.FIXTURE, kw.UNPATCH), self.fixture_unpatch))
        self.commands.append(RegularCommand((kw.GROUP, kw.ABOUT), self.group_about))
        self.commands.append(RegularCommand((kw.GROUP, kw.APPEND), self.group_append_fixture))
        self.commands.append(RegularCommand((kw.GROUP, kw.CLONE), self.group_clone))
        self.commands.append(RegularCommand((kw.GROUP, kw.CREATE), self.group_create, check_refs=False))
        self.commands.append(RegularCommand((kw.GROUP, kw.DISPLAY), self.group_display))
        self.commands.append(RegularCommand((kw.GROUP, kw.QUERY), self.group_query))
        self.commands.append(RegularCommand((kw.GROUP, kw.REMOVE), self.group_remove))
        self.commands.append(RegularCommand((kw.GROUP, kw.LABEL), self.group_label))
        self.commands.append(NoRefsCommand((kw.META, kw.ABOUT), self.metadata_about))
        self.commands.append(NoRefsCommand((kw.META, kw.SET), self.metadata_set))
        self.commands.append(RegularCommand((kw.ALL_PALETTE, kw.ABOUT), self.palette_all_about))
        self.commands.append(RegularCommand((kw.ALL_PALETTE, kw.CLONE), self.palette_all_clone))
        self.commands.append(RegularCommand((kw.ALL_PALETTE, kw.CREATE), self.palette_all_create, check_refs=False))
        self.commands.append(RegularCommand((kw.ALL_PALETTE, kw.DISPLAY), self.palette_all_display))
        self.commands.append(RegularCommand((kw.ALL_PALETTE, kw.REMOVE), self.palette_all_remove))
        self.commands.append(RegularCommand((kw.ALL_PALETTE, kw.LABEL), self.palette_all_label))
        self.commands.append(RegularCommand((kw.BEAM_PALETTE, kw.ABOUT), self.palette_beam_about))
        self.commands.append(RegularCommand((kw.BEAM_PALETTE, kw.CLONE), self.palette_beam_clone))
        self.commands.append(RegularCommand((kw.BEAM_PALETTE, kw.CREATE), self.palette_beam_create, check_refs=False))
        self.commands.append(RegularCommand((kw.BEAM_PALETTE, kw.DISPLAY), self.palette_beam_display))
        self.commands.append(RegularCommand((kw.BEAM_PALETTE, kw.REMOVE), self.palette_beam_remove))
        self.commands.append(RegularCommand((kw.BEAM_PALETTE, kw.LABEL), self.palette_beam_label))
        self.commands.append(RegularCommand((kw.COLOUR_PALETTE, kw.ABOUT), self.palette_colour_about))
        self.commands.append(RegularCommand((kw.COLOUR_PALETTE, kw.CLONE), self.palette_colour_clone))
        self.commands.append(RegularCommand((kw.COLOUR_PALETTE, kw.CREATE), self.palette_colour_create, check_refs=False))
        self.commands.append(RegularCommand((kw.COLOUR_PALETTE, kw.DISPLAY), self.palette_colour_display))
        self.commands.append(RegularCommand((kw.COLOUR_PALETTE, kw.REMOVE), self.palette_colour_remove))
        self.commands.append(RegularCommand((kw.COLOUR_PALETTE, kw.LABEL), self.palette_colour_label))
        self.commands.append(RegularCommand((kw.FOCUS_PALETTE, kw.ABOUT), self.palette_focus_about))
        self.commands.append(RegularCommand((kw.FOCUS_PALETTE, kw.CLONE), self.palette_focus_clone))
        self.commands.append(RegularCommand((kw.FOCUS_PALETTE, kw.CREATE), self.palette_focus_create, check_refs=False))
        self.commands.append(RegularCommand((kw.FOCUS_PALETTE, kw.DISPLAY), self.palette_focus_display))
        self.commands.append(RegularCommand((kw.FOCUS_PALETTE, kw.REMOVE), self.palette_focus_remove))
        self.commands.append(RegularCommand((kw.FOCUS_PALETTE, kw.LABEL), self.palette_focus_label))
        self.commands.append(RegularCommand((kw.INTENSITY_PALETTE, kw.ABOUT), self.palette_intensity_about))
        self.commands.append(RegularCommand((kw.INTENSITY_PALETTE, kw.CLONE), self.palette_intensity_clone))
        self.commands.append(RegularCommand((kw.INTENSITY_PALETTE, kw.CREATE), self.palette_intensity_create, check_refs=False))
        self.commands.append(RegularCommand((kw.INTENSITY_PALETTE, kw.DISPLAY), self.palette_intensity_display))
        self.commands.append(RegularCommand((kw.INTENSITY_PALETTE, kw.REMOVE), self.palette_intensity_remove))
        self.commands.append(RegularCommand((kw.INTENSITY_PALETTE, kw.LABEL), self.palette_intensity_label))
        self.commands.append(RegularCommand((kw.REGISTRY, kw.ABOUT), self.registry_about))
        self.commands.append(RegularCommand((kw.REGISTRY, kw.CREATE), self.registry_create, check_refs=False))
        self.commands.append(RegularCommand((kw.REGISTRY, kw.DISPLAY), self.registry_display))
        self.commands.append(RegularCommand((kw.REGISTRY, kw.QUERY), self.registry_query))
        self.commands.append(RegularCommand((kw.REGISTRY, kw.REMOVE), self.registry_remove))
        self.commands.append(RegularCommand((kw.STRUCTURE, kw.ABOUT), self.structure_about))
        self.commands.append(RegularCommand((kw.STRUCTURE, kw.CREATE), self.structure_create, check_refs=False))
        self.commands.append(RegularCommand((kw.STRUCTURE, kw.CLONE), self.structure_clone))
        self.commands.append(RegularCommand((kw.STRUCTURE, kw.DISPLAY), self.structure_display))
        self.commands.append(RegularCommand((kw.STRUCTURE, kw.FAN), self.structure_fan))
        self.commands.append(RegularCommand((kw.STRUCTURE, kw.LABEL), self.structure_label))
        self.commands.append(RegularCommand((kw.STRUCTURE, kw.SET), self.structure_set))
        self.commands.append(RegularCommand((kw.STRUCTURE, kw.REMOVE), self.structure_remove))

    def _base_about(self, objs):
        for obj in objs:
            self.post_output([obj.get_text_widget()])
            if not hasattr(obj, 'data'):
                self.post_output(['No data dictionary present'])
                continue
            self.post_output([str(len(obj.data))+' Data Tags:'])
            self.post_output(
                [str(k)+': '+str(v) for k, v in sorted(obj.data.items()) if k not in
                 literal_eval(self.interpreter.config['cli']['ignore-about-tags'])],
                indentation=1)

    def _base_clone(self, objs, dest):
        """Copy range to single (expanded to range) or copy single to range. If given a single source and single
        destination, just copy the object. If single source and range of destinations, copy the source to all
        destinations as determined by resolve_references. If range source and single destination, copy the first in
        the source to the destination point, then increment at the same intervals from the source and destination."""
        dest_refs = clihelper.resolve_references(dest)
        # Clone cannot support more than one source object and more than one
        # destination object at the same time
        if len(objs) > 1 and len(dest_refs) > 1:
            self.post_feedback(exception.ERROR_MSG_OVERLAPPING_RANGE)
        # If there is one source object and one or more destination object,
        # duplicates are made at whole number intervals in the destination range
        elif len(objs) == 1 and len(dest_refs) >= 1:
            src_obj = objs[0]
            for dest_ref in dest_refs:
                try:
                    self.file.duplicate_object(src_obj, dest_ref)
                except exception.ObjectAlreadyExistsError as e:
                    self.post_feedback(exception.ERROR_MSG_EXISTING_OBJECT.format(e.obj_type, e.ref))
        # If there are multiple source objects and only one destination object,
        # the first source object is duplicated at the destination ref. Then, for
        # each following source object, the destination ref is incremented by the
        # same amount as the difference between the current and previous source
        # objects. For example, if the sources are 1,2,5,7 and the given
        # destination is 9, the used destinations will be 9,10,13,15
        elif len(objs) > 1 and len(dest_refs) == 1:
            for src_obj in objs:
                dest_ref = decimal.Decimal(dest_refs[0]) + decimal.Decimal(src_obj.ref) - decimal.Decimal(objs[0].ref)
                # Unlike for a single-source clone command, this requires us to
                # fetch a new source object on every iteration
                try:
                    self.file.duplicate_object(src_obj, dest_ref)
                except exception.ObjectAlreadyExistsError as e:
                    self.post_feedback(exception.ERROR_MSG_EXISTING_OBJECT.format(e.obj_type, e.ref))

    def _base_create(self, refs, obj_type, allow_autoref=True, **kwargs):
        """Create new objects."""
        for r in refs:
            if self.file.get_by_ref(obj_type, r):
                self.post_feedback(exception.ERROR_MSG_EXISTING_OBJECT.format(obj_type.noun, str(r)))
                continue
            # If ref is zero, use automatically assigned ref. If autoref is not
            # allowed, then an object will be created at ref zero
            if r == 0 and allow_autoref:
                r = self.file.next_ref(obj_type)
            self.file.insert_object(obj_type(ref=Decimal(r), **kwargs))

    def _base_display(self, objs):
        """Print a single-line summary of a range of objects."""
        for obj in objs:
            self.post_output([obj.get_text_widget()])

    def _base_fan(self, objs, k, v_0, v_n):
        """Apply values to object key linearly from v_0 to v_n."""
        try:
            v_0 = float(v_0)
            v_n = float(v_n)
        except ValueError:
            self.post_feedback(exception.ERROR_MSG_FAN_VALUES)
            return
        v_i = v_0
        incr = (v_n - v_0) / (len(objs) - 1)
        for obj in objs:
            if type(obj).__base__ is not document.ArbitraryDataObject:
                self.post_feedback(exception.ERROR_MSG_UNSUPPORTED_DATA.format(obj.noun))
                continue
            obj.data[k] = str(v_i)
            v_i += incr

    def _base_label(self, objs, label):
        """Set the label attribute for an object."""
        for obj in objs:
            obj.label = label

    def _base_levels_query(self, objs, nips=True):
        """See the stored level values of all parameter types. Works with objects that
        use the levels key. Set nips to False to only show intensity values."""
        for obj in objs:
            if not hasattr(obj, 'levels'):
                self.post_feedback([obj.noun + ' does not support levels query'])
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

    def _base_remove(self, objs):
        """Remove an object from the document."""
        for obj in objs:
            self.file.remove_object(obj)

    def _base_set(self, objs, k, v=None):
        """Set an arbitrary data tag to a value."""
        for obj in objs:
            if type(obj).__base__ is not document.ArbitraryDataObject:
                self.post_feedback(exception.ERROR_MSG_UNSUPPORTED_DATA.format(obj.noun))
                return
            if not v:
                obj.data.pop(k, None)
            else:
                obj.data[k] = v

    def cue_about(self, cues):
        """Show stored intensity data for a cue."""
        return self._base_about(cues)

    def cue_clone(self, cues, dest):
        """Clone a cue."""
        return self._base_clone(cues, dest)

    def cue_create(self, refs):
        """Create a blank cue."""
        return self._base_create(refs, document.Cue)

    def cue_display(self, cues):
        """Show a single line summary of a cue."""
        return self._base_display(cues)

    def cue_label(self, cues, label):
        """Label a cue."""
        return self._base_label(cues, label)

    def cue_query(self, cues, flags=None):
        """Show stored level data for a cue. Add flag n to only show
        intensity parameter data."""
        if not flags:
            return self._base_levels_query(cues)
        if 'n' in flags:
            return self._base_levels_query(cues, nips=False)
        else:
            return self._base_levels_query(cues)

    def cue_remove(self, cues):
        """Remove a cue."""
        return self._base_remove(cues)

    def cue_set(self, cues, k, v=None):
        """Set an arbitrary data tag in a cue."""
        return self._base_set(cues, k, v)

    def filter_clone(self, filters, dest):
        """Clone a filter."""
        return self._base_clone(filters, dest)

    def filter_create(self, refs, key, value):
        """Create a new filter with given parameters."""
        return self._base_create(refs, document.Filter, key=key, value=value)

    def filter_remove(self, filters):
        """Remove a filter."""
        return self._base_remove(filters)

    def fixture_about(self, fixtures):
        """Display data tags and DMX functions of a fixture."""
        for obj in fixtures:
            self._base_about([obj])
            if not obj.functions:
                continue
            self.post_output([[str(len(obj.functions)), ' DMX Functions:']])
            for func in obj.functions:
                self.post_output([func.get_text_widget()], indentation=1)

    def fixture_clone(self, fixtures, dest):
        """Clone a fixture to a destination(s)"""
        return self._base_clone(fixtures, dest)

    def fixture_create(self, refs):
        """Create a blank fixture."""
        return self._base_create(refs, document.Fixture)

    def fixture_display(self, fixtures):
        """Show a single line summary of a fixture."""
        return self._base_display(fixtures)

    def fixture_fan(self, fixtures, k, v_0, v_n):
        """Set tags across a range of fixtures to a range of values."""
        return self._base_fan(fixtures, k, v_0, v_n)

    def fixture_patch(self, fixtures, univ, addr=None):
        """Patch the functions of a fixture in a registry. Omit address 
        to patch automatically from first available address."""
        try:
            addr = int(addr)
        except TypeError:
            pass
        for obj in fixtures:
            self.file.patch_fixture(obj, int(univ), addr)
            if addr:
                addr += obj.dmx_size()

    def fixture_remove(self, fixtures):
        """Remove a fixture."""
        self.fixture_unpatch(fixtures)
        return self._base_remove(fixtures)

    def fixture_set(self, fixtures, k, v=None):
        """Set an arbitrary data tag in a fixture."""
        return self._base_set(fixtures, k, v)

    def fixture_unpatch(self, fixtures):
        """Remove all of a fixture's functions from all registries."""
        for obj in fixtures:
            self.file.unpatch_fixture_from_all(obj)

    def group_about(self, groups):
        """Display the contents of a group."""
        for obj in groups:
            self.post_output([
                obj.get_text_widget(),
                ', '.join([str(i.ref) for i in obj.fixtures])])

    def group_append_fixture(self, groups, fixtures):
        """Append a fixture to a group list."""
        for group in groups:
            for fix in clihelper.match_objects(fixtures, self.file, document.Fixture):
                group.append_fixture(fix)

    def group_clone(self, groups, dest):
        """Clone a group."""
        return self._base_clone(groups, dest)

    def group_create(self, refs):
        """Create an empty group."""
        return self._base_create(refs, document.Group)

    def group_display(self, groups):
        """Show a single line summary of a group."""
        return self._base_display(groups)

    def group_query(self, groups):
        """Show the used fixtures in a group, and also give a summary of each fixture."""
        for grp in groups:
            self.post_output([grp.get_text_widget()])
            for fix in grp.fixtures:
                self.post_output([fix.get_text_widget()], indentation=1)

    def group_remove(self, groups):
        """Remove a group."""
        return self._base_remove(groups)

    def group_label(self, groups, label):
        """Set the label of a group."""
        return self._base_label(groups, label)

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
        return self._base_clone(refs, dest)

    def palette_beam_clone(self, refs, dest):
        """Clone a beam palette."""
        return self._base_clone(refs, dest)

    def palette_colour_clone(self, refs, dest):
        """Clone a colour palette."""
        return self._base_clone(refs, dest)

    def palette_focus_clone(self, refs, dest):
        """Clone a focus palette."""
        return self._base_clone(refs, dest)

    def palette_intensity_clone(self, refs, dest):
        """Clone an intensity palette."""
        return self._base_clone(refs, dest)

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
        return self._base_display(refs)

    def palette_beam_display(self, refs):
        """Show a single line summary of a beam palette."""
        return self._base_display(refs)

    def palette_colour_display(self, refs):
        """Show a single line summary of a colour palette."""
        return self._base_display(refs)

    def palette_focus_display(self, refs):
        """Show a single line summary of a focus palette."""
        return self._base_display(refs)

    def palette_intensity_display(self, refs):
        """Show a single line summary of an intensity palette."""
        return self._base_display(refs)

    def palette_all_about(self, refs):
        """Show the stored values in an all palette."""
        return self._base_levels_query(refs)

    def palette_beam_about(self, refs):
        """Show the stored values in a beam palette."""
        return self._base_levels_query(refs)

    def palette_colour_about(self, refs):
        """Show the stored values in a colour palette."""
        return self._base_levels_query(refs)

    def palette_focus_about(self, refs):
        """Show the stored values in a focus palette."""
        return self._base_levels_query(refs)

    def palette_intensity_about(self, refs):
        """Show the stored values in an intensity palette."""
        return self._base_levels_query(refs)

    def palette_all_remove(self, refs):
        """Remove an all palette."""
        return self._base_remove(refs)

    def palette_beam_remove(self, refs):
        """Remove a beam palette."""
        return self._base_remove(refs)

    def palette_colour_remove(self, refs):
        """Remove a colour palette."""
        return self._base_remove(refs)

    def palette_focus_remove(self, refs):
        """Remove a focus palette."""
        return self._base_remove(refs)

    def palette_intensity_remove(self, refs):
        """Remove an intensity palette."""
        return self._base_remove(refs)

    def palette_all_label(self, refs, label):
        """Set the label of an all palette."""
        return self._base_label(refs, label)

    def palette_beam_label(self, refs, label):
        """Set the label of a beam palette."""
        return self._base_label(refs, label)

    def palette_colour_label(self, refs, label):
        """Set the label of a colour palette."""
        return self._base_label(refs, label)

    def palette_focus_label(self, refs, label):
        """Set the label of a focus palette."""
        return self._base_label(refs, label)

    def palette_intensity_label(self, refs, label):
        """Set the label of an intensity palette."""
        return self._base_label(refs, label)

    def registry_about(self, registries):
        """Show a summary of the used addresses in a registry but do not provide any further information."""
        for reg in registries:
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
        return self._base_create(refs, document.Registry, allow_autoref=False)

    def registry_display(self, registries):
        """Display a single-line summary of a registry."""
        return self._base_display(registries)

    def registry_query(self, registries):
        """Show all used addresses in a registry and the functions they are occupied by."""
        for reg in registries:
            self.post_output([reg.get_text_widget()])
            for addr, uuid in sorted(reg.table.items()):
                func = self.file.get_function_by_uuid(uuid)
                fix = self.file.get_function_parent(func)
                self.post_output([['DMX', str(format(addr, '03d')), ': '] +
                                  fix.get_text_widget() + [' ('] +
                                  func.get_text_widget() + [')']])

    def registry_remove(self, registries):
        """Remove a registry."""
        return self._base_remove(registries)

    def structure_about(self, structures):
        """Show the stored data tags of a structure."""
        return self._base_about(structures)

    def structure_clone(self, structures, dest):
        """Clone a structure."""
        return self._base_clone(structures, dest)

    def structure_create(self, refs, structure_type=None):
        """Insert a blank structure object."""
        return self._base_create(refs, document.Structure,
                                 structure_type=structure_type)

    def structure_display(self, refs):
        """Display a single-line summary of a structure."""
        return self._base_display(refs)

    def structure_fan(self, refs, k, v_0, v_n):
        """Set tags across a range of fixtures to a range of values."""
        return self._base_fan(refs, k, v_0, v_n)

    def structure_label(self, refs, label):
        """Set the label of a structure."""
        return self._base_label(refs, label)

    def structure_remove(self, refs):
        """Remove a structure."""
        return self._base_remove(refs)

    def structure_set(self, refs, k, v=None):
        """Set an arbitrary data tag in a structure."""
        return self._base_set(refs, k, v)


def register_extension(interpreter):
    return BaseExtension(interpreter).register_extension()
