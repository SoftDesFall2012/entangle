__author__ = 'Nathan'

from Tkinter import *

root = Tk()
root.title("Tkinter test")

text = Text()
text1 = Text()

text1.config(width=15, height=1)
text1.pack()

def button1():
    text.insert(END, text1)

b = Button(root, text="Enter", width=10, height=2, command=button1)
b.pack()

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
text.config(width=60, height=15)
text.pack(side=LEFT, fill=Y)
scrollbar.config(command=text.yview)
text.config(yscrollcommand=scrollbar.set)

root.mainloop()