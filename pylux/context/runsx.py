# runsx.py is part of Pylux
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

"""Run the sound cues from the plot file.

runsx uses ffplay to run cues with the 'SX' type in the plot file.
"""

import os
import subprocess
import pylux.plot as plot
import pylux.clihelper as clihelper
import logging
from pylux.context.context import Context, Command
from pylux import get_data
from pylux.exception import *


class CueStack():

    def __init__(self, cues):
        self.cues = cues


class RunSxContext(Context):

    def __init__(self):
        super().__init__()
        self.name = 'runsx'
        # Register commands
        self.register(Command('ql', self.cue_list, []))
        self.register(Command('qp', self.cue_play, ['cue']))
        self.register(Command('ss', self.stack_start, ['start']))
        self.register(Command('sa', self.stack_advance, []))
        self.register(Command('sx', self.stack_exit, []))

    def post_init(self):
        super().post_init()
        self.cues = plot.CueList(self.plot_file)
        self.cues.assign_identifiers()
        for cue in self.cues.cues:
            if cue.data['type'].upper() != 'SX' or 'file' not in cue.data:
                self.cues.cues.remove(cue)

    def cue_list(self, parsed_input):
        for cue in sorted(self.cues.cues, key=lambda cue: cue.key):
            print(''.join(['\033[4m',str(cue.key),
                           '\033[0m at \'',cue.data['location'],
                           '\': ',cue.data['file']]))
            self.interface.append(cue.key, cue)

    def cue_play(self, parsed_input):
        to_play = self.interface.get(parsed_input[0])
        files = []
        for cue in to_play:
            files.append(cue.data['file'])
        for effect in files:
            subprocess.run(['mplayer', effect])

    def stack_start(self, parsed_input):
        self.stack_instance = CueStack(self.cues)

    def stack_advance(self, parsed_input):
        return None

    def stack_exit(self, parsed_input):
        return None

def get_context():
    return RunSxContext()
