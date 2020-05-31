from pylux.interpreter import RegularCommand, InterpreterExtension
from pylux import document
import pygdtf
from pylux.lib import data
import uuid
import pathlib


class TemplateExtension(InterpreterExtension):

    def register_commands(self):
        self.commands.append(RegularCommand(('Fixture', 'CompleteFrom'), self.fixture_completefrom))
        self.commands.append(RegularCommand(('Fixture', 'CreateFrom'), self.fixture_createfrom, check_refs=False))

    def _get_template_file(self, template):
        template_type = pathlib.Path(template).suffix
        if template_type:
            template_file = data.get_data('fixture/' + template)
        else:
            template_file = data.get_data('fixture/' + template + '.gdtf')
        if not template_file:
            self.interpreter.msg.post_feedback(['Template {0} does not exist'.format(template)])
            return None
        return pathlib.Path(template_file)

    def _fixture_completefrom_gdtf(self, refs, template_file):
        fixture_type = pygdtf.FixtureType(template_file)
        for r in refs:
            fix = document.get_by_ref(self.interpreter.file, 'fixture', r)
            if 'fixture-type' not in fix:
                fix['fixture-type'] = fixture_type.name
            if 'manufacturer' not in fix:
                fix['manufacturer'] = fixture_type.manufacturer
            if 'power' not in fix:
                fix['power'] = sum([b.power_consumption for b in fixture_type.get_geometry_by_type('Beam')])
            if fix['personality']:
                for dmx_chan in fixture_type.dmx_modes[0].dmx_channels:
                    if dmx_chan.offset:
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

    def _fixture_completefrom_json(self, refs, template_file):
        for r in refs:
            fix = document.get_by_ref(self.interpreter.file, 'fixture', r)
            document.complete_fixture_from_json_template(fix, template_file)

    def _fixture_createfrom_gdtf(self, refs, template_file):
        fixture_type = pygdtf.FixtureType(template_file)
        for r in refs:
            fix = document.insert_blank_fixture(self.interpreter.file, r)
            fix['fixture-type'] = fixture_type.name
            fix['manufacturer'] = fixture_type.manufacturer
            fix['power'] = sum([b.power_consumption for b in fixture_type.get_geometry_by_type('Beam')])
            for dmx_chan in fixture_type.dmx_modes[0].dmx_channels:
                if dmx_chan.offset:
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

    def _fixture_createfrom_json(self, refs, template_file):
        for r in refs:
            document.insert_fixture_from_json_template(self.interpreter.file, r, template_file)

    def fixture_createfrom(self, refs, template):
        template_file = self._get_template_file(template)
        if not template_file:
            return
        if template_file.suffix == '.json':
            self._fixture_createfrom_json(refs, str(template_file))
        else:
            self._fixture_createfrom_gdtf(refs, str(template_file))

    def fixture_completefrom(self, refs, template):
        template_file = self._get_template_file(template)
        if not template_file:
            return
        if template_file.suffix == '.json':
            self._fixture_completefrom_json(refs, str(template_file))
        else:
            self._fixture_completefrom_gdtf(refs, str(template_file))


def register_extension(interpreter):
    TemplateExtension(interpreter).register_extension()
