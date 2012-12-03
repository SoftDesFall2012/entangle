__author__ = 'jpark3'

#Text Editor Using GTK


import pygtk
pygtk.require('2.0')
import gtk
import pango



class Buffer(gtk.TextBuffer):
    N_COLORS = 16
    PANGO_SCALE = 1024

    def __init__(self):
        gtk.TextBuffer.__init__(self)
        tt = self.get_tag_table()
        self.refcount = 0
        self.filename = None
        self.untitled_serial = -1


class TextEditor:
    def close_application(self, widget):
        gtk.main_quit()

    def print_hello(self, w, data):
        print "Hello, World!"


    def change_digits(self, widget, spin, spin1):
        spin1.set_digits(spin.get_value_as_int())

    def get_value(self, widget, data, spin, spin2, label):
        if data == 1:
            buf = "%d" % spin.get_value_as_int()
        else:
            buf = "%0.*f" % (spin2.get_value_as_int(),
                             spin.get_value())
        label.set_text(buf)

    # This is the ItemFactoryEntry structure used to generate new menus.
    # Item 1: The menu path. The letter after the underscore indicates an
    #         accelerator key once the menu is open.
    # Item 2: The accelerator key for the entry
    # Item 3: The callback.
    # Item 4: The callback action.  This changes the parameters with
    #         which the callback is called.  The default is 0.
    # Item 5: The item type, used to define what kind of an item it is.
    #       Here are the possible values:

    #       NULL               -> "<Item>"
    #       ""                 -> "<Item>"
    #       "<Title>"          -> create a title item
    #       "<Item>"           -> create a simple item
    #       "<CheckItem>"      -> create a check item
    #       "<ToggleItem>"     -> create a toggle item
    #       "<RadioItem>"      -> create a radio item
    #       <path>             -> path of a radio item to link against
    #       "<Separator>"      -> create a separator
    #       "<Branch>"         -> create an item to hold sub items (optional)
    #       "<LastBranch>"     -> create a right justified branch

    def get_main_menu(self, window):
        accel_group = gtk.AccelGroup()

        # This function initializes the item factory.
        # Param 1: The type of menu - can be MenuBar, Menu,
        #          or OptionMenu.
        # Param 2: The path of the menu.
        # Param 3: A reference to an AccelGroup. The item factory sets up
        #          the accelerator table while generating menus.
        item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)

        # This method generates the menu items. Pass to the item factory
        #  the list of menu items
        item_factory.create_items(self.menu_items)

        # Attach the new accelerator group to the window.
        window.add_accel_group(accel_group)

        # need to keep a reference to item_factory to prevent its destruction
        self.item_factory = item_factory
        # Finally, return the actual menu bar created by the item factory.
        return item_factory.get_widget("<main>")

    def do_new(self, callback_action, widget):
        TextEditor()

    def do_link_variable(self, callback_action, widget):
        BasicTreeViewExample()




    def do_create_variable(self, callback_action, widget):
        new_window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        new_window.set_size_request(230,150)
        new_window.set_title("Create Variable")


        main_vbox = gtk.VBox(False, 5)
        main_vbox.set_border_width(10)
        new_window.add(main_vbox)

        frame = gtk.Frame("Parent Variable")
        main_vbox.pack_start(frame, True, True, 0)

        vbox = gtk.VBox(False, 0)
        vbox.set_border_width(5)
        frame.add(vbox)

        hbox = gtk.HBox(False, 0)
        vbox.pack_start(hbox, True, True, 5)

        vbox2 = gtk.VBox(False, 0)
        hbox.pack_start(vbox2, True, True, 5)

        label = gtk.Label("Min :")
        label.set_alignment(0, 0.5)
        vbox2.pack_start(label, False, True, 0)

        adj = gtk.Adjustment(0.0, 0.0, 1000.0, 1.0, 5.0, 0.0)
        spinner = gtk.SpinButton(adj, 0, 0)
        spinner.set_wrap(True)
        vbox2.pack_start(spinner, False, True, 0)

        vbox2 = gtk.VBox(False, 0)
        hbox.pack_start(vbox2, True, True, 5)

        label = gtk.Label("Max :")
        label.set_alignment(0, 0.5)
        vbox2.pack_start(label, False, True, 0)

        adj = gtk.Adjustment(0.0, 0.0, 1000.0, 1.0, 5.0, 0.0)
        spinner = gtk.SpinButton(adj, 0, 0)
        spinner.set_wrap(True)
        vbox2.pack_start(spinner, False, True, 0)

        vbox2 = gtk.VBox(False, 0)
        hbox.pack_start(vbox2, True, True, 5)


        hbox = gtk.HBox(False, 0)
        main_vbox.pack_start(hbox, False, True, 0)

        button = gtk.Button("Close")
        button.connect("clicked", lambda w: gtk.main_quit())

        button1=gtk.Button("OK")
        button1.connect("clicked", lambda w: gtk.main_quit())

        hbox.pack_start(button1, True, True, 5)
        hbox.pack_start(button, True, True, 5)

        new_window.show_all()



    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("destroy", self.close_application)
        window.set_title("ENTANGLE")

        window.set_size_request(500, 500)

        self.menu_items = (
            ( "/_File",         None,         None, 0, "<Branch>" ),
            ( "/File/_New",     "<control>N", self.do_new, 0, None ),
            ( "/File/_Open",    "<control>O", self.print_hello, 0, None ),
            ( "/File/_Save",    "<control>S", self.print_hello, 0, None ),
            ( "/File/Save _As", None,         None, 0, None ),
            ( "/File/sep1",     None,         None, 0, "<Separator>" ),
            ( "/File/Quit",     "<control>Q", gtk.main_quit, 0, None ),
            ( "/_Functions",      None,         None, 0, "<Branch>" ),
            ( "/Functions/Create Variable", None, self.do_create_variable, 0, None ),
            ( "/Functions/Link",  None,        self.do_link_variable, 0, None ),
            ( "/_Help",         None,         None, 0, "<LastBranch>" ),
            ( "/_Help/About",   None,         None, 0, None ),
            )

        main_vbox = gtk.VBox(False, 1)
        main_vbox.set_border_width(1)
        window.add(main_vbox)
        main_vbox.show()

        menubar = self.get_main_menu(window)

        main_vbox.pack_start(menubar, False, True, 0)
        menubar.show()

        box1 = gtk.VBox(False, 20) #expand =False
        main_vbox.pack_start(box1, True,True,0)
        box1.show()

        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)

        box1.pack_start(box2, True, True, 0) # (child, expand, fill, padding)
        box2.show()

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textview = gtk.TextView()
        sw.add(textview)
        sw.show()
        textview.show()

        box2.pack_start(sw, True, True, 0)

        window.show()


