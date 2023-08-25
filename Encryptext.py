"""
Imports
"""
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from cryptography.fernet import Fernet


"""
Window Settings
"""
# Create the window
root = Tk("Encryptext")

# Rename the window
root.title("Encryptext")
# Resize the window (manually resizable too)
root.geometry("800x500")


"""
Variables
"""
save_location = ""
font_size = 11
font_type = "Arial"
max_font_size = 400
min_font_size = 6
# Uses a zero width character to determine where it starts and stops
format_string = "​"
supported_file_types = [("Encryptext Files", "*.etx"),
                        ("Text Document", "*.txt"),
                        ("Python Files", "*.py"),
                        ("HTML Files", "*.html"),
                        ("CSS Files", "*.css"),
                        ("Markdown Files", "*.md"),
                        ("All Files", "*.*")
                        ]
encrypt_key = b'bZ3NDhpMPq_X1I_C3TFmOqEQ9uwSisk12pjCuN5u90E='
fernet = Fernet(encrypt_key)

"""
Functions
"""
def open_file(Event=None):
    # Make save_location global to change it for the whole program
    global save_location
    # Show a file selector and let user choose file
    save_location = filedialog.askopenfilename(title="Select file", filetypes=supported_file_types)

    if save_location != "":
        # Get the file exntension
        file_extension = save_location.split(".")[-1]
        # Get file name
        file_name = save_location.split("/")[-1]

        # Set the title of the window to the file name
        title.set(file_name)

        # Open the file and read its contents into an array
        file = open(save_location, "r")

        # If the file is a .etx file, decrypt it
        if file_extension == "etx":
            try:
                file = fernet.decrypt(file).decode()
            except Exception as e:
                messagebox.showerror("Error Opening File", "Access denied.\nUse the Encryptext file that you used to write this file to open it correctly.")

        # Set the textbox to be writable
        textbox.config(state=NORMAL)

        # Clear the textbox
        textbox.delete("1.0", END)

        # Write the file contents to the textbox
        textbox.insert(END, file.read())

        # Close the file
        file.close()

def new_file(Event=None):
    if len(textbox.get("1.0", END)) != 1:
        new_file_confirm = messagebox.askyesno("New File","Create new file?\n\nAny unsaved changes will be lost.")
        if new_file_confirm == True:
            save_location = ""
            textbox.config(state=NORMAL)
            textbox.delete("1.0", END)
            title.set("Untitled")
        else:
            pass
    else:
        save_location = ""
        textbox.config(state=NORMAL)
        textbox.delete("1.0", END)
        title.set("Untitled")

def save_file(Event=None):
    global textbox

def save_as(Event=None):
    print("Ran save as")

def undo(Event=None):
    print("Ran undo")

def redo(Event=None):
    print("Ran redo")

def cut(Event=None):
    textbox.event_generate("<<Cut>>")

def copy(Event=None):
    textbox.event_generate("<<Copy>>")

def paste(Event=None):
    textbox.event_generate("<<Paste>>")


"""
Menu Bar
"""
menubar = Menu(root, tearoff=0)

# Menu items
filemenu = Menu(menubar, tearoff=0)
editmenu = Menu(menubar, tearoff=0)
formatmenu = Menu(menubar, tearoff=0)
textfontmenu = Menu(formatmenu, tearoff=0)
textsizemenu = Menu(formatmenu, tearoff=0)
textstylemenu = Menu(formatmenu, tearoff=0)
helpmenu = Menu(menubar, tearoff=0)

# File menu items
filemenu.add_command(label="New File", accelerator="Ctrl+N", command=new_file)
root.bind_all("<Control-n>", new_file)

filemenu.add_command(label="Open File", accelerator="Ctrl+O", command=open_file)
root.bind_all("<Control-o>", open_file)

# filemenu.add_command(label="View File", command=view_file)

filemenu.add_separator()

filemenu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
root.bind_all("<Control-s>", save_file)

filemenu.add_command(label="Save As", accelerator="Alt+S", command=save_as)
root.bind_all("<Alt-s>", save_as)

filemenu.add_separator()

# filemenu.add_command(label="Edit Mode",  accelerator="Alt+E", command=edit_mode)
# root.bind_all("<Alt-e>", edit_mode)

# filemenu.add_command(label="View Mode", accelerator="Alt+V", command=view_mode)
# root.bind_all("<Alt-v>", view_mode)

filemenu.add_separator()

# filemenu.add_command(label="Exit", accelerator="Ctrl+W", command=quit_app)
# root.bind_all("<Control-w>", quit_app)

# Edit menu items
editmenu.add_command(label="Undo", accelerator="Ctrl+Z", command=undo)
root.bind_all("<Control-z>", undo)

editmenu.add_command(label="Redo", accelerator="Ctrl+Y", command=redo)
root.bind_all("<Control-y>", redo)

editmenu.add_separator()

editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=cut)

editmenu.add_command(label="Copy",  accelerator="Ctrl+C", command=copy)

editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=paste)

editmenu.add_separator()

# editmenu.add_command(label="Select All", accelerator="Ctrl+A", command=select_all)

# editmenu.add_command(label="Deselect All", accelerator="Alt+A", command=deselect_all)
# root.bind_all("<Alt-a>", deselect_all)

editmenu.add_separator()

# editmenu.add_command(label="Edit Preferences")

# Format menu items
# textfontmenu.add_command(label="Arial")

# textsizemenu.add_command(label="3")

# textsizemenu.add_command(label="Increase Font Size", accelerator="Alt+.", command=increase_font)
# root.bind_all("<Alt-.>", increase_font)

# textsizemenu.add_command(label="Decrease Font Size", accelerator="Alt+,", command=decrease_font)
# root.bind_all("<Alt-,>", decrease_font)

# formatmenu.add_command(label="Text Colour", command=change_text_colour)

# textstylemenu.add_command(label="Normal", command=normal_text_style)

# textstylemenu.add_command(label="Bold", accelerator= "Ctrl+B", command=bold_text_style)
# root.bind_all("<Control-b>", bold_text_style)

# textstylemenu.add_command(label="Italic", command=italic_text_style)

# helpmenu.add_command(label="About Encryptext", command=about_menu)

# helpmenu.add_command(label="Documentation", command=documentation)

# Add to menubar
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit", menu=editmenu)

formatmenu.add_cascade(label="Font", menu=textfontmenu)
formatmenu.add_cascade(label="Text Size", menu=textsizemenu)
formatmenu.add_cascade(label="Text Style", menu=textstylemenu)

menubar.add_cascade(label="Format", menu=formatmenu)
menubar.add_cascade(label="Help", menu=helpmenu)

# Display the menu bar
root.config(menu=menubar)


"""
Window Items
"""
title = StringVar()
title.set("Untitled")
title_of_file = Label(textvariable=title, font=("Arial", 15, "bold"), anchor='center')
title_of_file.pack(side=TOP, fill=X)

textbox = Text(root, state=NORMAL, font=(font_type, font_size, "normal"))

scroll_bar_vertical = Scrollbar(root, orient=VERTICAL)
scroll_bar_vertical.pack(side=RIGHT, fill=Y)
scroll_bar_vertical.config(command=textbox.yview)

textbox.config(yscrollcommand=scroll_bar_vertical.set)
textbox.pack(side=BOTTOM, fill=BOTH, expand=1)


"""
Window Display
"""
# When closing the app, run the quit_app function
# root.protocol("WM_DELETE_WINDOW", quit_app)

# Run the window (display it)
root.mainloop()