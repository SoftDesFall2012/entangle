# Helen Wang Software Design Fall 2012

from Tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=N+S+E+W)
        self.createWidgets()

    def createWidgets(self):
        # Makes window stretchable
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Makes 'Create variable' button
        self.createVariable = Button(self, text='Create variable')
        self.createVariable.grid(column=0, row=0, sticky=N+S+E+W)

        # Makes 'Link values' button
        self.linkValues = Button(self, text='Link values')
        self.linkValues.grid(column=0, row=1, sticky=N+E+S+W)

        # Makes scrollbar
        self.yScroll = Scrollbar(self, orient=VERTICAL)
        self.yScroll.grid(row=0, rowspan=2, column=2, sticky=N+S)

        # Makes text widget
        self.text = Text(self, width=100, height=10, yscrollcommand=self.yScroll.set)
        self.text.grid(column=1, row=0, rowspan=2, sticky=N+E+S+W)
        self.yScroll["command"] = self.text.yview # scroll vertically

app = Application()
app.master.title('Entangle')
app.mainloop()
