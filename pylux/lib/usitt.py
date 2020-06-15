from typing import List, Tuple
from decimal import Decimal
import math


END_OF_BLOCK = None


def clean_line(line):
    """Transform a line into a split list of words."""
    line = line.lstrip()
    line = line.strip()
    return line.split()


def next_in_block(current_line, block):
    return block[block.index(current_line) + 1]


class AsciiFile:

    def __init__(self, fp=None):
        self.parameters: List['Parameter'] = []
        self.personalities: List['Personality'] = []
        self.patch: List['PatchEntry'] = []
        self.cue_lists: List['CueList'] = []
        self.intensity_palettes: List['IntensityPalette'] = []
        self.focus_palettes: List['FocusPalette'] = []
        self.color_palettes: List['ColorPalette'] = []
        self.beam_palettes: List['BeamPalette'] = []
        self.groups: List['Group'] = []
        if fp:
            with open(fp, 'r') as f:
                self._raw = f.readlines()
        # Whilst most things in the document fit into 'blocks' i.e. text
        # blocks with clear blank lines delimiting the start and end, some do
        # not. The most obvious case is for cues, which can have blank lines
        # within the cue blocks between the param and effectdata values.
        # Therefore we keep a running record of which cue we are currently in
        # so if we do come across any Param lines by themselves, we know where
        # they belong. Note that 'Cue' in this sense could also be a Palette or
        # submaster as both of these also use $$Param lines.
        current_cue = None

        def append_current_cue():
            """Add the current 'cue' to its correct location. This could also be a
            palette or submaster."""
            if type(current_cue) == Cue:
                self.get_cue_list(current_cue.cue_list).cues.append(current_cue)
            elif type(current_cue) == IntensityPalette:
                self.intensity_palettes.append(current_cue)
            elif type(current_cue) == FocusPalette:
                self.focus_palettes.append(current_cue)
            elif type(current_cue) == ColorPalette:
                self.color_palettes.append(current_cue)
            elif type(current_cue) == BeamPalette:
                self.beam_palettes.append(current_cue)

        for line in self._raw:
            clean = clean_line(line)
            # If the line is empty, move onto the next one
            if not clean:
                continue
            if not clean[0]:
                continue
            # All comment lines are preceded by one or more exclamation points
            if clean[0][0] == '!':
                continue
            # Check for the version and general data in the preamble
            if clean[0] == 'Ident':
                self.ident = clean[1]
                continue
            if clean[0] == 'Manufacturer':
                self.manufacturer = clean[1]
                continue
            if clean[0] == 'Console':
                self.console = clean[1]
                continue
            if clean[0] == '$$Format':
                self.format = clean[1]
                continue
            if clean[0] == '$$Software':
                self.software_version = clean[2]
                self.software_build = clean[4]
                self.fixture_library_version = clean[8].replace(',', '')
                continue
            if clean[0] == '$$Title':
                self.title = ' '.join(clean[1:])
                continue
            if clean[0] == 'Set' and clean[1] == 'Channels':
                self.channel_count = int(clean[2])
                continue
            # Arbitrary set tags are indicated by a double dollar variable
            if clean[0] == 'Set' and clean[1][0:2] == '$$':
                self.__setattr__(clean[1][2:].lower(), tuple(clean[2:]))
                continue
            if clean[0] == '$ParamType':
                self.parameters.append(Parameter(int(clean[1]), int(clean[2]), self.next(line)[1], clean[3]))
                continue
            if clean[0] == '$Personality':
                block = self.all_to_blank(line)
                pers = Personality(pers_id=int(clean[1]))
                # When it comes to the PersChan entries, we need to know what
                # channel we're currently working on so that slots get added
                # properly, so we update the current_chan variable each time we
                # encounter a new $PersChan
                current_chan = None
                for block_line in block:
                    # If this is the end of the block, we've finished creating
                    # the personality so can add it to the internal list
                    if block_line is END_OF_BLOCK:
                        if current_chan:
                            pers.channels.append(current_chan)
                        self.personalities.append(pers)
                        continue
                    if block_line[0] == '$$Manuf':
                        pers.manuf = block_line[1]
                        continue
                    if block_line[0] == '$$Model':
                        pers.model = block_line[1]
                        continue
                    if block_line[0] == '$$Dcid':
                        pers.dcid = block_line[1]
                        continue
                    if block_line[0] == '$$Footprint':
                        pers.footprint = int(block_line[1])
                        continue
                    if block_line[0] == '$$VirtualInt':
                        pers.channels.append(PersonalityChannel(
                            param=self.intens_parameter(), virtual=True
                        ))
                        continue
                    if block_line[0] == '$$PersChan':
                        # This must be the start of a new channel, so add the
                        # current working channel to the personality channel list
                        # (if there is one) and start a fresh one
                        if current_chan:
                            pers.channels.append(current_chan)
                        if len(block_line) > 6:
                            snap = True
                        else:
                            snap = False
                        if int(block_line[4]):
                            lsb_offset = int(block_line[4])
                        else:
                            lsb_offset = None
                        param = self.get_parameter(int(block_line[1]))
                        current_chan = PersonalityChannel(
                            param, int(block_line[2]), int(block_line[3]), lsb_offset,
                            int(block_line[5]), snap
                        )
                        continue
                    if block_line[0] == '$$PersSlot':
                        # Slot labels can either be the final parameter in the first line,
                        # or on a line of their own if they are too long, so we need to
                        # check both cases
                        if len(block_line) > 6:
                            slot_text = ' '.join(block_line[6:])
                        elif next_in_block(block_line, block)[0] == '$$PersSlText':
                            slot_text = ' '.join(next_in_block(block_line, block)[1:])
                        else:
                            slot_text = None
                        current_chan.slots.append(PersonalitySlot(
                            int(block_line[1]), int(block_line[2]), int(block_line[3]),
                            float(block_line[4]), float(block_line[5]), slot_text
                        ))
                        continue
                    # We can't guarantee the parts for the personality have been defined
                    # yet, so we just add their DCIDs and we'll come back to them later
                    if block_line[0] == '$$PersPart':
                        pers.parts.append(PersonalityPart(int(block_line[1]), block_line[2]))
                    # PersSlText fields are dealt with at the same time as PersSlot,
                    # so we can safely ignore them when they come up in the iteration
                continue
            if clean[0] == '$Patch':
                block = self.all_to_blank(line)
                patch = PatchEntry(int(clean[1]), int(clean[2]), int(clean[3]))
                for block_line in block:
                    # Similar to the personality method, if this is the last
                    # line in the patch block, we can add it to the internal
                    # list of patches
                    if block_line is END_OF_BLOCK:
                        self.patch.append(patch)
                        continue
                    if block_line[0] == '$$Pers':
                        patch.pers_name = ' '.join(block_line[1:])
                        continue
                    if block_line[0] == 'Text':
                        patch.label = ' '.join(block_line[1:])
                        continue
                    if block_line[0] == '$$Proportion':
                        patch.proportion = float(block_line[1])
                        continue
                    if block_line[0] == '$$Options':
                        patch.options = tuple(block_line[1:])
                        continue
                    if block_line[0] == '$$TextGel':
                        patch.gel = ' '.join(block_line[1:])
                        continue
                    # This covers Text[1-10] without having to bother with regex
                    if '$$Text' in block_line[0]:
                        # Index of the text in the list needs to have one taken off
                        # to match 1-index used by Eos
                        patch.text[int(block_line[0].split('$$Text')[1]) - 1] = block_line[1]
                        continue
                    if block_line[0] == '$$Position':
                        patch.position = [float(i) for i in block_line[1:]]
                        continue
                    if block_line[0] == '$$Orientation':
                        patch.orientation = [float(i) for i in block_line[1:]]
                        continue
            if clean[0] == '$CueList':
                block = self.all_to_blank(line)
                qlist = CueList(num=int(clean[1]))
                for block_line in block:
                    if block_line is END_OF_BLOCK:
                        self.cue_lists.append(qlist)
                        continue
                    if block_line[0] == 'Text':
                        qlist.label = ' '.join(block_line[1:])
                        continue
            if clean[0] == 'Cue':
                block = self.all_to_blank(line)
                append_current_cue()
                current_cue = Cue(ref=Decimal(clean[1]), cue_list=int(clean[2]))
                for block_line in block:
                    if block_line is END_OF_BLOCK:
                        continue
                    if block_line[0] == 'Text':
                        current_cue.label = ' '.join(block_line[1:])
                        continue
                    if block_line[0] == '$$TimeUp':
                        current_cue.times.up = (Decimal(i) for i in block_line[1:])
                        continue
                    if block_line[0] == '$$TimeDown':
                        current_cue.times.down = (Decimal(i) for i in block_line[1:])
                        continue
                    if block_line[0] == '$$TimePosition':
                        current_cue.times.pos = (Decimal(i) for i in block_line[1:])
                        continue
                    if block_line[0] == '$$TimeColor':
                        current_cue.times.color = (Decimal(i) for i in block_line[1:])
                        continue
                    if block_line[0] == '$$TimeGraphic':
                        current_cue.times.beam = (Decimal(i) for i in block_line[1:])
                        continue
                    if block_line[0] == '$$ChanMove':
                        for move in block_line[1:]:
                            current_cue.moves.append(ChanMove(int(move.split('@')[0]),
                                                              move.split('@')[1]))
                        continue
                    if block_line[0] == 'Chan':
                        for track in block_line[1:]:
                            current_cue.tracked.append(ChanLevel(int(track.split('@')[0]),
                                                                 track.split('@')[1]))
                        continue
            if clean[0] == '$$Param':
                for param in clean[2:]:
                    current_cue.params.append(CueParam(int(clean[1]),
                                                       int(param.split('@')[0]),
                                                       param.split('@')[1]))
                continue
            if clean[0] == '$IntensPalette':
                block = self.all_to_blank(line)
                append_current_cue()
                current_cue = IntensityPalette(ref=Decimal(clean[1]))
                for block_line in block:
                    if block_line is END_OF_BLOCK:
                        continue
                    if block_line[0] == 'Text':
                        current_cue.label = ' '.join(block_line[1:])
                        continue
                continue
            if clean[0] == '$FocusPalette':
                block = self.all_to_blank(line)
                append_current_cue()
                current_cue = FocusPalette(ref=Decimal(clean[1]))
                for block_line in block:
                    if block_line is END_OF_BLOCK:
                        continue
                    if block_line[0] == 'Text':
                        current_cue.label = ' '.join(block_line[1:])
                        continue
                continue
            if clean[0] == '$ColorPalette':
                block = self.all_to_blank(line)
                append_current_cue()
                current_cue = ColorPalette(ref=Decimal(clean[1]))
                for block_line in block:
                    if block_line is END_OF_BLOCK:
                        continue
                    if block_line[0] == 'Text':
                        current_cue.label = ' '.join(block_line[1:])
                        continue
                continue
            if clean[0] == '$BeamPalette':
                block = self.all_to_blank(line)
                append_current_cue()
                current_cue = BeamPalette(ref=Decimal(clean[1]))
                for block_line in block:
                    if block_line is END_OF_BLOCK:
                        continue
                    if block_line[0] == 'Text':
                        current_cue.label = ' '.join(block_line[1:])
                        continue
                continue
            if clean[0] == '$Group':
                block = self.all_to_blank(line)
                group = Group(ref=int(clean[1]))
                for block_line in block:
                    if block_line is END_OF_BLOCK:
                        self.groups.append(group)
                        continue
                    if block_line[0] == 'Text':
                        group.label = ' '.join(block_line[1:])
                        continue
                    if block_line[0] == '$$ChanList':
                        for cid in block_line[1:]:
                            group.chan_ids.append(int(cid))
                        continue
                continue

        # We won't have added the last cue as the trigger for adding a cue to
        # the internal list is finding the next cue, so we need to flush this
        # out at the end.
        append_current_cue()
        # Although Eos does put all personalities in the file before the patch,
        # we can't *necessarily* guarantee that, so rather than passing actual
        # Personality objects (which may not actually exist yet) to the patch
        # entries, we just pass the personality id (which is how the ASCII file
        # handles this anyway. Then all we need to do is pass over and match the
        # two up once we know for sure we have got all the personalities stored
        for patch in self.patch:
            patch.pers = self.get_personality(patch.pers_number)
        # Similarly, we also need to go through and put in personality parts
        # which have now been defined
        for pers in self.personalities:
            if pers.parts:
                for part in pers.parts:
                    part.pers = self.get_personality_dcid(part.dcid)
        # And for the cues...
        for qlist in self.cue_lists:
            for cue in qlist.cues:
                for track in cue.tracked:
                    track.chan = self.get_chan(track.chan_id)
                for param in cue.params:
                    param.chan = self.get_chan(param.chan_id)
                    param.param = self.get_parameter(param.param_id)
                for move in cue.moves:
                    move.chan = self.get_chan(move.chan_id)
        # And for groups...
        for group in self.groups:
            for cid in group.chan_ids:
                # We have to check that the returned chan actually exists as it
                # is possible for channels to be present in group entries but not
                # actually exist in the patch section.
                if self.get_chan(cid):
                    group.chans.append(self.get_chan(cid))
        # And palettes, yawn...
        for ip in self.intensity_palettes:
            for param in ip.params:
                param.chan = self.get_chan(param.chan_id)
                param.param = self.get_parameter(param.param_id)
        for fp in self.focus_palettes:
            for param in fp.params:
                param.chan = self.get_chan(param.chan_id)
                param.param = self.get_parameter(param.param_id)
        for cp in self.color_palettes:
            for param in cp.params:
                param.chan = self.get_chan(param.chan_id)
                param.param = self.get_parameter(param.param_id)
        for bp in self.beam_palettes:
            for param in bp.params:
                param.chan = self.get_chan(param.chan_id)
                param.param = self.get_parameter(param.param_id)

    def next(self, current_line):
        """Given the current line, fetch the next line in the document."""
        return clean_line(self._raw[self._raw.index(current_line) + 1])

    def all_to_blank(self, current_line):
        """Given the current line, fetch a list of all lines up until the
        next blank line."""
        block = []
        for line in self._raw[self._raw.index(current_line):]:
            if clean_line(line):
                block.append(clean_line(line))
            else:
                # Add an END_OF_BLOCK indicator as the last 'line' in the
                # block, that way the parsers know when they have completed
                # a block. Obviously this could have been done just by having
                # the parser check the current index against the length of
                # the block, which would have been a bit neater. However this
                # was significantly easier.
                block.append(END_OF_BLOCK)
                return block

    def get_parameter(self, ref: int):
        for param in self.parameters:
            if param.id == ref:
                return param

    def intens_parameter(self):
        for param in self.parameters:
            if param.long_name == 'Intens':
                return param

    def get_personality(self, ref: int):
        for pers in self.personalities:
            if pers.id == ref:
                return pers

    def get_personality_dcid(self, dcid: str):
        for pers in self.personalities:
            if pers.dcid == dcid:
                return pers

    def get_cue_list(self, ref: int):
        for qlist in self.cue_lists:
            if qlist.id == ref:
                return qlist

    def get_chan(self, ref: int):
        for chan in self.patch:
            if chan.chan == ref:
                return chan

    def sortable_chan(self, patch: 'PatchEntry'):
        """Get the channel number in a sortable format, i.e. 1.01 ... 1.10 by
        checking how many component cells the master fixture has and
        formatting accordingly."""
        if patch.chan < self.channel_count:
            return str(patch.chan)
        master_number = int(str(patch.chan)[:-4]) - 10
        cell_number = int(str(patch.chan)[-4:]) + 1
        master_fixture = self.get_chan(master_number)
        total_cells = len(master_fixture.pers.parts)
        if total_cells == 0:
            return str(patch.chan)
        cell_digits = int(math.log10(total_cells)) + 1
        return str(master_number) + '.' + str(cell_number).zfill(cell_digits)


