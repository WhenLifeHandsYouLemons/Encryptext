from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

# Defining TextEditor Class
class TextEditor:
  # Defining Constructor
  def __init__(self,root):
    # Assigning root
    self.root = root
    # Creating Text Area
    self.txtarea = Text(self.root,font=("times new roman",12,"bold"))
    # Packing Text Area to root window
    self.txtarea.pack(fill=BOTH,expand=1)
# Creating TK Container
root = Tk()
# Passing Root to TextEditor Class
TextEditor(root)
# Root Window Looping
root.mainloop()