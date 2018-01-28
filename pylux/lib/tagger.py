import math

import reference

def tag_fixture_colour(fixture):
    if 'gel' in fixture:
        fixture['colour'] = reference.gel_colours[fixture['gel']]
    else:
        fixture['colour'] = 'White'

def tag_fixture_rotation(fixture):
    if 'pos' or 'focus' not in fixture:
        pass
    else:
        pos = [float(i) for i in(fixture['pos'].split(','))]
        focus = [float(i) for i in(fixture['focus'].split(','))]
        fixture['rotation'] = math.degrees(math.atan2(focus[1] - pos[1], focus[0] - pos[0]))

def tag_fixture_all(fixture):
    tag_fixture_colour(fixture)
    tag_fixture_rotation(fixture)