# command/shortcut/type(object/action)/expected_after/in_init
KEYMAPS = [
    ('About', 'a', 'action', ['Fixture', 'Group'], False),
    ('All', 'a', 'object', 'any', True),
    ('Append', 'A', 'action', 'Group', False),
    ('CompleteFrom', 'C', 'action', 'Fixture', False),
    ('CopyTo', 'c', 'action', 'any', False),
    ('Create', 'n', 'action', 'any', False),
    ('CreateFrom', 'N', 'action', 'Fixture', False),
    ('Cue', 'q', 'object', 'any', True),
    ('Display', 'd', 'action', 'any', True),
    ('File', 'f', 'object', 'any', True),
    ('Fixture', 'x', 'object', 'any', True),
    ('Group', 'g', 'object', 'any', True),
    ('ImportAscii', 'i', 'action', 'File', False),
    ('Metadata', 'm', 'object', 'any', True),
    ('Open', 'o', 'action', 'File', False),
    ('Patch', 'p', 'action', 'Fixture', False),
    ('Registry', 'r', 'object', 'any', True),
    ('Remove', 'r', 'action', 'any', False),
    ('Set', 's', 'action', 'any', False),
    ('Write', 'w', 'action', 'File', False)
]
DEFAULT_KEYMAP = [i for i in KEYMAPS if i[4]]
NO_KEYMAP = []
ALL_OBJECTS = [i for i in KEYMAPS if i[2] == 'object']
ALL_ACTIONS = [i for i in KEYMAPS if i[2] == 'action']
NUMERIC_MAP = {'a': 'All'}


def get_keymap(fragment):
    """Receive a command fragment and return a list of appropriate keymappings for the expected next word in the
    command"""
    keywords = fragment.split()
    if len(keywords) == 0:
        # Return the objects which can be used at the start of commands
        return _generate_keymap(DEFAULT_KEYMAP)
    if len(keywords) == 1:
        # Return any special characters which can be used in place of numbers
        if keywords[0] == 'File':
            legal_actions = [i for i in ALL_ACTIONS if i[3] in ['any', keywords[0]] or keywords[0] in i[3]]
            return _generate_keymap(legal_actions)
        elif keywords[0] in [i[0] for i in ALL_OBJECTS]:
            return {**_generate_keymap(DEFAULT_KEYMAP), **NUMERIC_MAP}
    if len(keywords) == 2:
        # Return a list of actions which are suitable for the object type in this command fragment
        if keywords[0] == 'File':
            return {}
        else:
            legal_actions = [i for i in ALL_ACTIONS if i[3] in ['any', keywords[0]] or keywords[0] in i[3]]
            return _generate_keymap(legal_actions, pre=' ')


def _generate_keymap(tuple_list, pre='', post=' '):
    keymap = {}
    for i in tuple_list:
        keymap[i[1]] = pre+i[0]+post
    return keymap
