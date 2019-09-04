# Generates some automatic tags based on the value of other tags or information
# available.

import math

import document
import reference


def tag_fixture_colour(doc, fixture):
    if 'gel' in fixture:
        fixture['colour'] = reference.gel_colours[fixture['gel']]
    else:
        fixture['colour'] = 'White'


def tag_fixture_rotation(doc, fixture):
    pos = [float(fixture['posX']), float(fixture['posY'])]
    focus = [float(fixture['focusX']), float(fixture['focusY'])]
    fixture['rotation'] = math.degrees(math.atan2(focus[1] - pos[1], focus[0] - pos[0]))


def tag_fixture_patch(doc, fixture):
    if 'personality' in fixture:
        start_func = document.get_by_value(fixture['personality'], 'offset', 1)[0]
        if start_func:
            location = document.get_function_patch_location(doc, start_func)
            fixture['patch-start'] = location


def tag_fixture_all(doc, fixture):
    tag_fixture_colour(doc, fixture)
    tag_fixture_rotation(doc, fixture)
    tag_fixture_patch(doc, fixture)
