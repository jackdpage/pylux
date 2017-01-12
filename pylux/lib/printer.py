def get_metadata_value(meta):
    if 'metadata-value' in meta:
        return meta['metadata-value']
    else:
        return '\033[31mEmpty\033[0m'


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
