from pylux import document


UNLABELLED_STR = '[Unlabelled]'


def get_pretty_level_string(level, doc=None, show_labels=False, raw_data=False, function=None):
    """From a level, which could be any decimal, hexadecimal or palette, return
    something which looks a bit nicer."""
    if len(level) < 2:
        return level
    if level[0:2] in document.PALETTE_PREFIXES:
        palette_type = document.PALETTE_PREFIXES[level[0:2]]
        palette = doc.get_by_ref(palette_type, level[2:])
        if raw_data and function:
            display_str = palette.get_function_level(function)
            if not display_str:
                display_str = level
        elif show_labels and palette.label:
            display_str = palette.label
        else:
            display_str = level
        return palette_type.file_node_str, display_str
    else:
        return level


def get_generic_ref(obj):
    if hasattr(obj, 'ref'):
        ref_print = (obj.file_node_str, str(obj.ref))
    elif type(obj) == document.FixtureFunction:
        ref_print = ('function', ','.join([str(i) for i in obj.offset]))
    else:
        ref_print = ''

    return ref_print


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
    extra = ('', '', '')

    s = [pre, extra[0], ref_print, extra[1], label, extra[2]]

    return s


def get_metadata_string(k, v):

    s = [('metadata', k), ': ', v]

    return s