class BasicTreeViewExample:

    # close the window and quit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_title("Variable TreeView")

        self.window.set_size_request(200, 200)

        self.window.connect("delete_event", self.delete_event)

        # create a TreeStore with one string column to use as the model
        self.treestore = gtk.TreeStore(str)

        # we'll add some data now - 4 rows with 3 child rows each
        for parent in range(4):
            piter = self.treestore.append(None, ['parent %i' % parent])
            for child in range(3):
                self.treestore.append(piter, ['child %i of parent %i' %
                                              (child, parent)])

        # create the TreeView using treestore
        self.treeview = gtk.TreeView(self.treestore)

        # create the TreeViewColumn to display the data
        self.tvcolumn = gtk.TreeViewColumn('Column 0')

        # add tvcolumn to treeview
        self.treeview.append_column(self.tvcolumn)

        # create a CellRendererText to render the data
        self.cell = gtk.CellRendererText()

        # add the cell to the tvcolumn and allow it to expand
        self.tvcolumn.pack_start(self.cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.tvcolumn.add_attribute(self.cell, 'text', 0)

        # make it searchable
        self.treeview.set_search_column(0)

        # Allow sorting on the column
        self.tvcolumn.set_sort_column_id(0)

        # Allow drag and drop reordering of rows
        self.treeview.set_reorderable(True)

        self.window.add(self.treeview)

        self.window.show_all()




def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    TextEditor()
    main()


