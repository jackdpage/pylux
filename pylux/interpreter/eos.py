from copy import deepcopy
import math, re
from pylux.interpreter import RegularCommand, InterpreterExtension, NoRefsCommand
from pylux import document


class EosExtension(InterpreterExtension):

    def register_commands(self):
        self.commands.append(NoRefsCommand(('File', 'ImportAscii'), self.file_importascii))

    def file_importascii(self, file, target):
        with open(file) as f:
            raw = f.readlines()

        def convert_fix_ref(eos_ref):
            # Convert an Eos fixture ref into the standard format of fixture
            # ref. For most fixtures this does nothing - it serves to convert
            # those multicell fixture cells
            if int(eos_ref) > 5000:
                master_number = int(str(eos_ref)[:-4]) - 10
                master_fixture = document.get_by_ref(self.interpreter.file, 'fixture', master_number)
                # We find out the total number of component cells in the master fixture to determine
                # how many digits should be in the cell number. We do this so that they are numbered
                # 1.01, 1.02, ..., 1.10 etc. rather than 1.1, 1.2, ..., 1.10 etc. The latter method
                # would be much easier and wouldn't require any lookup of existing master fixtures,
                # however it will not work properly with normal sorting tools and is quite ambiguous.
                total_cells = master_fixture['component-cells']
                cell_digits = int(math.log10(total_cells)) + 1
                cell_number = int(str(eos_ref)[-4:]) + 1
                return str(master_number) + '.' + str(cell_number).zfill(cell_digits)
            else:
                return eos_ref

        def extract_blocks(start_regex):
            # Utility function to extract blocks of data beginning with given
            # regex pattern and ending with a blank line. Returns as a list
            # of lines for easy parsing.
            blocks = []
            current_block = []
            start_r = re.compile(start_regex)
            end_r = re.compile('^\s*$')
            for l in raw:
                if re.match(start_r, l):
                    current_block.append(l)
                if current_block != []:
                    # We only want to perform the following functions if we're
                    # already in a block, to prevent adding the whole document.
                    if re.match(end_r, l):
                        blocks.append(current_block)
                        current_block = []
                    else:
                        current_block.append(l)
            return blocks

        def resolve_line(line):
            # Strips down lines in blocks and returns them in a key/value
            # format.
            line = line.lstrip()
            line = line.strip()
            return line.split(' ', maxsplit=1)

        # Look through parameters saved in this ASCII file and make our
        # own list to we can refer to them later.
        parameters = {}
        r = re.compile('\$ParamType +([0-9]*) ([0-9]*) (.*)')
        for l in raw:
            match = re.match(r, l)
            if match:
                parameters[match.group(1)] = match.group(3).strip()

        if target == 'conventional_patch':
            entries = []
            r = re.compile('Patch.*')
            # Scan file for lines beginning with the Patch keyword and populate
            # into list for parsing.
            for l in raw:
                match = re.match(r, l)
                if match:
                    entries.append(match.string)
            # For each patch line found, find each mapping within the line and
            # add to the plot file using the built in command.
            r = re.compile('[0-9]*<[0-9]{0,3}')
            template = self.interpreter.config['ascii']['conventional-template']
            for e in entries:
                maps = re.findall(r, e)
                for f in maps:
                    ref = f.split('<')[0]
                    addr = int(f.split('<')[1])
                    dmx = str(addr % 512)
                    univ = str(math.floor(addr / 512))
                    self.parent.functions['fixture_createfrom'](ref, [template])
                    document.safe_address_fixture_by_ref(self.interpreter.file, ref, univ, addr)

        elif target == 'eos_patch':
            personality_blocks = extract_blocks('\$Personality.*')
            patch_blocks = extract_blocks('\$Patch.*')
            templates = {}

            # Look through personalities saved in this ASCII file and make our
            # own list of them so we can refer to them later.
            for block in personality_blocks:
                pers_ref = block[0].split(' ')[1]
                pers = []
                template = {'type': 'fixture'}
                for l in block:
                    res = resolve_line(l)
                    if res[0] == '$$Manuf':
                        template['manufacturer'] = res[1]
                    elif res[0] == '$$Model':
                        template['fixture-type'] = res[1]
                    elif res[0] == '$$PersChan':
                        pers.append({
                            'type': 'function',
                            'param': parameters[res[1].split()[0]],
                            'offset': int(res[1].split()[2]),
                        })
                        if int(res[1].split()[1]) == 2:
                            pers.append({
                                'type': 'function',
                                'param': parameters[res[1].split()[0]] + ' (16b)',
                                'offset': int(res[1].split()[3])
                            })
                    # Count up the number of $$PersPart, which indicates a cell in a multicell fixture
                    elif res[0] == '$$PersPart':
                        if 'component-cells' in template:
                            template['component-cells'] += 1
                        else:
                            template['component-cells'] = 1
                # If the fixture personality does not contain an Intens parameter, add a virtual Intens parameter
                # with offset zero, so the fixture can be used for commands such as get_fixture_intens
                if 'Intens' not in [i['param'] for i in pers]:
                    pers.append({
                        'type': 'function',
                        'param': 'Intens',
                        'offset': 0,
                        'virtual': True
                    })
                template['personality'] = pers
                templates[pers_ref.strip()] = template

            for patch in patch_blocks:
                fix_ref = convert_fix_ref(patch[0].split(' ')[1])
                # We have to make a deep copy of the template, to ensure that
                # we aren't adjusting the personality and functions in place
                # when we add UUIDs
                template = deepcopy(templates[patch[0].split(' ')[2]])
                addr = int(patch[0].split(' ')[3])
                dmx = addr % 512
                univ = math.floor(addr / 512)
                fixture = document.insert_blank_fixture(self.interpreter.file, fix_ref)
                for k in template:
                    fixture[k] = template[k]
                document.fill_missing_function_uuids(fixture)
                # Patch the fixture from the address in the @Patch line
                document.safe_address_fixture_by_ref(self.interpreter.file, fix_ref, univ, dmx)
                # We've dealt with the main @Patch line, now we can scan through
                # the rest of the block and see if we can merge in anything else.
                for l in patch:
                    res = resolve_line(l)
                    if res[0] == '$$TextGel':
                        fixture['gel'] = res[1]
                    if res[0] == 'Text':
                        fixture['label'] = res[1]
                    if res[0] == '$$Position':
                        pos_array = res[1].split(maxsplit=3)
                        fixture['posX'] = pos_array[0]
                        fixture['posY'] = pos_array[1]
                        fixture['posZ'] = pos_array[2]
                    if res[0] == '$$Orientation':
                        fixture['rotation'] = res[1].split()[1]

        elif target == 'cues':
            cue_blocks = extract_blocks('Cue.*')
            for block in cue_blocks:
                # Ignore anything which isn't in Cue List 1, we can't quite handle that yet
                cue_list = block[0].split()[2]
                if str(cue_list) != '1':
                    break
                cue_ref = block[0].split()[1]
                cue = document.insert_blank_cue(self.interpreter.file, cue_ref)
                for l in block:
                    res = resolve_line(l)
                    if res[0] == 'Text':
                        cue['label'] = res[1]
                    elif res[0] == 'Up':
                        cue['fade-up'] = res[1]
                    elif res[0] == 'Down':
                        cue['fade-down'] = res[1]
                    elif res[0] == 'Chan':
                        for level in res[1].split():
                            fix_ref = convert_fix_ref(level.split('@')[0])
                            try:
                                document.set_cue_fixture_level_by_fixture_ref(self.interpreter.file, cue,
                                                                              fix_ref, level.split('@')[1])
                            except TypeError:
                                self.interpreter.msg.post_feedback(['Fixture '+fix_ref+' appeared in cue ' + cue_ref +
                                                                    ' but is not patched. Ignoring...'])
                                continue
                    elif res[0] == '$$Param':
                        fix_ref = convert_fix_ref(res[1].split()[0])
                        fixture = document.get_by_ref(self.interpreter.file, 'fixture', fix_ref)
                        if fixture:
                            for param_level in res[1].split():
                                if '@' in param_level:
                                    param_type = parameters[param_level.split('@')[0]]
                                    # If this parameter is Intens, it will be referring to a 16 bit value, which we
                                    # have probably already added as an 8 bit from the generic levels lines. Therefore,
                                    # we will remove the 8 bit entry and replace with this 16 bit entry.
                                    if param_type == 'Intens':
                                        intens_uuid = document.find_fixture_intens(fixture)['uuid']
                                        cue_levels = document.get_by_ref(self.interpreter.file, 'cue', cue_ref)['levels']
                                        if intens_uuid in cue_levels:
                                            del cue_levels[intens_uuid]
                                    # We use the same CP/BP/FP/IP designation of Eos, except they call All Palettes
                                    # Presets, with the abbreviation PR rather than AP, so we will swap these out
                                    param_value = param_level.split('@')[1].replace('PR', 'AP')
                                    func = document.get_by_value(fixture['personality'], 'param', param_type)[0]
                                    document.set_cue_function_level(self.interpreter.file, cue, func, param_value)

        elif target == 'groups':
            group_blocks = extract_blocks('\$Group')
            for block in group_blocks:
                ref = block[0].split()[1]
                group = document.insert_blank_group(self.interpreter.file, ref)
                for l in block:
                    res = resolve_line(l)
                    if res[0] == 'Text':
                        group['label'] = res[1]
                    elif res[0] == '$$ChanList':
                        for chan in res[1].split():
                            chan = convert_fix_ref(chan)
                            document.group_append_fixture_by_ref(self.interpreter.file, group, chan)

        elif target == 'palettes':

            def _process_palette_block(block, palette):
                for l in block:
                    res = resolve_line(l)
                    if res[0] == 'Text':
                        palette['label'] = res[1]
                    elif res[0] == '$$Param':
                        fix_ref = convert_fix_ref(res[1].split()[0])
                        fixture = document.get_by_ref(self.interpreter.file, 'fixture', fix_ref)
                        if fixture:
                            for param_level in res[1].split():
                                if '@' in param_level:
                                    param_type = parameters[param_level.split('@')[0]]
                                    param_value = param_level.split('@')[1]
                                    func = document.get_by_value(fixture['personality'], 'param', param_type)[0]
                                    document.set_palette_function_level(self.interpreter.file, palette, func, param_value)

            intens_palette_blocks = extract_blocks('\$IntensPalette')
            for block in intens_palette_blocks:
                ref = block[0].split()[1]
                palette = document.insert_blank_intensity_palette(self.interpreter.file, ref)
                _process_palette_block(block, palette)
            focus_palette_blocks = extract_blocks('\$FocusPalette')
            for block in focus_palette_blocks:
                ref = block[0].split()[1]
                palette = document.insert_blank_focus_palette(self.interpreter.file, ref)
                _process_palette_block(block, palette)
            colour_palette_blocks = extract_blocks('\$ColorPalette')
            for block in colour_palette_blocks:
                ref = block[0].split()[1]
                palette = document.insert_blank_colour_palette(self.interpreter.file, ref)
                _process_palette_block(block, palette)
            beam_palette_blocks = extract_blocks('\$BeamPalette')
            for block in beam_palette_blocks:
                ref = block[0].split()[1]
                palette = document.insert_blank_beam_palette(self.interpreter.file, ref)
                _process_palette_block(block, palette)

        else:
            print('Unsupported target. See the help page for this command for a list of supported targets.')


def register_extension(interpreter):
    EosExtension(interpreter).register_extension()

