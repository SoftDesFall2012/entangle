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
bold=[]
italic=[]
underline=[]
box3 = gtk.VBox(False, 10)

def make_menu_item(name, callback, data=None):
    item = gtk.MenuItem(name)
    item.connect("activate", callback, data)
    item.show()
    return item

'''
class Buffer(gtk.TextBuffer):
    def __init__(self):
        gtk.TextBuffer.__init__(self)


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
            savedText = savedText + '|' + str(t) + '|'+ str(t_child)
            fout.write(savedText)

        finally:
            fout.close()
'''

class TextEditor:

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self, buffer = None):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.close_application)
        self.window.set_title("Entangle")

        self.window.set_size_request(600, 700)

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

        #buffer = Buffer()
        self.font = None
        self.font_dialog = None
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

        global box3

        # box for button toolbar
        box3 = gtk.VBox(False, 10)

        frame0=gtk.Frame("Font")
        box3.pack_start(frame0,False,False,20)
        frame0.show()
        #Boolean=1
        fontbutton = gtk.Button("Font")
        fontbutton.connect("clicked", self.select_font)
        vbox = gtk.VBox(False, 5)
        frame0.add(vbox)

        # Fonts
        texttagtable = gtk.TextTagTable()
        self.buffer = gtk.TextBuffer(texttagtable)

        button_bold = gtk.Button("Bold", gtk.STOCK_BOLD)
        button_italic = gtk.Button("Italic", gtk.STOCK_ITALIC)
        button_underline = gtk.Button("Underline", gtk.STOCK_UNDERLINE)

        self.texttag_bold = gtk.TextTag("bold")
        self.texttag_bold.set_property("weight", pango.WEIGHT_BOLD)
        texttagtable.add(self.texttag_bold)
        self.texttag_italic = gtk.TextTag("italic")
        self.texttag_italic.set_property("style", pango.STYLE_ITALIC)
        texttagtable.add(self.texttag_italic)
        self.texttag_underline = gtk.TextTag("underline")
        self.texttag_underline.set_property("underline", pango.UNDERLINE_SINGLE)
        texttagtable.add(self.texttag_underline)

        # change color for variables
        self.texttag_color = gtk.TextTag("foreground")
        self.texttag_color.set_property("foreground", pango.Color('#00CED1'))
        texttagtable.add(self.texttag_color)

        vbox.pack_start(fontbutton)
        vbox.pack_start(button_bold)
        vbox.pack_start(button_italic)
        vbox.pack_start(button_underline)

        #fontbutton.show()

        button_bold.connect("clicked", self.bold_text)
        button_italic.connect("clicked", self.italic_text)
        button_underline.connect("clicked", self.underline_text)

        frame0.show_all()

        #box3.set_size_request(100,300)
        frame1 = gtk.Frame("Tools")
        box3.pack_start(frame1, False, False, 20)
        frame1.show()

        box1.pack_start(box3, False, True, 0)
        box3.show()

        # create toolbox
        toolbox = gtk.VBox(False, 10)
        toolbox.set_border_width(10)

        # add toolbox to frame
        frame1.add(toolbox)
        toolbox.show()

        # create history
        #history = gtk.TextView() # something to display history?

        # box for text input
        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0) # (child, expand, fill, padding)
        box2.show()

        # scrolled window with place for text input
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview = gtk.TextView(self.buffer)
        self.textview.set_wrap_mode(gtk.WRAP_WORD)

        sw.add(self.textview)
        sw.show()
        self.textview.show()

        box2.pack_start(sw, True, True, 20)

        # connect delete_event signal to main window
        self.window.connect("delete_event", self.delete_event)

        # set window border
        self.window.set_border_width(5)



        # insert Create Variable button
        self.button1 = gtk.Button('Create Variable')
        self.button1.connect("clicked", self.do_create_variable, None)
        toolbox.pack_start(self.button1, True, True, 0)
        self.button1.show()

        # insert Link Values button
        self.button2 = gtk.Button('Link Values')
        self.button2.connect("clicked", self.do_link_variable, None)
        toolbox.pack_start(self.button2, True, True, 0)
        self.button2.show()

        box1.show()
        self.window.show()

    def font_dialog_destroyed(self, data=None):
        self.font_dialog = None

    def font_selection_ok(self, button):
        self.font = self.font_dialog.get_font_name()

        if self.window:
            font_desc = pango.FontDescription(self.font)
            if font_desc:
                self.textview.modify_font(font_desc)

    def select_font(self, button):
        if not self.font_dialog:
            window = gtk.FontSelectionDialog("Font Selection Dialog")
            self.font_dialog = window

            window.set_position(gtk.WIN_POS_MOUSE)

            window.connect("destroy", self.font_dialog_destroyed)

            window.ok_button.connect("clicked",
                self.font_selection_ok)
            window.cancel_button.connect_object("clicked",
                lambda wid: wid.destroy(),
                self.font_dialog)
        window = self.font_dialog
        if not (window.flags() & gtk.VISIBLE):
            window.show()
        else:
            window.destroy()
            self.font_dialog = None


    def bold_text(self, widget):
        bold_child=[]
        if self.buffer.get_selection_bounds() != ():
            start, end = self.buffer.get_selection_bounds()
            self.buffer.apply_tag(self.texttag_bold, start, end)
            text = start.get_slice(end)
            bold_child.append('bold')
            bold_child.append(text)
            bold_child.append(start)
            bold_child.append(end)
            self.save_bold_child(bold_child)


    def italic_text(self, widget):
        italic_child=[]
        if self.buffer.get_selection_bounds() != ():
            start, end = self.buffer.get_selection_bounds()
            self.buffer.apply_tag(self.texttag_italic, start, end)
            text = start.get_slice(end)
            italic_child.append('italic')
            italic_child.append(text)
            italic_child.append(start)
            italic_child.append(end)
            self.save_italic_child(italic_child)

    def underline_text(self, widget):
        underline_child=[]
        if self.buffer.get_selection_bounds() != ():
            start, end = self.buffer.get_selection_bounds()
            self.buffer.apply_tag(self.texttag_underline, start, end)
            text = start.get_slice(end)
            underline_child.append('underline')
            underline_child.append(text)
            underline_child.append(start)
            underline_child.append(end)
            self.save_underline_child(underline_child)

    def do_save(self,callback_action, widget):
        self.do_save_buffer()

    def add_tree(self,widget):

        # create a TreeStore with one string column to use as the model
        self.treestore = gtk.TreeStore(str)

        global t

        for parent in t:
            piter = self.treestore.append(None, ['parent variable : %s' % parent[1]])
            for child in t_child:
                if parent[1] == child[2]:
                    self.treestore.append(piter, ['%s' % child[1]])

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

        global box3

        box3.pack_start(self.treeview, False, False, 0)
        #frame2.add(self.treeview)
        self.treeview.show()



    def close_application(self, widget, new_window):
        #new_window.emit("delete-event", gtk.gdk.Event(gtk.gdk.DELETE))
        new_window.destroy()
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
        self.buffer = self.textview.get_buffer()
        start, end = self.buffer.get_selection_bounds()
        self.buffer.apply_tag(self.texttag_color, start, end)
        text = start.get_slice(end)

        # -----Create GUI for Link Variable-----

        new_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        # Set the window title
        new_window.set_title("Link Variable - Entangle")
        # Set a handler for delete_event that immediately
        # exits GTK.
        new_window.connect("delete_event", self.close_application)
        # Sets the border width of the window.
        new_window.set_size_request(200,500)
        # Create a vertical box
        vbox = gtk.VBox(True, 2)
        # Put the vbox in the main window
        new_window.add(vbox)
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
        buttonOK.connect("clicked", self.add_tree)
        buttonOK.connect("clicked", self.close_application,new_window)

        #buttonOK.connect("clicked", self.destroy())

        vbox_sub.pack_start(buttonOK, False, False, 20)

        new_window.show_all()

    def save_to_buffer_link(self,widget, child, parent,funct, spin, start, end):
        link_data=[]

        y_val=spin.get_value_as_int()
        link_data.append('lv')
        link_data.append(child)
        for i in parent:
            link_data.append(i)

        link_data.append(funct[0])
        link_data.append(y_val)
        link_data.append(start)
        link_data.append(end)
        self.save_child(link_data)

    def save_to_buffer(self, widget, parent, spin, spin2, start, end):
        t=[]
        min=spin.get_value_as_int()
        max=spin2.get_value_as_int()
        t.append('cv')
        t.append(parent)
        t.append(min)
        t.append(max)
        t.append(start)
        t.append(end)
        self.save_parent(t)
        #t=[parent, min, max, start, end]

    def do_create_variable(self, callback_action, widget):

        new_window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        new_window.set_size_request(230,150)
        new_window.set_title("Create Variable")

        self.buffer = self.textview.get_buffer()
        start, end = self.buffer.get_selection_bounds()
        self.buffer.apply_tag(self.texttag_color, start, end)
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
        button.connect("clicked", self.close_application,new_window)


        hbox.pack_start(button, True, True, 5)

        button = gtk.Button("Close")
        button.connect("clicked", self.close_application,new_window)
        hbox.pack_start(button, True, True, 5)

        new_window.show_all()

    def do_history(self,widget):
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

    def save_underline_child(self,underline_child):
        global underline
        underline.append(underline_child)

    def save_italic_child(self,italic_child):
        global italic
        italic.append(italic_child)


    def save_bold_child(self,bold_child):
        global bold
        bold.append(bold_child)
        print bold
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
        global italic
        global bold
        global t_child
        global underline

        self.buffer = self.textview.get_buffer()
        try:
            startiter = self.buffer.get_start_iter()
            enditer = self.buffer.get_end_iter()
            savedText = str(self.buffer.get_text(startiter, enditer))
            savedText = savedText + '|' + str(t) + '|'+ str(t_child) + '|' + str(bold) + '|' + str(italic) + '|' + str(underline)
            fout.write(savedText)

        finally:
            fout.close()






def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    TextEditor()
    main()


