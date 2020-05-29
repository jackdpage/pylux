from pylux.interpreter import RegularCommand, InterpreterExtension
from pylux import document
import pygdtf
from pylux.lib import data
import uuid


class GdtfExtension(InterpreterExtension):

    def register_commands(self):
        self.commands.append(RegularCommand(('Fixture', 'CreateFrom'), self.fixture_createfrom, check_refs=False))

    def fixture_createfrom(self, refs, template):
        template_file = data.get_data('fixture/'+template+'.gdtf')
        if not template_file:
            self.interpreter.msg.post_feedback(['Template {0} does not exist'.format(template)])
            return None
        fixture_type = pygdtf.FixtureType(template_file)
        for r in refs:
            fix = document.insert_blank_fixture(self.interpreter.file, r)
            fix['fixture-type'] = fixture_type.name
            fix['manufacturer'] = fixture_type.manufacturer
            fix['power'] = sum([b.power_consumption for b in fixture_type.get_geometry_by_type('Beam')])
            for dmx_chan in fixture_type.dmx_modes[0].dmx_channels:
                fix['personality'].append({
                    'type': 'function',
                    'uuid': str(uuid.uuid4()),
                    'param': dmx_chan.logical_channels[0].attribute,
                    'offset': dmx_chan.offset[0]
                })
                if len(dmx_chan.offset) > 1:
                    fix['personality'].append({
                        'type': 'function',
                        'uuid': str(uuid.uuid4()),
                        'param': dmx_chan.logical_channels[0].attribute + ' (16b)',
                        'offset': dmx_chan.offset[1]
                    })


def register_extension(interpreter):
    GdtfExtension(interpreter).register_extension()
