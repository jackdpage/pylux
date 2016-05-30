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

        self.register(Command('al', self.action_list, []))

        self.register(Command('ll', self.location_list, []))

    def post_init(self):

        self.interface.buffers['CUE'] = ReferenceBuffer(colour=94)
        self.interface.buffers['ACT'] = ReferenceBuffer(colour=95)
        self.interface.buffers['LOC'] = ReferenceBuffer(colour=96)

    def cue_list(self, parsed_input):
        '''List all cues in the effects plot.'''
        self.interface.open('CUE')
        for cue in self.plot_file.cues:
            s = ''.join([cuestring.get_action_string(cue.action),' at ',
                         cuestring.get_location_string(cue.location)])
            self.interface.add(s, cue, 'CUE')

    def action_list(self, parsed_input):
        '''List cue actions made in this session.'''
        self.interface.open('ACT')
        for action in self.cue_actions:
            s = cuestring.get_action_string(action)
            self.interface.add(s, action, 'ACT')

    def location_list(self, parsed_input):
        '''List cue locations made in this session.'''
        self.interface.open('LOC')
        for location in self.cue_locations:
            s = cuestring.get_location_string(location)
            self.interface.add(s, location, 'LOC')
 
        
def get_context():
    return QEditorContext()
