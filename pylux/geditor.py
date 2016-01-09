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

import plot
from tkinter import *
from tkinter.ttk import *
from tkinter import tix
from tkinter import constants
from tkinter import filedialog

class GuiApp(Frame):

    def __init__(self, plot_file, config,  master=None):
        Frame.__init__(self, master)
        self.pack()
        self.master = master
        self.plot_file = plot_file
        self.config = config
        self.create_menubar()
        try:
            self.create_fixtures_list()
        except AttributeError:
            print('no plot file')
    
    def create_menubar(self):
        self.menubar = Menu(self)
        self.master.config(menu=self.menubar)
        self.file_menu = Menu(self.menubar)
        self.menubar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Open...', 
            command=self.command_load_file)
        self.debug_menu = Menu(self.menubar)
        self.menubar.add_cascade(label='Debug', menu=self.debug_menu)
        self.debug_menu.add_command(label='GenFixList',
            command=self.create_fixtures_list)

    def create_fixtures_list(self):
        self.gfixtures_tree = Treeview(self, selectmode='browse', 
            columns=['tag', 'value'])
        fixtures = plot.FixtureList(self.plot_file)
        for fixture in fixtures.fixtures:
            uuid = fixture.uuid
            olid = fixture.olid
            try:
                name = fixture.data['name']
            except IndexError:
                name = uuid
            self.gfixtures_tree.insert('', 'end', uuid, text=name, 
                values=[olid])
            for data_item in fixture.data:
                name = data_item
                value = fixture.data[data_item]
                self.gfixtures_tree.insert(uuid, 'end', values=[name, value])
        self.gfixtures_tree.pack()

    def command_load_file(self):
        gfile_dialog = filedialog.askopenfile()
        self.plot_file.load(gfile_dialog.name)


def main(plot_file, config):
    root = tix.Tk()
    app = GuiApp(plot_file, config, master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
