# gui.py is part of Pylux
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
import pylux.clihelper as clihelper
import xml.etree.ElementTree as ET
import gi.repository
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MainWindow(Gtk.Window):
    """The main window in which things happen.

    Consists of a notebook, each page of which edits different 
    components of the plot file.
    """

    def __init__(self):
        Gtk.Window.__init__(self, title='Pylux')
        self.set_default_size(700, 500)
        self.main_container = Gtk.Box(spacing=6, 
                                 orientation=Gtk.Orientation.VERTICAL)
        self.add(self.main_container)
        self.main_notebook = Gtk.Notebook()
        self.main_container.pack_start(self.main_notebook, True, True, 0)
        self.main_notebook.append_page(FixturesPage(), Gtk.Label('Fixtures'))
        self.main_notebook.append_page(RegistriesPage(), 
                                       Gtk.Label('Registries'))
        self.main_notebook.append_page(CuesPage(), Gtk.Label('Cues'))


class FixturesPage(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self, spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.set_border_width(10)
        self.fixture_list = Gtk.ListBox()
        self.pack_start(self.fixture_list, True, True, 0)
        self.fixtures = plot.FixtureList(PLOT_FILE).fixtures
        for fixture in self.fixtures:
            listbox_row = self.FixtureListItem(fixture)
            self.fixture_list.add(listbox_row)

    class FixtureListItem(Gtk.ListBoxRow):

        def __init__(self, fixture):
            Gtk.ListBoxRow.__init__(self)
            self.fixture = fixture
            self.container_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            self.add(self.container_box)
            # Label showing fixture name or type
            self.name_label = Gtk.Label(clihelper.get_fixture_print(fixture))
            self.container_box.pack_start(self.name_label, False, True, 0)
            # Action buttons
            button_info = Gtk.Button.new_from_icon_name('dialog-information', 1)
            button_clone = Gtk.Button.new_from_icon_name('edit-copy', 1)
            button_delete = Gtk.Button.new_from_icon_name('edit-delete', 1)
            self.container_box.pack_end(button_delete, False, False, 0)
            self.container_box.pack_end(button_clone, False, False, 0)
            self.container_box.pack_end(button_info, False, False, 0)
        

class RegistriesPage(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self, spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.set_border_width(10)
        self.registry_list = Gtk.ListBox()
        self.pack_start(self.registry_list, True, True, 0)
        self.registries = plot.RegistryList(PLOT_FILE).registries
        for registry in self.registries:
            listbox_row = self.RegistryListItem(registry)
            self.registry_list.add(listbox_row)

    class RegistryListItem(Gtk.ListBoxRow):

        def __init__(self, registry):
            Gtk.ListBoxRow.__init__(self)
            self.registry = registry
            self.container_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            self.add(self.container_box)
            # Label showing universe
            self.universe_label = Gtk.Label(registry.universe)
            self.container_box.pack_start(self.universe_label, False, True, 0)
            # Action buttons
            button_list = Gtk.Button.new_from_icon_name('dialog-information', 1)
            self.container_box.pack_end(button_list, False, False, 0)


class CuesPage(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self, spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.set_border_width(10)
        self.add(Gtk.Label('cues'))


class SplashWindow(Gtk.Window):
    """Window prompting user to load a plot file.

    Displayed when no plot file is loaded.
    """

    def __init__(self):
        Gtk.Window.__init__(self, title='Welcome to Pylux')
        self.set_default_size(650, 400)
        self.main_container = Gtk.Box(spacing=6, 
                                 orientation=Gtk.Orientation.VERTICAL)
        self.add(self.main_container)
        self.main_container.pack_start(Gtk.Label('no plot file'), True, True, 0)
    

def main():
    if PLOT_FILE.file == None:
        window = SplashWindow()
    else:
        window = MainWindow()
    window.connect('delete-event', Gtk.main_quit)
    window.show_all()
    Gtk.main()


if __name__ == 'pylux_root':
    main()
