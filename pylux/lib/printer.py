def get_metadata_value(meta):
    s = meta['metadata-key']+': '
    if 'metadata-value' in meta:
        return s+meta['metadata-value']
    else:
        return s+'\033[31mEmpty\033[0m'


def get_fixture_string(fixture):
    if 'name' in fixture:
        name = fixture['name']
    else:
        name = '\033[31mUnnamed\033[0m'
    if 'fixture-type' in fixture:
        type = fixture['fixture-type']
    else:
        type = 'n/a'
    ref = fixture['ref']
    return type+' - '+name


def get_registry_string(registry):
    if 'patch' in registry:
        patch = registry['patch']
    else:
        patch = '\033[31mUnpatched\033[0m'
    return 'DMX512 Universe - '+patch


def get_function_string(function):
    name = function['name']
    param = function['parameter']

    return name+' ('+param+')'


def get_generic_string(obj, pre=''):
    if obj['type'] in PRINTER_INDEX:
        if 'ref' in obj:
            ref_print = ''.join(['\033[1m\033[',
                                 str(PRINTER_INDEX[obj['type']][1]), 'm',
                                 str(obj['ref']), '\033[0m '])
        else: ref_print = ''
        s = pre + ref_print + PRINTER_INDEX[obj['type']][0](obj)
        return s
    else:
        if 'name' in obj:
            name = obj['name']
        else:
            name = '\033[31mUnnamed\033[0m'
        type = obj['type']
        return name+' ('+type+')'


PRINTER_INDEX = {
    'metadata': (get_metadata_value, 94),
    'fixture': (get_fixture_string, 92),
    'registry': (get_registry_string, 93),
    'function': (get_function_string, 95),
    'scene': (None, 96)
}