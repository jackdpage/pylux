import math

import reference

def tag_fixture_colour(fixture):
    fixture['colour'] = reference.gel_colours[fixture['gel']]

def tag_fixture_location(fixture):
    fixture['posX'] = fixture['pos'].split(',')[0]
    fixture['posY'] = fixture['pos'].split(',')[1]
    fixture['posZ'] = fixture['pos'].split(',')[2]

def tag_fixture_focus(fixture):
    fixture['focusX'] = fixture['focus'].split(',')[0]
    fixture['focusY'] = fixture['focus'].split(',')[1]
    fixture['focusZ'] = fixture['focus'].split(',')[2]

def tag_fixture_rotation(fixture):
    position = (float(fixture['posX']), float(fixture['posY']))
    focus = (float(fixture['focusX']), float(fixture['focusY']))
    fixture['rotation'] = math.degrees(math.atan2(focus[1] - position[1], focus[0] - position[0]))

def tag_fixture_all(fixture):
    tag_fixture_colour(fixture)
    tag_fixture_location(fixture)
    tag_fixture_focus(fixture)
    tag_fixture_rotation(fixture)