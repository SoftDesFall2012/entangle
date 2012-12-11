__author__ = 'jpark3' # acquired from entangle: 12/9

#-------Text Editor Using GTK------------

import pygtk
pygtk.require('2.0')
import sys, os, errno
import gtk
import pango

#   -----define global values-----------
t=[] # create variable lists
t_child=[]
linked_parent=[]
sign=[] #sign for selecting functions


def make_menu_item(name, callback, data=None):
    item = gtk.MenuItem(name)
    item.connect("activate", callback, data)
    item.show()
    return item


class Buffer(gtk.TextBuffer):
    def __init__(self):
        gtk.TextBuffer.__init__(self)
        tt = self.get_tag_table()

        self.parent=[]
        # A list to hold our active tags
        self.tags_on = []
        # Our Bold tag.
        self.tag_bold = self.create_tag("bold", weight=pango.WEIGHT_BOLD)

    def save_parent(self, parent_list):
        global t
        t.append(parent_list)
        print t
        return t
    def save_child(self, child_list):
        global t_child
        t_child.append(child_list)
        print t_child
        return t_child

    def do_save_buffer(self):
        fout = open("text_save.txt", "w")
        global t

        try:
            startiter = self.get_start_iter()
            enditer = self.get_end_iter()
            savedText = str(self.get_text(startiter, enditer))
            savedText = savedText + '\n' + str(t) + '\n'+ str(t_child)
            fout.write(savedText)
        finally:
            fout.close()


