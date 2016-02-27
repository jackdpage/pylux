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
        self.main_container = Gtk.Box(spacing=6, 
                                 orientation=Gtk.Orientation.VERTICAL)
        self.set_default_size(500, 800)
        self.add(self.main_container)
        self.main_notebook = Gtk.Notebook()
        self.main_container.pack_start(self.main_notebook, True, True, 0)
        self.main_notebook.append_page(FixturesPage(), Gtk.Label('Fixtures'))
        self.main_notebook.append_page(RegistriesPage(), 
                                       Gtk.Label('Registries'))
        self.main_notebook.append_page(CuesPage(), Gtk.Label('Cues'))


class FixturesPage(Gtk.ScrolledWindow):

    def __init__(self):
        Gtk.ScrolledWindow.__init__(self, None, None)
        self.fixture_list = Gtk.ListBox()
        self.add_with_viewport(self.fixture_list)
        self.fixtures = plot.FixtureList(PLOT_FILE).fixtures
        for fixture in self.fixtures:
            listbox_row = self.FixtureListItem(fixture)
            self.fixture_list.add(listbox_row)

    class FixtureListItem(Gtk.ListBoxRow):
        """Display a single fixture and some action buttons.

        An extension of ListBoxRow that displays a fixture's name or 
        type, and a series of action buttons to perform actions on 
        that fixture.
        """

        def __init__(self, fixture):
            """Initialise the ListBoxRow and add the buttons."""
            Gtk.ListBoxRow.__init__(self)
            self.fixture = fixture
            self.container_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            self.add(self.container_box)
            # Label showing fixture name or type
            self.name_label = Gtk.Label(clihelper.get_fixture_print(fixture))
            self.container_box.pack_start(self.name_label, False, True, 0)
            # Action buttons
            button_info = Gtk.Button.new_from_icon_name('dialog-information', 1)
            button_info.connect('clicked', self.fixture_getall)
            button_clone = Gtk.Button.new_from_icon_name('edit-copy', 1)
            button_clone.connect('clicked', self.fixture_clone)
            button_delete = Gtk.Button.new_from_icon_name('edit-delete', 1)
            button_delete.connect('clicked', self.fixture_remove)
            self.container_box.pack_end(button_delete, False, False, 0)
            self.container_box.pack_end(button_clone, False, False, 0)
            self.container_box.pack_end(button_info, False, False, 0)

        def fixture_getall(self, widget):
            info_window = FixturesPage.FixtureInfoWindow(self.fixture)
            info_window.connect('delete-event', info_window.destroy)
            info_window.show_all()

        def fixture_clone(self, widget):
            print('Doing literally nothing.')

        def fixture_remove(self, widget):
            self.fixture.unaddress(plot.RegistryList(PLOT_FILE))
            plot.FixtureList(PLOT_FILE).remove(self.fixture)

    class FixtureInfoWindow(Gtk.Window):
        """A window showing the result of getall."""
        
        def __init__(self, fixture):
            self.fixture = fixture
            fixture_print = clihelper.get_fixture_print(fixture)
            Gtk.Window.__init__(self, title='Editing '+fixture_print)
            # Make the list store and populate
            self.list_store = Gtk.ListStore(str, str)
            for tag, value in self.fixture.data.items():
                self.list_store.append([tag, value])
            # Make the tree view from the store
            self.tree_view = Gtk.TreeView(self.list_store)
            self.add(self.tree_view)
            renderer = Gtk.CellRendererText()
            renderer_edit = Gtk.CellRendererText(editable=True)
            tag_column = Gtk.TreeViewColumn('Tag', renderer, text=0)
            self.tree_view.append_column(tag_column)
            value_column = Gtk.TreeViewColumn('Value', renderer_edit, text=1)
            self.tree_view.append_column(value_column)
            # Manage the selection
            selection = self.tree_view.get_selection()
            selection.connect('changed', self.selection_change)
            # Manage the editing
            renderer_edit.connect('edited', self.property_edit)

        def selection_change(self, selection):
            model, list_iter = selection.get_selected()
            if list_iter != None:
                print(model[list_iter][0])

        def property_edit(self, widget, path, text):
            self.list_store[path][1] = text
            self.fixture.data[self.list_store[path][0]] = text
            self.fixture.save()


class RegistriesPage(Gtk.ScrolledWindow):

    def __init__(self):
        Gtk.ScrolledWindow.__init__(self, None, None)
        self.registry_list = Gtk.ListBox()
        self.add_with_viewport(self.registry_list)
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


class CuesPage(Gtk.ScrolledWindow):

    def __init__(self):
        Gtk.ScrolledWindow.__init__(self, None, None)
        self.cues_list = Gtk.ListBox()
        self.add_with_viewport(self.cues_list)
        for cue in sorted(plot.CueList(PLOT_FILE).cues, key=lambda q: q.key):
            listbox_row = self.CueListItem(cue)
            self.cues_list.add(listbox_row)

    class CueListItem(Gtk.ListBoxRow):

        def __init__(self, cue):
            Gtk.ListBoxRow.__init__(self)
            self.cue = cue
            self.container_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            self.add(self.container_box)
            # Label showing key, type and location
            self.key_label = Gtk.Label(cue.key)
            self.type_label = Gtk.Label(cue.data['type'])
            self.location_label = Gtk.Label(cue.data['location'])
            self.container_box.pack_start(self.key_label, False, True, 0)
            self.container_box.pack_start(self.type_label, False, True, 10)
            self.container_box.pack_start(self.location_label, False, True, 10)
            # Action buttons
            button_list = Gtk.Button.new_from_icon_name('dialog-information', 1)
            button_mvup = Gtk.Button.new_from_icon_name('go-up', 1)
            button_mvdn = Gtk.Button.new_from_icon_name('go-down', 1)
            button_remove = Gtk.Button.new_from_icon_name('edit-delete', 1)
            self.container_box.pack_end(button_remove, False, False, 0)
            self.container_box.pack_end(button_mvdn, False, False, 0)
            self.container_box.pack_end(button_mvup, False, False, 0)
            self.container_box.pack_end(button_list, False, False, 0)


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
    if PLOT_FILE.path == None:
        window = SplashWindow()
    else:
        window = MainWindow()
    window.connect('delete-event', DEBUG__shutdown_WITH_SAVE____)
    window.show_all()
    Gtk.main()

    
def DEBUG__shutdown_WITH_SAVE____(a, b):
    print(a)
    print(b)
    Gtk.main_quit()
    PLOT_FILE.save()


if __name__ == 'pylux_root':
    main()
