# Generates some automatic tags based on the value of other tags or information
# available.

import math

from pylux import reference


def tag_fixture_colour(fixture):
    if 'gel' in fixture.data:
        try:
            fixture.data['colour'] = reference.gel_colours[fixture.data['gel']]
        except KeyError:
            fixture.data['colour'] = 'White'
    else:
        fixture.data['colour'] = 'White'


def tag_fixture_rotation(fixture):
    # If we can't calculate the rotation (e.g. a moving head would not have any focus values) then set the rotation
    # to zero to have the fixture point in its default orientation. Unless the rotation tag already exists, in which
    # case leave it as-is in case it was added manually.
    if 'posX' in fixture.data and 'posY' in fixture.data and 'focusX' in fixture.data and 'focusY' in fixture.data:
        pos = [float(fixture.data['posX']), float(fixture.data['posY'])]
        focus = [float(fixture.data['focusX']), float(fixture.data['focusY'])]
        fixture.data['rotation'] = 90 - math.degrees(math.atan2(focus[1] - pos[1], focus[0] - pos[0]))
    elif 'rotation' not in fixture.data:
        fixture.data['rotation'] = 0


def tag_fixture_patch(doc, fixture):
    if len(fixture.functions):
        patch = doc.get_function_patch(fixture.functions[0])
        fixture.data['patch_start'] = patch


def tag_fixture_all(doc, fixture):
    tag_fixture_all_doc_independent(fixture)
    tag_fixture_patch(doc, fixture)


def tag_fixture_all_doc_independent(fixture):
    tag_fixture_colour(fixture)
    tag_fixture_rotation(fixture)
