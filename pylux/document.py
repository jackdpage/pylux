from decimal import Decimal
import json
from typing import List
from uuid import uuid4
from pylux.lib import exception
from copy import deepcopy


UNLABELLED_STRING = '[Unlabelled]'
DIMMER_PARAM_NAME = 'Dimmer'


class Document:

    def __init__(self, load_path=None):
        self._content = []
        self.metadata = {}
        if load_path:
            self.load_file(load_path)

    def load_file(self, path):
        """Load a JSON document from a path."""
        with open(path, 'r') as f:
            s = f.read()
        raw = json.loads(s)
        for obj in raw:
            if 'type' not in obj:
                continue
            obj_type = obj.pop('type')
            if obj_type in FILE_NODE_STR_MAP:
                self._content.append(
                    FILE_NODE_STR_MAP[obj_type](json_object=obj))
            elif obj_type == 'metadata':
                self.metadata = deepcopy(obj['tags'])
        for group in self.get_by_type(Group):
            for n, fix in enumerate(group.fixtures):
                if type(fix) == str:
                    group.fixtures[n] = self.get_by_uuid(fix)

    def write_file(self, path):
        """Write a JSON document to a path."""
        json_document = [i.json() for i in self._content]
        json_document.append({'type': 'metadata', 'tags': deepcopy(self.metadata)})
        with open(path, 'w') as f:
            json.dump(json_document, f)

    def insert_object(self, obj):
        """Add an object to the internal content list."""
        self._content.append(obj)

    def remove_object(self, obj):
        """Remove an object from the internal content list."""
        self._content.remove(obj)

    def get_by_type(self, obj_type):
        """Get an iterator of all objects of a given type."""
        for obj in self._content:
            if type(obj) == obj_type:
                yield obj

    def get_by_ref(self, obj_type, ref: Decimal):
        """Get the object of a given type with a given reference."""
        for obj in self.get_by_type(obj_type):
            if obj.ref == Decimal(ref):
                return obj

    def get_by_uuid(self, uuid):
        """Get the object with the given unique identifier."""
        for obj in self._content:
            if obj.uuid == uuid:
                return obj

    def duplicate_object(self, src: 'TopLevelObject', dest_ref: Decimal):
        """Duplicate a source object with a new reference."""
        obj_type = type(src)
        if self.get_by_ref(obj_type, dest_ref):
            raise exception.ObjectAlreadyExistsError(obj_type, dest_ref)
        new_obj = src.get_copy()
        new_obj.ref = dest_ref
        self._content.append(new_obj)

    def get_function_by_uuid(self, uuid: str):
        """Get a function object given its unique identifier."""
        for fix in self.get_by_type(Fixture):
            for func in fix.functions:
                if func.uuid == uuid:
                    return func

    def get_function_parent(self, func: 'FixtureFunction'):
        """Get the fixture that a function belongs to."""
        for fix in self.get_by_type(Fixture):
            for func_i in fix.functions:
                if func.uuid == func_i.uuid:
                    return fix

    def get_function_patch(self, func: 'FixtureFunction'):
        """Get the registry and address number of a functions patch."""
        for reg in self.get_by_type(Registry):
            addr = reg.get_function_patch(func)
            if addr:
                return reg, addr

    def unpatch_fixture_from_all(self, fixture: 'Fixture'):
        """Unpatch a fixture from all registries."""
        for reg in self.get_by_type(Registry):
            reg.unpatch_fixture(fixture)

    def patch_fixture(self, fixture: 'Fixture', universe: int, address: int):
        """Patch a fixture to a universe and address, automatically creating
        the registry if it does not already exist."""
        reg = self.get_by_ref(Registry, Decimal(universe))
        if not reg:
            self.insert_object(Registry(ref=Decimal(universe)))
            reg = self.get_by_ref(Registry, Decimal(universe))
        reg.patch_fixture(fixture, address)


