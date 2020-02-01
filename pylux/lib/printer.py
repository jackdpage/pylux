UNLABELLED_STRING = '\033[31mUnnamed\033[0m'


def get_metadata_value(meta):
    s = meta['metadata-key']+': '
    if 'metadata-value' in meta:
        return s+meta['metadata-value']
    else:
        return s+'\033[31mEmpty\033[0m'


def get_fixture_string(fixture):
    if 'label' in fixture:
        label = fixture['label']
    else:
        label = '\033[31mUnlabelled\033[0m'
    if 'fixture-type' in fixture:
        type = fixture['fixture-type']
    else:
        type = 'n/a'
    ref = fixture['ref']
    return type+' - '+label


def get_registry_string(registry):
    if 'patch' in registry:
        patch = registry['patch']
    else:
        patch = '\033[31mUnpatched\033[0m'
    return 'DMX512 Universe - '+patch


def get_function_string(function):
    name = function['param']
    offset = ''.join(['\033[1m\033[95m', str(function['offset']), '\033[0m '])

    return offset+name


def get_cue_string(cue):
    if 'label' in cue:
        label = cue['label']
    else:
        label = UNLABELLED_STRING
    levels = str(len(cue['levels']))
    return 'Cue - '+label+' ('+levels+' levels)'


def get_group_string(group):
    if 'label' in group:
        label = group['label']
    else:
        label = UNLABELLED_STRING
    return 'Group - '+label+' ('+str(len(group['fixtures']))+' fixtures)'


def get_generic_ref(obj):
    if 'ref' in obj:
        ref_print = (obj['type'], obj['ref'])
    elif obj['type'] == 'function':
        ref_print = ('function', str(obj['offset']))
    else:
        ref_print = ''

    return ref_print


def get_generic_string(obj, pre=''):
    if obj['type'] in PRINTER_INDEX:
        if 'ref' in obj:
            ref_print = ''.join(['\033[1m\033[',
                                 str(PRINTER_INDEX[obj['type']][1]), 'm',
                                 str(obj['ref']), '\033[0m '])
        else:
            ref_print = ''
        s = pre + ref_print + PRINTER_INDEX[obj['type']][0](obj)
        return s
    else:
        if 'label' in obj:
            label = obj['label']
        else:
            label = UNLABELLED_STRING
        obj_type = obj['type']
        return label+' ('+obj_type+')'


def get_fixture_extra_text(obj):
    if 'fixture-type' in obj:
        fixture_type = obj['fixture-type']
    else:
        fixture_type = 'n/a'

    return '', fixture_type+' - ', ''


def get_cue_extra_text(obj):
    return '', '', ' ('+str(len(obj['levels']))+' levels)'


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
    else:
        label = ('unlabelled', 'Unlabelled')
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
    'registry': get_registry_extra_text
}

PRINTER_INDEX = {
    'metadata': (get_metadata_value, 94),
    'fixture': (get_fixture_string, 92),
    'registry': (get_registry_string, 93),
    'function': (get_function_string, 95),
    'cue': (get_cue_string, 96),
    'group': (get_group_string, 95)
}


class ProgressBar(object):
    """ProgressBar class holds the options of the progress bar.
    The options are:
        start   State from which start the progress. For example, if start is
                5 and the end is 10, the progress of this state is 50%
        end     State in which the progress has terminated.
        width   --
        fill    String to use for "filled" used to represent the progress
        blank   String to use for "filled" used to represent remaining space.
        format  Format
        incremental
    """
    def __init__(self, start=0, end=255, width=10, fill='=', blank=' ', incremental=True):
        self.start = start
        self.end = end
        self.width = width
        self.fill = fill
        self.blank = blank
        self.incremental = incremental
        self.step = 100 / float(width) #fix
        self.reset()

    def __add__(self, increment):
        increment = self._get_progress(increment)
        if 100 > self.progress + increment:
            self.progress += increment
        else:
            self.progress = 100
        return self

    def __str__(self):
        progressed = int(self.progress / self.step) #fix
        fill = (progressed-1) * self.fill
        blank = (self.width - progressed) * self.blank
        return ''.join(['[',fill,'>',blank,'] ',str(round(self.progress)),'%'])

    __repr__ = __str__

    def _get_progress(self, increment):
        return float(increment * 100) / self.end

    def reset(self):
        """Resets the current progress to the start point"""
        self.progress = self._get_progress(self.start)
        return self
