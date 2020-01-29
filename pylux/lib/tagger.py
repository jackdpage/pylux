# Generates some automatic tags based on the value of other tags or information
# available.

import math

from pylux import document, reference


def tag_fixture_colour(fixture):
    if 'gel' in fixture:
        fixture['colour'] = reference.gel_colours[fixture['gel']]
    else:
        fixture['colour'] = 'White'


def tag_fixture_rotation(fixture):
    if 'posX' or 'posY' or 'focusX' or 'focusY' not in fixture:
        pass
    else:
        pos = [float(fixture['posX']), float(fixture['posY'])]
        focus = [float(fixture['focusX']), float(fixture['focusY'])]
        fixture['rotation'] = math.degrees(math.atan2(focus[1] - pos[1], focus[0] - pos[0]))


def tag_fixture_patch(doc, fixture):
    if 'personality' in fixture:
        start_func = None
        for func in fixture['personality']:
            if not start_func:
                start_func = func
            elif func['offset'] < start_func['offset']:
                start_func = func
        if start_func:
            location = document.get_function_patch_location(doc, start_func)
            fixture['patch-start'] = location


def tag_fixture_all(doc, fixture):
    tag_fixture_all_doc_independent(fixture)
    tag_fixture_patch(doc, fixture)

def tag_fixture_all_doc_independent(fixture):
    tag_fixture_colour(fixture)
    tag_fixture_rotation(fixture)