class TopLevelObject:
    """Base class for all generic top-level object types. All standard
    types should extend this class. The only exceptions are objects which
    do not have the common object structure, for example metadata."""

    # The representations of the object in the JSON file and on the user
    # facing command line, respectively.
    file_node_str = None
    command_str = None

    # Top-level attributes used by the object. Does not include the
    # arbitrary data dictionary. Attribute name used by the class should
    # be the same as the node name used in the file. These can only be
    # basic string style attributes. Anything more advanced will need to
    # be defined separately.
    required_attributes = []

    def __init__(self, uuid: str = None, ref: Decimal = None,
                 label: str = None, json_object: dict = None, **kwargs):
        """
        Create a new object, either using data provided in the
        parameters, or in the form of a JSON object, from which the
        object will be created. This super init function should be
        called *after* any object-specific attributes are defined in
        the subclass, otherwise the JSON may be read before attributes
        have been defined.
        :param uuid: unique identifier of the object
        :param ref: decimal reference number
        :param label: human-facing label/name of the object
        :param json_object: a JSON dict from which the object can be
        created
        """
        if not uuid:
            self.uuid = str(uuid4())
        else:
            self.uuid = uuid
        self.ref = ref
        self.label = label
        for k in self.required_attributes:
            self.__setattr__(k, kwargs.get(k, None))
        if json_object:
            self._read_json(json_object)

    def _read_json(self, json_object):
        """
        Fill the object data using information from a JSON object. Call
        this super function to apply the standard object attributes
        before adding object-specific attributes in the subclass.
        :param json_object: JSON dict as passed from __init__
        """
        self.uuid = json_object.get('uuid')
        self.ref = Decimal(json_object.get('ref'))
        self.label = json_object.get('label', None)
        for k in self.required_attributes:
            self.__setattr__(k, json_object.get(k, None))

    def json(self):
        """Create a dict/list JSON-style format which can be serialised
        by the JSON parser for writing to disk."""
        json_object = {'type': self.file_node_str, 'uuid': self.uuid, 'ref': str(self.ref)}
        if self.label:
            json_object['label'] = self.label
        for k in self.required_attributes:
            if self.__getattribute__(k):
                json_object[k] = self.__getattribute__(k)
        return json_object

    def get_text_widget(self):
        """
        Provides the text widget for the object in standard printed form
        with no additional processing. The default method returns just
        the ref, formatted according to file_node_str, and the label,
        if present.
        :return: list of strings and tuples in the defined form
        """
        if not self.label:
            label = UNLABELLED_STRING
        else:
            label = self.label
        return [(self.file_node_str, str(self.ref)), ' ', label]

    def get_copy(self):
        """Return a copy of this object, with changes to features which
        are required to stay unique."""
        new_instance = deepcopy(self)
        new_instance.uuid = str(uuid4())
        return new_instance


class ArbitraryDataObject(TopLevelObject):
    """A special type of top level object which also has an arbitrary
    data dictionary."""

    omitted_data_tags = ['type', 'ref', 'uuid', 'label']

    def __init__(self, data: dict = None, *args, **kwargs):
        if not data:
            self.data = {}
        else:
            self.data = data
        super().__init__(*args, **kwargs)

    def _read_json(self, json_object):
        super()._read_json(json_object)
        for k, v in json_object.items():
            if k not in self.omitted_data_tags:
                self.data[k] = v

    def json(self):
        """Create a dict/list JSON-style format which can be serialised
        by the JSON parser for writing to disk."""
        json_object = super().json()
        for k, v in self.data.items():
            json_object[k] = v
        return json_object


class Cue(ArbitraryDataObject):

    file_node_str = 'cue'
    command_str = 'Cue'
    omitted_data_tags = ArbitraryDataObject.omitted_data_tags + \
        ['cue_list', 'levels']
    required_attributes = ['cue_list']

    def __init__(self, levels: List['FunctionLevel'] = None, *args, **kwargs):
        if not levels:
            self.levels = []
        else:
            self.levels = levels
        super().__init__(*args, **kwargs)

    def _read_json(self, json_object):
        super()._read_json(json_object)
        for func, val in json_object['levels'].items():
            self.levels.append(FunctionLevel(func, val))

    def json(self):
        json_object = super().json()
        levels = {}
        for l in self.levels:
            levels[l.function] = l.value
        json_object['levels'] = levels
        return json_object

    def get_text_widget(self):
        if not self.label:
            label = UNLABELLED_STRING
        else:
            label = self.label
        return [(self.file_node_str, str(self.ref)), ' ', label, ' (',
                str(len(self.levels)), ' levels)']


class FunctionLevel:

    def __init__(self, function: str = None, value: str = None):
        self.function = function
        self.value = value


class CueList:

    def __init__(self, ref: Decimal = None):
        self.ref = ref


class Filter(TopLevelObject):

    file_node_str = 'filter'
    command_str = 'Filter'
    required_attributes = ['key', 'value']

    def get_text_widget(self):
        return [(self.file_node_str, self.ref), ' ', str(self.__getattribute__('key')),
                '=', str(self.__getattribute__('value'))]


