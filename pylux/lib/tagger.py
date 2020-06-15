# Generates some automatic tags based on the value of other tags or information
# available.

import math

from pylux import OLDdocument, reference


def tag_fixture_colour(fixture):
    if 'gel' in fixture:
        try:
            fixture['colour'] = reference.gel_colours[fixture['gel']]
        except KeyError:
            fixture['colour'] = 'White'
    else:
        fixture['colour'] = 'White'


def tag_fixture_rotation(fixture):
    # If we can't calculate the rotation (e.g. a moving head would not have any focus values) then set the rotation
    # to zero to have the fixture point in its default orientation. Unless the rotation tag already exists, in which
    # case leave it as-is in case it was added manually.
    if 'posX' in fixture and 'posY' in fixture and 'focusX' in fixture and 'focusY' in fixture:
        pos = [float(fixture['posX']), float(fixture['posY'])]
        focus = [float(fixture['focusX']), float(fixture['focusY'])]
        fixture['rotation'] = 90 - math.degrees(math.atan2(focus[1] - pos[1], focus[0] - pos[0]))
    elif 'rotation' not in fixture:
        fixture['rotation'] = 0


def tag_fixture_patch(doc, fixture):
    if 'personality' in fixture:
        start_func = None
        for func in fixture['personality']:
            if not start_func:
                start_func = func
            elif func['offset'] < start_func['offset']:
                start_func = func
        if start_func:
            location = OLDdocument.get_function_patch_location(doc, start_func)
            fixture['patch-start'] = location


def tag_fixture_all(doc, fixture):
    tag_fixture_all_doc_independent(fixture)
    tag_fixture_patch(doc, fixture)


def tag_fixture_all_doc_independent(fixture):
    tag_fixture_colour(fixture)
    tag_fixture_rotation(fixture)
