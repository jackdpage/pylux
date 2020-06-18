from pylux.interpreter import InterpreterExtension, NoRefsCommand, Noun, Verb
from pylux import document
from pylux import reference
from pylux.lib import usitt, exception
from decimal import Decimal


class EosExtension(InterpreterExtension):

    def register_commands(self):
        self.commands.append(NoRefsCommand((Noun.FILE, Verb.IMPORT), self.file_importascii))

    def file_importascii(self, file, flag=None):
        if flag == 'overwrite':
            overwrite = True
        else:
            overwrite = False
        ascii_file = usitt.AsciiFile(file)

        for eos_fix in ascii_file.patch:
            ref = Decimal(ascii_file.sortable_chan(eos_fix))
            if self.file.get_by_ref(document.Fixture, ref) and not overwrite:
                self.post_feedback(exception.ERROR_MSG_EXISTING_OBJECT.format(document.Fixture, str(ref)))
                continue
            functions = []
            for func in eos_fix.pers.channels:
                if func.param.long_name in reference.EOS_GDTF_MAP:
                    param_name = reference.EOS_GDTF_MAP[func.param.long_name]
                else:
                    param_name = func.param.long_name
                if func.virtual:
                    offset = None
                else:
                    offset = func.offset[0]
                functions.append(document.FixtureFunction(param_name, offset, func.param_size))
            if self.config['ascii'].getboolean('substitute-delimiters'):
                fixture_type = eos_fix.pers_name.replace('_', ' ')
            else:
                fixture_type = eos_fix.pers_name
            new_fixture = document.Fixture(ref=ref, functions=functions, label=eos_fix.label,
                                           data={'fixture-type': fixture_type})
            if eos_fix.position:
                new_fixture.data['posX'] = str(eos_fix.position[0])
                new_fixture.data['posY'] = str(eos_fix.position[1])
                new_fixture.data['posZ'] = str(eos_fix.position[2])
            if eos_fix.orientation:
                new_fixture.data['rotation'] = str(eos_fix.orientation[2])
            if eos_fix.gel:
                new_fixture.data['gel'] = eos_fix.gel
            self.file.insert_object(new_fixture)
            if eos_fix.address:
                patch_univ = int((eos_fix.address + 1) / 512)
                patch_addr = eos_fix.address % 512
                self.file.patch_fixture(new_fixture, patch_univ, patch_addr)
        for eos_group in ascii_file.groups:
            new_group = document.Group(ref=Decimal(eos_group.id))
            for eos_fix in eos_group.chans:
                fix = self.file.get_by_ref(document.Fixture, Decimal(ascii_file.sortable_chan(eos_fix)))
                new_group.fixtures.append(fix)
            if eos_group.label:
                new_group.label = eos_group.label
            self.file.insert_object(new_group)

        def add_palette(palette_type, ascii_palette):
            new_palette = palette_type(ref=Decimal(ascii_palette.id), label=ascii_palette.label)
            for eos_param in ascii_palette.params:
                try:
                    fix = self.file.get_by_ref(document.Fixture, Decimal(ascii_file.sortable_chan(eos_param.chan)))
                except AttributeError:
                    self.post_feedback(exception.ERROR_MSG_UNPATCHED_FIXTURE.format(
                        str(eos_param.chan_id), new_palette.noun, str(new_palette.ref)))
                    continue
                func_uuid = fix.get_function(
                    reference.EOS_GDTF_MAP.get(eos_param.param.long_name, eos_param.param.long_name)).uuid
                new_palette.levels.append(document.FunctionLevel(func_uuid, eos_param.level))
            self.file.insert_object(new_palette)

        for ip in ascii_file.intensity_palettes:
            add_palette(document.IntensityPalette, ip)
        for fp in ascii_file.focus_palettes:
            add_palette(document.FocusPalette, fp)
        for cp in ascii_file.color_palettes:
            add_palette(document.ColourPalette, cp)
        for bp in ascii_file.beam_palettes:
            add_palette(document.BeamPalette, bp)

        for cue_list in ascii_file.cue_lists:
            for ascii_cue in cue_list.cues:
                new_cue = document.Cue(ref=Decimal(ascii_cue.id), label=ascii_cue.label,
                                       cue_list=int(cue_list.id))
                # Scanning moves, tracked and params are all very similar, there
                # is a lot of repetition here
                for eos_move in ascii_cue.moves:
                    try:
                        fix = self.file.get_by_ref(document.Fixture, Decimal(ascii_file.sortable_chan(eos_move.chan)))
                    except AttributeError:
                        self.post_feedback(exception.ERROR_MSG_UNPATCHED_FIXTURE.format(
                            str(eos_move.chan_id), new_cue.noun, str(new_cue.ref)))
                        continue
                    func_uuid = fix.get_dimmer_function().uuid
                    new_cue.levels.append(document.FunctionLevel(func_uuid, eos_move.level))
                for eos_chan in ascii_cue.tracked:
                    try:
                        fix = self.file.get_by_ref(document.Fixture, Decimal(ascii_file.sortable_chan(eos_chan.chan)))
                    except AttributeError:
                        self.post_feedback(exception.ERROR_MSG_UNPATCHED_FIXTURE.format(
                            str(eos_chan.chan_id), new_cue.noun, str(new_cue.ref)))
                        continue
                    func_uuid = fix.get_dimmer_function().uuid
                    # We may have already added this so-called tracked value in the
                    # moves section. It seems to be a bit random whether they are
                    # in one section, the other or both, so we really do need to
                    # check the entirety of each. It doesn't really matter which of
                    # the move or track values takes precedence; they are both the
                    # same every time.
                    for level in new_cue.levels:
                        if level.function == func_uuid:
                            new_cue.levels.remove(level)
                            break
                    new_cue.levels.append(document.FunctionLevel(func_uuid, eos_chan.level))
                for eos_param in ascii_cue.params:
                    try:
                        fix = self.file.get_by_ref(document.Fixture, Decimal(ascii_file.sortable_chan(eos_param.chan)))
                    except AttributeError:
                        self.post_feedback(exception.ERROR_MSG_UNPATCHED_FIXTURE.format(
                            str(eos_param.chan_id), new_cue.noun, str(new_cue.ref)))
                        continue
                    func_name = reference.EOS_GDTF_MAP.get(eos_param.param.long_name, eos_param.param.long_name)
                    func_uuid = fix.get_function(func_name).uuid
                    # Param values which refer to the Intensity parameter will have already
                    # been inserted from either the moves or chans section, so that copy
                    # needs to be removed when we add the param value. (Param values
                    # are preferred to the moves or chans values as they can include
                    # referenced values whereas the others cannot)
                    if func_name == document.DIMMER_PARAM_NAME:
                        for level in new_cue.levels:
                            if level.function == func_uuid:
                                new_cue.levels.remove(level)
                                break
                    new_cue.levels.append(document.FunctionLevel(func_uuid, eos_param.level))
                self.file.insert_object(new_cue)


def register_extension(interpreter):
    EosExtension(interpreter).register_extension()