class Fixture(ArbitraryDataObject):

    file_node_str = 'fixture'
    command_str = 'Fixture'
    omitted_data_tags = ArbitraryDataObject.omitted_data_tags + \
        ['personality']

    def __init__(self, functions: List['FixtureFunction'] = None,
                 *args, **kwargs):
        if not functions:
            self.functions = []
        else:
            self.functions = functions
        super().__init__(*args, **kwargs)

    def _read_json(self, json_object):
        super()._read_json(json_object)
        for func in json_object.get('personality'):
            self.functions.append(FixtureFunction(
                func.get('param'), func.get('offset'), func.get('size', 1),
                func.get('uuid')
            ))

    def json(self):
        json_object = super().json()
        personality = []
        for func in self.functions:
            personality.append({'param': func.parameter, 'offset': func.offset[0],
                                'size': len(func.offset), 'uuid': func.uuid})
        json_object['personality'] = personality
        return json_object

    def get_text_widget(self):
        fixture_type = self.data.get('fixture-type', 'n/a')
        if not self.label:
            return [('fixture', str(self.ref)), ' ', fixture_type]
        else:
            return [('fixture', str(self.ref)), ' ', fixture_type, ' - ',
                    self.label]

    def get_copy(self):
        new_instance = deepcopy(self)
        new_instance.uuid = str(uuid4())
        for func in new_instance.functions:
            func.uuid = str(uuid4())
        return new_instance

    def get_dimmer_function(self):
        """Return the function, if any, that corresponds to the dimmer."""
        for func in self.functions:
            if func.parameter == DIMMER_PARAM_NAME:
                return func

    def physical_functions(self):
        """Return a list of functions that are not virtual."""
        return [i for i in self.functions if i.offset]

    def dmx_size(self):
        return sum([len(i.offset) for i in self.physical_functions()])


class FixtureFunction:

    def __init__(self, parameter: str = None, offset: int = None,
                 size=1, uuid=None):
        """
        A single parameter of a fixture. This should be representative
        of an 8 or 16-bit DMX channel. For fixtures which have multiple
        logical functions on a single DMX channel, provide a more
        general parameter name or choose the dominant parameter for
        that channel.
        :param parameter: the general function of this parameter,
        following standard GDTF conventions
        :param offset: the starting offset of this parameter in the
        DMX profile of the fixture. Omit or set to zero if this is a
        virtual parameter that does not actually use a DMX channel.
        :param size: the number of DMX channels occupied by this
        parameter. Default is 1 for 8-bit parameters. 2 indicates
        a 16-bit parameter. It is assumed that greater and lesser
        bits will be patched consecutively.
        :param uuid: Provide a UUID if it needs to be defined
        explicitly, otherwise one will be generated automatically.
        """
        if uuid:
            self.uuid = uuid
        else:
            self.uuid = str(uuid4())
        self.parameter = parameter
        if not offset:
            self.offset = None
        else:
            self.offset = [offset + n for n in range(0, size)]

    def get_text_widget(self):
        if self.offset:
            return [('function', ','.join([str(i) for i in self.offset])), ' ',
                    self.parameter]
        else:
            return [('function', 'X'), ' ', self.parameter]


class Group(TopLevelObject):

    file_node_str = 'group'
    command_str = 'Group'

    def __init__(self, fixtures: List['Fixture'] = None, *args, **kwargs):
        if not fixtures:
            self.fixtures = []
        else:
            self.fixtures = fixtures
        super().__init__(*args, **kwargs)

    def _read_json(self, json_object):
        super()._read_json(json_object)
        for fix in json_object['fixtures']:
            self.fixtures.append(fix)

    def json(self):
        json_object = super().json()
        json_object['fixtures'] = [i.uuid for i in self.fixtures]
        return json_object

    def get_text_widget(self):
        if not self.label:
            label = UNLABELLED_STRING
        else:
            label = self.label
        return [(self.file_node_str, str(self.ref)), ' ', label, ' (',
                str(len(self.fixtures)), ' fixtures)']

    def append_fixture(self, fixture: 'Fixture'):
        """Add a fixture to the end of the group listing."""
        self.fixtures.append(fixture)


class Palette(TopLevelObject):

    palette_prefix = ''

    def __init__(self, levels: List['FunctionLevel'] = None, *args, **kwargs):
        if not levels:
            self.levels = []
        else:
            self.levels = levels
        super().__init__(*args, **kwargs)

    def _read_json(self, json_object):
        super()._read_json(json_object)
        for func, val in json_object['levels'].items():
            self.levels.append(FunctionLevel(func, val))

    def json(self):
        json_object = super().json()
        levels = {}
        for l in self.levels:
            levels[l.function] = l.value
        json_object['levels'] = levels
        return json_object

    def get_text_widget(self):
        if not self.label:
            label = UNLABELLED_STRING
        else:
            label = self.label
        return [(self.file_node_str, self.palette_prefix + str(self.ref)), ' ',
                label, ' (', str(len(self.levels)), ' levels)']

    def get_function_level(self, func):
        for l in self.levels:
            if func.uuid == l.function:
                return l.value


