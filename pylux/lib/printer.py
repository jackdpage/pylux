def get_pretty_level_string(level):
    """From a level, which could be any decimal, hexadecimal or palette, return
    something which looks a bit nicer."""
    if 'BP' in level:
        return 'beampalette', level
    elif 'CP' in level:
        return 'colourpalette', level
    elif 'FP' in level:
        return 'focuspalette', level
    elif 'IP' in level:
        return 'intensitypalette', level
    elif 'AP' in level:
        return 'allpalette', level
    else:
        return level


def get_cue_level_string(obj):
    return ' ('+str(len(obj['levels']))+' levels)'


def get_generic_ref(obj):
    if 'ref' in obj:
        ref_print = (obj['type'], obj['ref'])
    elif obj['type'] == 'function':
        ref_print = ('function', str(obj['offset']))
    else:
        ref_print = ''

    return ref_print


def get_fixture_extra_text(obj):
    if 'fixture-type' in obj:
        fixture_type = obj['fixture-type']
    else:
        fixture_type = 'n/a'

    return '', fixture_type+' - ', ''


def get_cue_extra_text(obj):
    return '', '', get_cue_level_string(obj)


def get_cp_extra_text(obj):
    return ('colourpalette', 'CP'), '', get_cue_level_string(obj)


def get_bp_extra_text(obj):
    return ('beampalette', 'BP'), '', get_cue_level_string(obj)


def get_fp_extra_text(obj):
    return ('focuspalette', 'FP'), '', get_cue_level_string(obj)


def get_ip_extra_text(obj):
    return ('intensitypalette', 'IP'), '', get_cue_level_string(obj)


def get_ap_extra_text(obj):
    return ('allpalette', 'AP'), '', get_cue_level_string(obj)


def get_group_extra_text(obj):
    return '', '', ' ('+str(len(obj['fixtures']))+' fixtures)'


def get_registry_extra_text(obj):
    return 'Universe ', '', str(len(obj['table']))+' occupied'


def get_generic_text_widget(obj, pre=''):
    if 'ref' in obj:
        ref_print = (obj['type'], obj['ref']+' ')
    elif obj['type'] == 'function':
        ref_print = ('function', str(obj['offset'])+' ')
    else:
        ref_print = ''
    if 'label' in obj:
        label = obj['label']
    elif obj['type'] == 'function':
        label = obj['param']
    elif obj['type'] == 'registry':
        label = '- '
    elif obj['type'] == 'filter':
        label = obj['k']+'='+obj['v']
    else:
        label = 'Unlabelled'
    if obj['type'] in EXTRA_TEXT:
        extra = EXTRA_TEXT[obj['type']](obj)
    else:
        extra = ('', '', '')

    s = [pre, extra[0], ref_print, extra[1], label, extra[2]]

    return s


EXTRA_TEXT = {
    'fixture': get_fixture_extra_text,
    'cue': get_cue_extra_text,
    'group': get_group_extra_text,
    'registry': get_registry_extra_text,
    'colourpalette': get_cp_extra_text,
    'focuspalette': get_fp_extra_text,
    'beampalette': get_bp_extra_text,
    'intensitypalette': get_ip_extra_text,
    'allpalette': get_ap_extra_text
}