class Parameter:

    def __init__(self, param_id: int = None, cat: int = None,
                 short_name: str = None, long_name: str = None):
        self.id = param_id
        self.cat = cat
        self.short_name = short_name
        self.long_name = long_name


class Personality:

    def __init__(self, pers_id: int = None, manuf: str = None, model: str = None,
                 dcid: str = None, source_dcid: str = None, remote_dim: bool = None,
                 footprint: int = None, total_footprint: int = None, options: str = None,
                 root_part_offset: int = None, channels: List['PersonalityChannel'] = None,
                 parts: list = None, virtual_int: bool = None,
                 notes: str = None):
        self.id = pers_id
        self.manuf = manuf
        self.model = model
        self.dcid = dcid
        self.source_dcid = source_dcid
        self.remote_dim = remote_dim
        self.footprint = footprint
        self.total_footprint = total_footprint
        self.options = options
        self.root_part_offset = root_part_offset
        if not channels:
            self.channels = []
        else:
            self.channels = channels
        if not parts:
            self.parts = []
        else:
            self.parts = parts
        self.virtual_int = virtual_int
        self.notes = notes


class PersonalityChannel:

    def __init__(self, param: 'Parameter' = None, param_size: int = None,
                 offset_msb: int = None, offset_lsb: int = None, home: int = None,
                 snap: bool = None, slots: List['PersonalitySlot'] = None,
                 virtual: bool = False):
        self.param = param
        self.param_size = param_size
        self.offset = (offset_msb, offset_lsb)
        self.home = home
        self.snap = snap
        if not slots:
            self.slots = []
        else:
            self.slots = slots
        self.virtual = virtual


