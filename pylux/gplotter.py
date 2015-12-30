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

import plotter
from tkinter import *
from tkinter.ttk import *

class GuiApp(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_interface()

    def create_interface(self):
        self.fixture_list_tree = Treeview(self, selectmode='browse', 
            columns=['tag', 'value'])
        self.fixture_list_tree.pack()
        xml_fixture_list = PROJECT_FILE.root.find('fixtures')
        for fixture in xml_fixture_list:
            uuid = fixture.get('uuid')
            olid = fixture.get('olid')
            self.fixture_list_tree.insert('', 'end', uuid, text=uuid, 
                values=[olid])
            data = []
            for data_item in fixture:
                name = data_item.tag
                value = data_item.text
                self.fixture_list_tree.insert(uuid, 'end', values=[name, value])
                data.append(data_item.text)

def main():
    plotter.init()
    global PROJECT_FILE
    PROJECT_FILE = plotter.FileManager()
    if plotter.LAUNCH_ARGS.file != None:
        PROJECT_FILE.load(plotter.LAUNCH_ARGS.file)
        print('Using project file '+PROJECT_FILE.file) 
    root = Tk()
    app = GuiApp(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