class TextEditor:

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self, buffer = None):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.close_application)
        self.window.set_title("Entangle")

        self.window.set_size_request(500, 500)

        self.menu_items = (
            ( "/_File",         None,         None, 0, "<Branch>" ),
            ( "/File/_New",     "<control>N", self.do_new, 0, None ),
            ( "/File/_Open",    "<control>O", None, 0, None ),
            ( "/File/_Save",    "<control>S", self.do_save, 0, None ),
            ( "/File/Save _As", None,         None, 0, None ),
            ( "/File/sep1",     None,         None, 0, "<Separator>" ),
            ( "/File/Quit",     "<control>Q", gtk.main_quit, 0, None ),
            ( "/_Functions",      None,         None, 0, "<Branch>" ),
            ( "/Functions/Create Variable", "<control><shift>N", self.do_create_variable, 0, None ),
            ( "/Functions/Link",  "<control><shift>L", self.do_link_variable, 0, None ),
            ( "/_Run",      None,         None, 0, "<Branch>" ),
            ( "/Run/Compile", "<control><shift>F10", None, 0, None ),
            ( "/_Help",         None,         None, 0, "<LastBranch>" ),
            ( "/_Help/About",   None,         None, 0, None ),
            )

        buffer = Buffer()

        # main window
        main_vbox = gtk.VBox(False, 1)
        main_vbox.set_border_width(1)
        self.window.add(main_vbox)
        main_vbox.show()

        menubar = self.get_main_menu(self.window)

        main_vbox.pack_start(menubar, False, True, 0)
        menubar.show()

        # main area of interaction (text input + sidebar)
        box1 = gtk.HBox(False, 10) #expand =False
        main_vbox.pack_start(box1, True,True,0)
        box1.show()

        # box for button toolbar
        box3 = gtk.VBox(False, 10)

        frame1 = gtk.Frame("Tools")
        box3.pack_start(frame1, False, False, 20)
        frame1.show()

        frame2 = gtk.Frame("History")
        box3.pack_start(frame2, False, False, 20)
        frame2.show()

        box1.pack_start(box3, False, True, 0)
        box3.show()

        # create toolbox
        toolbox = gtk.VBox(False, 10)
        toolbox.set_border_width(10)

        # add toolbox to frame
        frame1.add(toolbox)
        toolbox.show()

        # create history
        history = gtk.TextView() # something to display history?
        frame2.add(history)
        history.show()

        # box for text input
        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0) # (child, expand, fill, padding)
        box2.show()

        # scrolled window with place for text input
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview = gtk.TextView(buffer)
        sw.add(self.textview)
        sw.show()
        self.textview.show()

        box2.pack_start(sw, True, True, 0)

        # connect delete_event signal to main window
        self.window.connect("delete_event", self.delete_event)

        # set window border
        self.window.set_border_width(10)

        # insert Create Variable button
        self.button1 = gtk.Button('Create Variable')
        self.button1.connect("clicked", self.do_create_variable)
        toolbox.pack_start(self.button1, True, True, 0)
        self.button1.show()

        # insert Link Values button
        self.button2 = gtk.Button('Link Values')
        self.button2.connect("clicked", self.do_link_variable)
        toolbox.pack_start(self.button2, True, True, 0)
        self.button2.show()

        box1.show()
        self.window.show()

    def do_save(self,callback_action, widget):
        buffer = self.textview.get_buffer()
        buffer.do_save_buffer()

    def close_application(self, widget):
        gtk.main_quit()

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

    def callback(self, widget, data=None):
        global linked_parent

        if widget.get_active():
            if data not in linked_parent:
                linked_parent.append(data)

        else:
            if data in linked_parent:
                linked_parent.remove(data)


    def cb_pos_menu_select(self, item, val):
        # Set the value position on both scale widgets
        global sign
        del sign[0]
        sign.append(val)


    def do_link_variable(self, callback_action, widget):
        global linked_parent
        global sign
        #refreshing global memory
        linked_parent=[]
        sign=[]
        sign.append('+')
        buffer = self.textview.get_buffer()
        start, end = buffer.get_selection_bounds()
        text = start.get_slice(end)

        #----Open up Tree View History-----
        TreeView()

        # -----Create GUI for Link Variable-----

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        # Set the window title
        self.window.set_title("Link Variable - Entangle")
        # Set a handler for delete_event that immediately
        # exits GTK.
        self.window.connect("delete_event", self.close_application)
        # Sets the border width of the window.
        self.window.set_size_request(200,400)
        # Create a vertical box
        vbox = gtk.VBox(True, 2)
        # Put the vbox in the main window
        self.window.add(vbox)
        frame = gtk.Frame("Parent Variables")
        frame.set_size_request(100,200)
        vbox.pack_start(frame, False, False, 20)

        vbox_sub = gtk.VBox(False, 0)
        vbox_sub.set_size_request(100,200)
        frame.add(vbox_sub)

        label = gtk.Label("Select One Variable to Link")
        vbox_sub.pack_start(label, False, False, 10)
        label.show()

        global t
        for list in t:
            # Create button
            button = gtk.CheckButton("%s" %list[1])

            # When the button is toggled, we call the "callback" method
            # with a pointer to "button" as its argument
            button.connect("toggled", self.callback, "%s" %list[1])
            # Insert button
            vbox_sub.pack_start(button, False, False, 0)
            button.show()




        # --------- Create Option Menu ------------
        frame = gtk.Frame("Functions")
        frame.set_size_request(100,100)
        vbox.pack_start(frame, True, True, 20)

        vbox_sub = gtk.VBox(False, 0)
        vbox_sub.set_size_request(50,100)
        frame.add(vbox_sub)

        label = gtk.Label("Choose a function")
        vbox_sub.pack_start(label, False, False, 10)
        label.show()

        opt = gtk.OptionMenu()
        menu = gtk.Menu()

        item = make_menu_item ("ADD (x+y)", self.cb_pos_menu_select, '+')
        menu.append(item)

        item = make_menu_item ("SUBTRACT (x-y)", self.cb_pos_menu_select,'-')
        menu.append(item)

        item = make_menu_item ("MULTIPLY (x*y)", self.cb_pos_menu_select, '*')
        menu.append(item)

        item = make_menu_item ("DIVIDE (x/y) ", self.cb_pos_menu_select, '/')
        menu.append(item)

        opt.set_menu(menu)
        vbox_sub.pack_start(opt, False, False, 0)
        opt.show()

        label = gtk.Label("Insert Y Value")
        vbox_sub.pack_start(label, False, False, 10)

        adj = gtk.Adjustment(0.0, 0.0, 1000.0, 1.0, 5.0, 0.0)
        spinner1 = gtk.SpinButton(adj, 0, 0)
        spinner1.set_wrap(True)
        vbox_sub.pack_start(spinner1, False, True, 0)

        buttonOK=gtk.Button("OK")
        buttonOK.connect("clicked", self.save_to_buffer_link, text, linked_parent, sign, spinner1, start, end)
        #buttonOK.connect("clicked", self.destroy())

        vbox_sub.pack_start(buttonOK, False, False, 20)

        self.window.show_all()

    def save_to_buffer_link(self,widget, child, parent,funct, spin, start, end):
        link_data=[]
        buffer = self.textview.get_buffer()
        y_val=spin.get_value_as_int()
        link_data.append('lv')
        link_data.append(child)
        for i in parent:
            link_data.append(i)

        link_data.append(funct[0])
        link_data.append(y_val)
        link_data.append(start)
        link_data.append(end)
        buffer.save_child(link_data)

    def save_to_buffer(self, widget, parent, spin, spin2, start, end):
        t=[]
        buffer = self.textview.get_buffer()
        min=spin.get_value_as_int()
        max=spin2.get_value_as_int()
        t.append('cv')
        t.append(parent)
        t.append(min)
        t.append(max)
        t.append(start)
        t.append(end)
        buffer.save_parent(t)
        #t=[parent, min, max, start, end]

    def do_create_variable(self, callback_action, widget):

        new_window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        new_window.set_size_request(230,150)
        new_window.set_title("Create Variable")

        buffer = self.textview.get_buffer()
        start, end = buffer.get_selection_bounds()
        text = start.get_slice(end)

        main_vbox = gtk.VBox(False, 5)
        main_vbox.set_border_width(10)
        new_window.add(main_vbox)

        frame = gtk.Frame("%s" % text)
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
        spinner1 = gtk.SpinButton(adj, 0, 0)
        spinner1.set_wrap(True)
        vbox2.pack_start(spinner1, False, True, 0)

        vbox2 = gtk.VBox(False, 0)
        hbox.pack_start(vbox2, True, True, 5)

        label = gtk.Label("Max :")
        label.set_alignment(0, 0.5)
        vbox2.pack_start(label, False, True, 0)

        adj = gtk.Adjustment(0.0, 0.0, 1000.0, 1.0, 5.0, 0.0)
        spinner2 = gtk.SpinButton(adj, 0, 0)
        spinner2.set_wrap(True)

        vbox2.pack_start(spinner2, False, True, 0)

        val_label = gtk.Label("")
        val_label2= gtk.Label("")
        hbox = gtk.HBox(False, 0)
        main_vbox.pack_start(hbox, False, True, 0)

        button = gtk.Button("OK")

        button.connect("clicked", self.save_to_buffer, text, spinner1, spinner2,
            start, end )


        hbox.pack_start(button, True, True, 5)

        button = gtk.Button("Close")
        button.connect("clicked", self.close_application)
        hbox.pack_start(button, True, True, 5)

        new_window.show_all()

# View Histror for Parent & Child Variable
class TreeView:

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

        global t
        # we'll add some data now - 4 rows with 3 child rows each

        for parent in t:
            piter = self.treestore.append(None, ['parent variable : %s' % parent[1]])

            for child in range(3):
                self.treestore.append(piter, ['child %i of parent vairable : %s' %
                                              (child, parent[1])])

        # create the TreeView using treestore
        self.treeview = gtk.TreeView(self.treestore)

        # create the TreeViewColumn to display the data
        self.tvcolumn = gtk.TreeViewColumn('History')

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