class PersonalitySlot:

    def __init__(self, min_dmx: int = None, max_dmx: int = None, home: int = None,
                 min_user: float = None, max_user: float = None, label: str = None,
                 slot_dcid: str = None):
        self.dmx_range = (min_dmx, max_dmx)
        self.user_range = (min_user, max_user)
        self.home = home
        self.label = label
        self.slot_dcid = slot_dcid


class PersonalityPart:

    def __init__(self, offset: int = None, dcid: str = None, label: str = None):
        self.offset = offset
        self.dcid = dcid
        self.label = label
        self.pers = None


class PatchEntry:

    def __init__(self, chan: int = None, pers_number: int = None, address: int = None,
                 edmx: bool = None, part: 'PersonalityPart' = None, pers_name: str = None,
                 label: str = None, proportion: float = None, options: tuple = None,
                 text: list = None, gel: str = None, notes: str = None,
                 position: Tuple[float] = None, orientation: Tuple[float] = None):
        self.chan = chan
        self.pers_number = pers_number
        self.pers = None
        self.address = address
        self.edmx = edmx
        self.part = part
        self.pers_name = pers_name
        self.label = label
        self.proportion = proportion
        self.options = options
        if not text:
            self.text = [None] * 10
        else:
            self.text = text
        self.gel = gel
        self.notes = notes
        self.position = position
        self.orientation = orientation


