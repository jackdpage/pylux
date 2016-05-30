# qeditor.py is part of Pylux
#
# Pylux is a program for the management of lighting documentation
# Copyright 2015 Jack Page
#
# Pylux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pylux is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Manage cues in the plot file."""


import os
import pylux.clihelper
from pylux.clihelper import ReferenceBuffer
from pylux.context.context import Context, Command
from pylux.lib import cuestring, data
import libxpx.xpx as xpx
import xml.etree.ElementTree as ET


class QEditorContext(Context):

    def __init__(self):
        """Registers commands."""
        super().__init__()
        self.name = 'qeditor'

        # Internal XPX objects
        self.cue_actions = []
        self.cue_locations = []

        # Command registration

        self.register(Command('ql', self.cue_list, []))
        self.register(Command('qn', self.cue_new, [
            ('map', True, 'Location/action mapping in the form ACT@LOC')]))

        self.register(Command('al', self.action_list, []))
        self.register(Command('ao', self.action_list_output, []))
        self.register(Command('an', self.action_new, [
            ('type', True, 'The type of cue: LX or SX'),
            ('output', True, 'Output of the cue, may be a scene/chase.'),
            ('fade', True, 'fadeUp,dwell,fadeDown comma separated.')]))

        self.register(Command('ll', self.location_list, []))
        self.register(Command('ln', self.location_new, [
            ('type', True, 'abs or rel.'),
            ('event', True, 'Machine readable location description.')]))

    def post_init(self):

        self.interface.buffers['CUE'] = ReferenceBuffer(colour=94)
        self.interface.buffers['ACT'] = ReferenceBuffer(colour=95)
        self.interface.buffers['LOC'] = ReferenceBuffer(colour=96)
        self.interface.buffers['OUT'] = ReferenceBuffer(colour=93)

    def cue_list(self, parsed_input):
        '''List all cues in the effects plot.'''
        self.interface.open('CUE')
        for cue in self.plot_file.cues:
            action = cuestring.get_action_string(cue.action, self.plot_file)
            location = cuestring.get_location_string(cue.location, 
                                                     self.plot_file)
            s = action+' at '+location
            self.interface.add(s, cue, 'CUE')

    def cue_new(self, parsed_input):
        '''Create a cue by mapping an action to a location.'''
        # Split the first argument at the @ symbol, then pass this 
        # into the interface get function, then create a new cue 
        # for every action that was passed.
        actions = self.interface.get('ACT', parsed_input[0].split('@')[0])
        locations = self.interface.get('LOC', parsed_input[0].split('@')[1])
        for action in actions:
            for location in locations:
                self.plot_file.cues.append(xpx.Cue(location=location, 
                                                   action=action))
            
    def action_list(self, parsed_input):
        '''List cue actions made in this session.'''
        self.interface.open('ACT')
        for action in self.cue_actions:
            s = cuestring.get_action_string(action, self.plot_file)
            self.interface.add(s, action, 'ACT')

    def action_list_output(self, parsed_input):
        '''List all possible lighting state outputs.'''
        self.interface.open('OUT')
        if len(self.plot_file.scenes) > 0:
            print('\033[1mScenes')
            for scene in self.plot_file.scenes:
                s = scene.name
                self.interface.add(s, scene, 'OUT')
        if len(self.plot_file.chases) > 0:
            print('\033[1mChases')
            for chase in self.plot_file.chases:
                s = chase.name
                self.interface.add(s, chase, 'OUT')

    def action_new(self, parsed_input):
        '''Create a new cue action.'''
        cue_type = parsed_input[0]
        fade = tuple(parsed_input[2].split(','))
        if cue_type.lower() == 'lx':
            output = self.interface.get('OUT', parsed_input[1])[0]
            output_ref = xpx.XPXReference(output.uuid)
            self.cue_actions.append(xpx.CueAction(type='lx', fade=fade, 
                                                  output=output_ref))
        elif cue_type.lower() == 'sx':
            self.cue_actions.append(xpx.CueAction(type='sx', fade=fade,
                                                  output=parsed_input[1]))

    def location_list(self, parsed_input):
        '''List cue locations made in this session.'''
        self.interface.open('LOC')
        for location in self.cue_locations:
            s = cuestring.get_location_string(location, self.plot_file)
            self.interface.add(s, location, 'LOC')

    def location_new(self, parsed_input):
        '''Create a new cue location.'''
        self.cue_locations.append(xpx.CueLocation(type=parsed_input[0],
                                                  event=parsed_input[1]))
 
        
def get_context():
    return QEditorContext()
