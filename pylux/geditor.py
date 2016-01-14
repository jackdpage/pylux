#!/usr/bin/python3

# gplotter.py is part of Pylux
#
# Pylux is a program for the management of lighting documentation
# Copyright 2015 Jack Page
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

import pylux.plot as plot
from tkinter import *
from tkinter.ttk import *
from tkinter import tix
from tkinter import constants
from tkinter import filedialog

class GuiApp(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.master = master
        self.create_menubar()
        try:
            self.create_fixtures_list()
        except AttributeError:
            print('no plot file')
        self.create_fixture_action_buttons()
    
    def create_menubar(self):
        self.menubar = Menu(self)
        self.master.config(menu=self.menubar)
        self.file_menu = Menu(self.menubar)
        self.menubar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Open...', 
            command=self.command_file_load)
        self.debug_menu = Menu(self.menubar)
        self.menubar.add_cascade(label='Debug', menu=self.debug_menu)
        self.debug_menu.add_command(label='GenFixList',
            command=self.create_fixtures_list)

    def create_fixtures_list(self):
        self.gfixtures_tree = Treeview(self, selectmode='browse', 
            columns=['tag', 'value'])
        fixtures = plot.FixtureList(PLOT_FILE)
        for fixture in fixtures.fixtures:
            uuid = fixture.uuid
            if 'name' in fixture.data:
                name = fixture.data['name']
            else:
                name = fixture.data['type']
            self.gfixtures_tree.insert('', 'end', uuid, text=name, 
                values=[fixture.data['type']])
            for data_item in fixture.data:
                name = data_item
                value = fixture.data[data_item]
                self.gfixtures_tree.insert(uuid, 'end', values=[name, value])
        self.gfixtures_tree.pack()

    def create_fixture_action_buttons(self):
        self.gnew_fixture_button = Button(self)
        self.gnew_fixture_button['text'] = 'New fixture'
        self.gnew_fixture_button['command'] = self.command_fixture_add() 
        self.gnew_fixture_button.pack(side='bottom')

    def command_file_load(self):
        gfile_dialog = filedialog.askopenfile()
        PLOT_FILE.load(gfile_dialog.name)

    def command_fixture_add(self):
        print('adding a fixture.... shhhh only pretending')


def main():
    root = tix.Tk()
    app = GuiApp(master=root)
    app.mainloop()

if __name__ == 'pylux_root':
    main()