class CueList:

    def __init__(self, num: int = None, cues: List['Cue'] = None, label: str = None):
        self.id = num
        self.label = label
        if not cues:
            self.cues = []
        else:
            self.cues = cues


class Cue:

    def __init__(self, ref: Decimal = None, label: str = None, times: 'CueTiming' = None,
                 block: bool = None, q_assert: bool = None, int_block: bool = None,
                 chan_moves: List['ChanMove'] = None, param_levels: List['CueParam'] = None,
                 tracked_levels: List['ChanLevel'] = None,
                 effect_chans: List['EffectChan'] = None, effect_data: 'EffectData' = None,
                 cue_list: int = None):
        self.id = ref
        self.label = label
        if not times:
            self.times = CueTiming()
        else:
            self.times = times
        self.block = bool(block)
        self.is_assert = bool(q_assert)
        self.int_block = bool(int_block)
        if not chan_moves:
            self.moves = []
        else:
            self.moves = chan_moves
        if not param_levels:
            self.params = []
        else:
            self.params = param_levels
        if not tracked_levels:
            self.tracked = []
        else:
            self.tracked = tracked_levels
        if not effect_chans:
            self.effect_chans = []
        else:
            self.effect_chans = effect_chans
        if not effect_data:
            self.effect_data = []
        else:
            self.effect_data = effect_data
        self.cue_list = cue_list