class AllPalette(Palette):

    file_node_str = 'allpalette'
    command_str = 'AllPalette'
    palette_prefix = 'PR'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BeamPalette(Palette):

    file_node_str = 'beampalette'
    command_str = 'BeamPalette'
    palette_prefix = 'BP'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ColourPalette(Palette):

    file_node_str = 'colourpalette'
    command_str = 'ColourPalette'
    palette_prefix = 'CP'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FocusPalette(Palette):

    file_node_str = 'focuspalette'
    command_str = 'FocusPalette'
    palette_prefix = 'FP'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class IntensityPalette(Palette):

    file_node_str = 'intensitypalette'
    command_str = 'IntensityPalette'
    palette_prefix = 'IP'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Registry(TopLevelObject):

    file_node_str = 'registry'
    command_str = 'Registry'

    def __init__(self, table: dict = None, *args, **kwargs):
        if not table:
            self.table = {}
        else:
            self.table = table
        super().__init__(*args, **kwargs)

    def _read_json(self, json_object):
        super()._read_json(json_object)
        for k, v in json_object.get('table', {}).items():
            self.table[int(k)] = v

    def json(self):
        json_object = super().json()
        json_object['table'] = deepcopy(self.table)
        return json_object

    def get_text_widget(self):
        return ['Universe ', (self.file_node_str, str(self.ref)), ' - ',
                str(len(self.table)), ' occupied']

    def get_occupied(self):
        """Return a list of occupied addresses."""
        return sorted([int(d) for d in self.table.keys()])

    def get_available(self):
        """Return a list of available addresses in the DMX512 space."""
        all_addrs = [i for i in range(1, 513)]
        occupied = self.get_occupied()
        available = [i for i in all_addrs if i not in occupied]
        return sorted(available)

    def get_start_address(self, n):
        """Get the earliest available start address for a fixture
        requiring n channels."""
        available = self.get_available()
        for addr in available:
            if set([i for i in range(addr, addr + n)]).issubset(available):
                return addr
        raise exception.InsufficientAvailableChannels(self, n)

    def is_valid_start(self, start, n):
        """Given a start address and n required channels, will the
        patch fit?"""
        available = self.get_available()
        if set(range(start, start + n)).issubset(available):
            return True

    def get_function_patch(self, func: 'FixtureFunction'):
        """Get the address number of a function in the registry table,
        if it exists there."""
        for addr, uuid in self.table.items():
            if uuid == func.uuid:
                return addr

    def get_fixture_patch(self, fix: 'Fixture'):
        """Get an iterator of the patch locations of any functions
        patched in this registry of a given fixture."""
        func_uuids = [func.uuid for func in fix.functions]
        for addr, uuid in self.table.items():
            if uuid in func_uuids:
                yield addr

    def unpatch_function(self, func: 'FixtureFunction'):
        """Remove a function from the registry table, if it is
        patched there."""
        addr = self.get_function_patch(func)
        if addr:
            del self.table[addr]

    def patch_fixture(self, fixture: 'Fixture', addr: int = None):
        """Patch all channels of a fixture from a given start address,
        or provide no start address or zero to patch automatically."""
        if not addr:
            addr = self.get_start_address(fixture.dmx_size())
        if not self.is_valid_start(addr, fixture.dmx_size()):
            raise exception.InsufficientAvailableChannels(self, fixture.dmx_size())
        for func in fixture.physical_functions():
            for i in range(0, len(func.offset)):
                self.table[addr + i] = func.uuid
            addr += len(func.offset)

    def unpatch_fixture(self, fixture: 'Fixture'):
        """Unpatch all channels of a fixture which appear in this
        registry."""
        patch_addrs = [i for i in self.get_fixture_patch(fixture)]
        for addr in patch_addrs:
            del self.table[addr]


class Structure(ArbitraryDataObject):

    file_node_str = 'structure'
    command_str = 'Structure'
    omitted_data_tags = ArbitraryDataObject.omitted_data_tags + \
        ['structure_type']

    def __init__(self, structure_type: str = None, *args, **kwargs):
        super().__init__(data={'structure_type': structure_type},
                         *args, **kwargs)

    def get_text_widget(self):
        if not self.label:
            label = UNLABELLED_STRING
        else:
            label = self.label
        structure_type = self.data.get('structure_type', 'no type')
        if not structure_type:
            structure_type = 'no type'
        return [(self.file_node_str, str(self.ref)), ' ', label, ' (',
                structure_type, ')']


ALL_TYPES = [Cue, Fixture, Filter, Group, AllPalette, BeamPalette,
             ColourPalette, FocusPalette, IntensityPalette, Registry,
             Structure]
COMMAND_STR_MAP = {obj.command_str: obj for obj in ALL_TYPES}
FILE_NODE_STR_MAP = {obj.file_node_str: obj for obj in ALL_TYPES}
PALETTE_PREFIXES = {obj.palette_prefix: obj for obj in ALL_TYPES if
                    obj.__base__ == Palette}
