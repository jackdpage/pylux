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
import gi.repository
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class TextInputDialog(Gtk.Dialog):

    def __init__(self, parent, title):
        Gtk.Dialog.__init__(self, title, parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)
        self.entry_box = Gtk.Entry()
        self.container_box = self.get_content_area()
        self.container_box.add(self.entry_box)
        self.show_all()


class FixturesWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Fixtures')
        self.box_container = Gtk.Box(spacing=6, 
                                 orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box_container)

        # Create MenuBar
        self.menubar = Gtk.MenuBar()
        self.box_container.pack_start(self.menubar, True, True, 0)
        self.menu_file = Gtk.MenuItem(label='File')

        self.gui_list_fixtures()


        # Create fixture action buttons
        self.button_fixture_new = Gtk.Button(label='New fixture')
        self.button_fixture_new.connect('clicked', self.action_fixture_new)
        self.button_fixture_remove = Gtk.Button(label='Remove fixture')
        self.button_fixture_remove.connect('clicked', 
                                           self.action_fixture_remove)
        self.button_fixture_clone = Gtk.Button(label='Clone fixture')
        self.button_fixture_clone.connect('clicked', self.action_fixture_clone)

        # Pack fixture action buttons into Box
        self.box_fixture_buttons = Gtk.Box(spacing=4)
        self.box_container.pack_start(self.box_fixture_buttons, True, True, 0)
        self.box_fixture_buttons.pack_start(self.button_fixture_new, 
                                            True, True, 0)
        self.box_fixture_buttons.pack_start(self.button_fixture_remove, 
                                            True, True, 0)
        self.box_fixture_buttons.pack_start(self.button_fixture_clone, 
                                            True, True, 0)

    def gui_list_fixtures(self):
        """Create an empty ListBox for fixtures."""
        self.listbox_fixtures = Gtk.ListBox()
        self.listbox_fixtures.set_selection_mode(Gtk.SelectionMode.NONE)
        self.box_container.pack_start(self.listbox_fixtures, True, True, 0)
        fixtures = plot.FixtureList(PLOT_FILE)
        for fixture in fixtures.fixtures:
            self.gui_add_fixture(fixture)

    def gui_add_fixture(self, fixture):
        """Add a fixture to the ListBox as a ListBoxRow."""
        listbox_row_fixture = Gtk.ListBoxRow()
        box_listbox_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, 
                                   spacing=20)
        listbox_row_fixture.add(box_listbox_row)
        if 'name' in fixture.data:
            fixture_name = fixture.data['name']
        else:
            fixture_name = fixture.data['type']
        label_fixture_name = Gtk.Label(fixture_name)
        label_fixture_uuid = Gtk.Label(fixture.uuid)
        box_listbox_row.pack_start(label_fixture_name, True, True, 0)
        box_listbox_row.pack_start(label_fixture_uuid, True, True, 0)
        self.listbox_fixtures.add(listbox_row_fixture)

    def action_fixture_new(self, widget):
        type_dialog = TextInputDialog(self, 'Fixture Type')
        response = type_dialog.run()
        if response == Gtk.ResponseType.OK:
            fixture_type = type_dialog.entry_box.get_text()
            fixture = plot.Fixture(PLOT_FILE)
            try:
                fixture.new(fixture_type, '/usr/share/pylux/fixture/')
            except FileNotFoundError:
                print('Error: Couldn\'t find a fixture file with this name')
            else:
                fixture.add()
                fixture.save()
                self.gui_add_fixture(fixture)
                self.show_all()
        type_dialog.destroy()

    def action_fixture_remove(self, widget):
        print('Removing fixture...')

    def action_fixture_clone(self, widget):
        print('Cloning fixture...')

    def action_fixture_getall(self, widget, fixture):
        
        


def main():
    win = FixturesWindow()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == 'pylux_root':
    main()
