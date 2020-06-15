import math
from pylux.interpreter import InterpreterExtension, NoRefsCommand
from pylux import document
from pylux import reference
from pylux.lib import usitt, exception
from decimal import Decimal


class EosExtension(InterpreterExtension):

    def register_commands(self):
        self.commands.append(NoRefsCommand(('File', 'ImportAscii'), self.file_importascii))

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
                functions.append(document.FixtureFunction(param_name, func.offset[0], func.param_size))
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


def register_extension(interpreter):
    EosExtension(interpreter).register_extension()
