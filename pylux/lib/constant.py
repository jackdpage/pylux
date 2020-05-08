# OBJ_TYPE = ('internalsavename', 'CommandUsageName', {'fields': {}, 'to': [], 'insert': {}})
CUE_TYPE = ('cue', 'Cue', {'levels': {}})
ALL_PALETTE_TYPE = ('allpalette', 'AllPalette', {'levels': {}})
BEAM_PALETTE_TYPE = ('beampalette', 'BeamPalette', {'levels': {}})
COLOUR_PALETTE_TYPE = ('colourpalette', 'ColourPalette', {'levels': {}})
FOCUS_PALETTE_TYPE = ('focuspalette', 'FocusPalette', {'levels': {}})
INTENSITY_PALETTE_TYPE = ('intensitypalette', 'IntensityPalette', {'levels': {}})
FIXTURE_TYPE = ('fixture', 'Fixture', {})
GROUP_TYPE = ('group', 'Group', {'fixtures': []})
FILTER_TYPE = ('filter', 'Filter', {'k': '', 'v': ''})
REGISTRY_TYPE = ('registry', 'Registry', {'table': {}})
STRUCTURE_TYPE = ('structure', 'Structure', {'structure_type': ''})


CONTEXT_KEYS = [globals()[i][1] for i in globals().keys() if '_TYPE' in i]
