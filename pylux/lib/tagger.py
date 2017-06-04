import math

import reference

def tag_fixture_colour(fixture):
    if 'gel' in fixture:
        fixture['colour'] = reference.gel_colours[fixture['gel']]
    else:
        fixture['colour'] = 'White'

def tag_fixture_rotation(fixture):
    position = (float(fixture['posX']), float(fixture['posY']))
    focus = (float(fixture['focusX']), float(fixture['focusY']))
    fixture['rotation'] = math.degrees(math.atan2(focus[1] - position[1], focus[0] - position[0]))

def tag_fixture_all(fixture):
    tag_fixture_colour(fixture)
    tag_fixture_rotation(fixture)