def get_metadata_value(meta):
    s = meta['metadata-key']+': '
    if 'metadata-value' in meta:
        return s+meta['metadata-value']
    else:
        return s+'\033[31mEmpty\033[0m'


def get_fixture_string(fixture):
    if 'fixture-name' in fixture:
        name = fixture['fixture-name']
    else:
        name = '\033[31mUnnamed\033[0m'
    if 'fixture-type' in fixture:
        type = fixture['fixture-type']
    else:
        type = 'n/a'
    return type+' - '+name


def get_generic_string(obj):
    if obj['type'] in PRINTER_INDEX:
        return PRINTER_INDEX[obj['type']](obj)
    else:
        if 'name' in obj:
            name = obj['name']
        else:
            name = '\033[31mUnnamed\033[0m'
        type = obj['type']
        return name+' ('+type+')'

PRINTER_INDEX = {
    'metadata': get_metadata_value,
    'fixture': get_fixture_string,
}