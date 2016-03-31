#!/usr/bin/env python3

from TestFrameFactory import ClusterFactory
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class TestFrameManagerMain(Gtk.Window):
    def __init__(self):
        super().__init__()

        self.gladefile = "app.glade"  # store the file name
        self.builder = Gtk.Builder()  # create an instance of the gtk.Builder
        self.builder.add_from_file(self.gladefile)  # add the xml file to the Builder

        # This line does the magic of connecting the signals created in the Glade3
        # builder to our defines above. You must have one def for each signal if
        # you use this line to connect the signals.
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("applicationwindow1")  # This gets the 'window1' object
        self.window.show()  # this shows the 'window1' object

    def on_applicationwindow1_destroy(self, object, data=None):
        print("quit with cancel")
        Gtk.main_quit()

        # This is the same as above but for our menu item.

    def on_gtk_quit_activate(self, menuitem, data=None):
        print("quit from menu")
        Gtk.main_quit()

    def on_file_open_activate(self, menuitem, data=None):
        self.fcd = Gtk.FileChooserDialog("Open...",
                                         self,
                                         Gtk.FileChooserAction.OPEN,
                                         (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.response = self.fcd.run()
        fn = None
        if self.response == Gtk.ResponseType.OK:
            fn = self.fcd.get_filename()
            print("Selected filepath: %s" % self.fcd.get_filename())
            self.fcd.destroy()

        cluster = ClusterFactory().get_from_ods_spreadsheet(fn)

        print("Cluster %s. ID: %s" % (cluster.name, cluster.id))


if __name__ == '__main__':
    main = TestFrameManagerMain()
    Gtk.main()
