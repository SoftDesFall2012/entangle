# Helen Wang Software Design Fall 2012

from Tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=N+S+E+W)
        self.createWidgets()

    def printText(self):
        # Prints input text
        t = str(self.text.get('1.0', 'end'))
        print t
        print type(t)

    def saveText(self):
        # Saves input text in a .txt file
        fout = open("text_save.txt", "w")
        try:
            savedText = str(self.text.get('1.0', 'end'))
            fout.write(savedText)
        finally:
            fout.close()

    def boldText(self):
        # Bolds highlighted text
#        self.text.tag_add("bt", "sel.first", "sel.last")
#        self.text.tag_config("bt", font="bold")

         # toggle the bold state based on the first character
        # in the selected range. If bold, unbold it. If not
        # bold, bold it.
        current_tags = self.text.tag_names("sel.first")
        if "bold" in current_tags:
            # first char is bold, so unbold the range
            self.text.tag_remove("bold", "sel.first", "sel.last")
        else:
            # first char is normal, so bold the whole selection
            self.text.tag_add("bold", "sel.first", "sel.last") # (tagname, index1, index2)

    def appendText(self):
        # Inserts text at end of highlighted text
        self.text.insert("sel.last", "end")

    def popWindow(self):
        # Creates popup window
        win = Toplevel()
        win.frame()
        win.config(bg="grey")

    def createWidgets(self):
        # Makes window stretchable; parameters must be adjusted when buttons are added
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Makes 'Create variable' button
        self.createVariable = Button(self, text='Create variable', command=self.popWindow)
        self.createVariable.grid(column=0, row=0, sticky=N+E+S+W)

        # Makes 'Link values' button
        self.linkValues = Button(self, text='Link values')
        self.linkValues.grid(column=0, row=1, sticky=N+E+S+W)

        # Makes 'Save' button
        self.save = Button(self, text='Save', command=self.saveText)
        self.save.grid(column=0, row=2, sticky=N+E+S+W)

        # Makes scrollbar
        self.yScroll = Scrollbar(self, orient=VERTICAL)
        self.yScroll.grid(row=0, rowspan=3, column=2, sticky=N+S)

        # Makes text widget
        self.text = Text(self, width=100, height=10, yscrollcommand=self.yScroll.set)
        self.text.grid(column=1, row=0, rowspan=3, sticky=N+E+S+W)
        self.yScroll["command"] = self.text.yview # scroll vertically

app = Application()
app.master.title('Entangle')
app.mainloop()
