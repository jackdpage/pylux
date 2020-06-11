from pylux import document


def get_pretty_level_string(level, doc=None, show_labels=False, raw_data=False, function=None):
    """From a level, which could be any decimal, hexadecimal or palette, return
    something which looks a bit nicer."""
    if len(level) < 2:
        return level
    if level[0:2] in document.PALETTE_ABBRS:
        formatting = document.PALETTE_ABBRS[level[0:2]]
        if raw_data and function:
            palette = document.get_palette_by_cue_string(doc, level)
            display_str = document.get_palette_raw_level(function, palette)
        elif show_labels:
            display_str = document.get_palette_by_cue_string(doc, level).get('label', level)
        else:
            display_str = level
        return formatting, display_str
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


def get_fixture_extra_text(obj, **kwargs):
    if 'fixture-type' in obj:
        fixture_type = obj['fixture-type']
    else:
        fixture_type = 'n/a'

    if not kwargs['label']:
        return '', fixture_type, ''
    else:
        return '', fixture_type+' - ', ''


def get_cue_extra_text(obj, **kwargs):
    if not kwargs['label']:
        return '', '[Unlabelled]', get_cue_level_string(obj)
    else:
        return '', '', get_cue_level_string(obj)


def get_cp_extra_text(obj, **kwargs):
    return ('colourpalette', 'CP'), '', get_cue_level_string(obj)


def get_bp_extra_text(obj, **kwargs):
    return ('beampalette', 'BP'), '', get_cue_level_string(obj)


def get_fp_extra_text(obj, **kwargs):
    return ('focuspalette', 'FP'), '', get_cue_level_string(obj)


def get_ip_extra_text(obj, **kwargs):
    return ('intensitypalette', 'IP'), '', get_cue_level_string(obj)


def get_ap_extra_text(obj, **kwargs):
    return ('allpalette', 'AP'), '', get_cue_level_string(obj)


def get_group_extra_text(obj, **kwargs):
    return '', '', ' ('+str(len(obj['fixtures']))+' fixtures)'


def get_registry_extra_text(obj, **kwargs):
    return 'Universe ', '', str(len(obj['table']))+' occupied'


def get_structure_extra_text(obj, **kwargs):
    if 'structure_type' not in obj:
        structure_type = 'no type'
    else:
        if obj['structure_type'] == '':
            structure_type = 'no type'
        else:
            structure_type = obj['structure_type']
    return '', '', ' ('+structure_type+')'


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
        label = ''
    if obj['type'] in EXTRA_TEXT:
        extra = EXTRA_TEXT[obj['type']](obj, label=label)
    else:
        extra = ('', '', '')

    s = [pre, extra[0], ref_print, extra[1], label, extra[2]]

    return s


def get_metadata_string(k, v):

    s = [('metadata', k), ': ', v]

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
    'allpalette': get_ap_extra_text,
    'structure': get_structure_extra_text
}