class CueTiming:

    def __init__(self, up=None, down=None, pos=None, color=None, beam=None):
        self.up = up
        self.down = down
        self.pos = pos
        self.color = color
        self.beam = beam


class ChanLevel:

    def __init__(self, chan_ref: int, level):
        self.chan_id = chan_ref
        self.level = level
        self.chan: 'PatchEntry' = None


class ChanMove(ChanLevel):
    pass


class CueParam:

    def __init__(self, chan_ref, param_ref, level):
        self.chan_id = chan_ref
        self.param_id = param_ref
        self.level = level
        self.chan: 'PatchEntry' = None
        self.param: 'Parameter' = None


class EffectChan:

    def __init__(self, effect_id, chan_id, param_ids):
        self.effect_id = effect_id
        self.chan_id = chan_id
        self.param_ids = param_ids


class EffectData:

    def __init__(self, effect_id, key, val):
        self.effect_id = effect_id
        self.key = key
        self.value = val


class Palette:

    def __init__(self, ref: Decimal = None, label: str = None,
                 params: List['CueParam'] = None):
        self.id = ref
        self.label = label
        if not params:
            self.params = []
        else:
            self.params = params


class IntensityPalette(Palette):
    pass


class FocusPalette(Palette):
    pass


class BeamPalette(Palette):
    pass


class ColorPalette(Palette):
    pass


class Group:

    def __init__(self, ref: int = None, label: str = None, chan_ids: list = None):
        self.id = ref
        self.label = label
        self.chans = []
        if not chan_ids:
            self.chan_ids = []
        else:
            self.chan_ids = chan_ids
