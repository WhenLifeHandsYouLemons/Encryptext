"""
Imports
"""
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
from tkinter.ttk import *
import webbrowser
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
# Change the icon
root.iconbitmap("app_icon.ico")

"""
Variables
"""
save_location = ""

font_size = 11
font_type = "Arial"
max_font_size = 96
min_font_size = 8

# Uses a zero width character to determine where formatting starts and stops
format_item_separator = "​" # There's 1 character here
format_separator = "​​" # There's 2 characters here
format_string = "​​​" # There's 3 characters here

supported_file_types = [("Encryptext Files", "*.etx"),
                        ("Text Document", "*.txt"),
                        ("Python Files", "*.py"),
                        ("HTML Files", "*.html"),
                        ("CSS Files", "*.css"),
                        ("Markdown Files", "*.md"),
                        ("All Files", "*.*")
                        ]

# ENCRYPTION KEY HERE
encrypt_key = b''
# ENCRYPTION KEY HERE
fernet = Fernet(encrypt_key)

history = []
# Add atleast 3 versions history
for i in range(3):
    history.append("")
# Set the current history version to 1 (centered)
current_version = 1
max_history = 50

tags = []
tag_no = 0

"""
Functions
"""
def quit_app(Event=None):
    # Check if the textbox is empty
    if len(textbox.get("1.0", END)) != 1:
        quit_confirm = messagebox.askyesno("Quit","Quit Encryptext?\n\nAny unsaved changes will be lost.")
        if quit_confirm == True:
            root.destroy()
    else:
        root.destroy()

def open_file(Event=None, current=False):
    # Make save_location global to change it for the whole program
    global save_location
    global tags

    # Check if the textbox is empty
    if len(textbox.get("1.0", END)) != 1 and current == False:
        new_file_confirm = messagebox.askyesno("Open File","Open a file?\n\nAny unsaved changes will be lost.")
    else:
        new_file_confirm = True

    if new_file_confirm == True:
        # Show a file selector and let user choose file
        if current == False:
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

            # Set the textbox to be writable
            textbox.config(state=NORMAL)

            # Clear the textbox
            textbox.delete("1.0", END)

            # If the file is a .etx file, decrypt it
            if file_extension == "etx":
                try:
                    # Convert the text to bytes
                    file = bytes(file.read(), "utf-8")
                    # Decrypt the file
                    file = fernet.decrypt(file).decode()
                    # Convert to string and remove the b'' from the string
                    file = str(file)

                    # Look through the text and get all the formatting
                    file = file.split(format_string)
                    formats = file[0].split(format_separator)
                    text = file[1]

                    # Write the file contents to the textbox
                    textbox.insert(END, text[:-1])

                    # Add all the formatting to the text and add it to the tags list
                    if formats[0] != "":
                        for i in range(len(formats)):
                            format = formats[i].split(format_item_separator)

                            textbox.tag_add(format[0], format[1], format[2])

                            if "colour" in format[0]:
                                textbox.tag_config(format[0], foreground=format[3])
                            elif "size" in format[0]:
                                textbox.tag_config(format[0], font=(format[3], int(format[4])))
                            else:
                                # Get format type
                                if "bold" in format[0]:
                                    textbox.tag_config(format[0], font=(format[3], int(format[4]), "bold"))
                                elif "italic" in format[0]:
                                    textbox.tag_config(format[0], font=(format[3], int(format[4]), "italic"))
                                elif "normal" in format[0]:
                                    textbox.tag_config(format[0], font=(format[3], int(format[4]), "normal"))

                            tags.append(formats[i])
                except Exception as e:
                    messagebox.showerror("Error Opening File", "Access denied.\nUse the Encryptext file that you used to write this file to open it correctly.")
            else:
                # Write the file contents to the textbox
                textbox.insert(END, file.read()[:-1])

                # Close the file
                file.close()

def new_file(Event=None):
    global save_location

    # Check if the textbox is empty
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
    # If it's a new file
    if save_location == "":
        save_as()
    else:
        # Get the text from the textbox
        text = textbox.get("1.0", END)

        # Open the file
        file = open(save_location, "w")

        # If the file is a .etx file, encrypt it
        if save_location.split(".")[-1] == "etx":
            full_text = "​​​".join(["​​".join(tags), text])
            text = fernet.encrypt(full_text.encode())

            # Convert the text to a string
            text = str(text)
            # Remove the b'' from the string
            text = text[2:-1]

        # Write the text to the file
        file.write(text)
        # Close the file
        file.close()

def save_as(Event=None):
    global save_location

    # Get the text from the textbox
    text = textbox.get("1.0", END)

    # Show a file selector and let user choose file
    save_location = filedialog.asksaveasfilename(title="Save file as", filetypes=supported_file_types)

    if save_location != "":
        # If the file is a .etx file, encrypt it
        if save_location.split(".")[-1] == "etx":
            full_text = "​​​".join(["​​".join(tags), text])
            text = fernet.encrypt(full_text.encode())

            # Convert the text to a string
            text = str(text)
            # Remove the b'' from the string
            text = text[2:-1]

        # Open the file
        file = open(save_location, "w")

        # Write the text to the file
        file.write(text)
        # Close the file
        file.close()

        # Open the new file
        open_file(current=True)

def undo(Event=None):
    global history

    # Check if the previous version is the same as the current version
    if history[current_version - 1] != textbox.get("1.0", END):
        # Update the current version
        history[current_version] = textbox.get("1.0", END)
        # Remove the last newline character
        history[current_version] = history[current_version][:-1]

        # Check if the final version is blank
        if history[-1] != "":
            if len(history) - current_version < max_history:
                # Add a new version
                history.append("")

        # Shift every version up one
        for i in range(len(history) - 1, 0, -1):
            history[i] = history[i - 1]

        # Clear the first version
        history[0] = ""

        # Update the textbox
        textbox.delete("1.0", END)
        textbox.insert(END, history[current_version])

def redo(Event=None):
    global history
    global current_version

    # Check if the next version is the same as the current version
    if history[current_version + 1] != textbox.get("1.0", END):
        # Update the current version
        history[current_version] = textbox.get("1.0", END)
        # Remove the last newline character
        history[current_version] = history[current_version][:-1]

        # Check if the first version is blank
        if history[0] != "":
            if current_version < max_history:
                # Add a new version
                history.insert(0, "")
                # Update the current version
                current_version += 1

        # Shift every version down one
        for i in range(0, len(history) - 1):
            history[i] = history[i + 1]

        # Clear the last version
        history[-1] = ""

        # Update the textbox
        textbox.delete("1.0", END)
        textbox.insert(END, history[current_version])

def track_changes(Event=None):
    global history
    global current_version

    # Check if the first version is empty
    if history[0] != "":
        if current_version < max_history:
            # Add a new version
            history.insert(0, "")
            # Update the current version
            current_version += 1

    # Shift every version down one
    for i in range(0, len(history) - 1):
        history[i] = history[i + 1]

    # Update the current version
    history[current_version] = textbox.get("1.0", END)
    # Remove the last newline character
    history[current_version] = history[current_version][:-1]

def cut(Event=None):
    textbox.event_generate("<<Cut>>")

def copy(Event=None):
    textbox.event_generate("<<Copy>>")

def paste(Event=None):
    textbox.event_generate("<<Paste>>")

def view_file(Event=None):
    # Open the file
    open_file()

    # Set the textbox to be read-only
    textbox.config(state=DISABLED)

def view_mode(Event=None):
    # Set the textbox to be read-only
    textbox.config(state=DISABLED)

def edit_mode(Event=None):
    # Set the textbox to be writable
    textbox.config(state=NORMAL)

def select_all(Event=None):
    textbox.event_generate("<<SelectAll>>")

def deselect_all(Event=None):
    textbox.event_generate("<<SelectNone>>")

def about_menu(Event=None):
    messagebox.showinfo("About Encryptext", "Encryptext can do what Notepad does, and more. You can edit, format, and encrypt files securely, while also editing regular files with ease.\n\n Free for everyone. Forever. ❤")

def documentation(Event=None):
    webbrowser.open_new("https://github.com/WhenLifeHandsYouLemons/Encryptext")

def bold_text_style(Event=None):
    global tag_no
    # Get the position of current selection
    start_selection = textbox.index("sel.first")
    end_selection = textbox.index("sel.last")

    # Create a tag
    textbox.tag_add(f"bold{tag_no}", start_selection, end_selection)
    textbox.tag_config(f"bold{tag_no}", font=(font_type, font_size, "bold"))
    tags.append("​".join([f"bold{tag_no}", start_selection, end_selection, font_type, str(font_size)]))

    tag_no += 1

def italic_text_style(Event=None):
    global tag_no
    # Get the position of current selection
    start_selection = textbox.index("sel.first")
    end_selection = textbox.index("sel.last")

    # Create a tag
    textbox.tag_add(f"italic{tag_no}", start_selection, end_selection)
    textbox.tag_config(f"italic{tag_no}", font=(font_type, font_size, "italic"))
    tags.append("​".join([f"italic{tag_no}", start_selection, end_selection, font_type, str(font_size)]))

    tag_no += 1

def normal_text_style(Event=None):
    global tag_no
    # Get the position of current selection
    start_selection = textbox.index("sel.first")
    end_selection = textbox.index("sel.last")

    # Create a tag
    textbox.tag_add(f"normal{tag_no}", start_selection, end_selection)
    textbox.tag_config(f"normal{tag_no}", font=(font_type, font_size, "normal"))
    tags.append("​".join([f"normal{tag_no}", start_selection, end_selection, font_type, str(font_size)]))

    tag_no += 1

def text_colour_change(Event=None):
    global tag_no
    colour_code = colorchooser.askcolor(title ="Choose a colour")
    colour_code = colour_code[-1]

    # Get the position of current selection
    start_selection = textbox.index("sel.first")
    end_selection = textbox.index("sel.last")

    # Create a tag
    textbox.tag_add(f"colour{tag_no}", start_selection, end_selection)
    textbox.tag_config(f"colour{tag_no}", foreground=colour_code)

    # Check if there are any old tags with the same selection and format type
    for i in range(len(tags)):
        tag = tags[i].split("​")
        if tag[1] == start_selection and tag[2] == end_selection and tag[3] == colour_code and tag[4] == font_type and tag[0].startswith("colour"):
            # Remove the old tag
            textbox.tag_delete(tag[0])
            # Remove the old tag from the list
            tags.pop(i)

    tags.append("​".join([f"colour{tag_no}", start_selection, end_selection, colour_code, font_type, str(font_size)]))

    tag_no += 1

def increase_font(Event=None):
    global tag_no
    global font_size
    if font_size == max_font_size:
        messagebox.showerror("Error", "Font size cannot go higher than 96.")
    else:
        font_size += 1
        size = font_size
        start_selection = textbox.index("sel.first")
        end_selection = textbox.index("sel.last")

        # Create a tag
        textbox.tag_add(f"size{tag_no}", start_selection, end_selection)
        textbox.tag_config(f"size{tag_no}", font=(font_type, size))

        # Check if there are any old tags with the same selection and format type
        for i in range(len(tags)):
            tag = tags[i].split("​")
            if tag[1] == start_selection and tag[2] == end_selection and tag[3] == font_type and tag[0].startswith("size"):
                # Remove the old tag
                textbox.tag_delete(tag[0])
                # Remove the old tag from the list
                tags.pop(i)

        tags.append("​".join([f"size{tag_no}", start_selection, end_selection, font_type, str(size)]))

    tag_no += 1

def decrease_font(Event=None):
    global tag_no
    global font_size
    if font_size == min_font_size:
        messagebox.showerror("Error", "Font size cannot go lower than 8.")
    else:
        font_size -= 1
        size = font_size
        start_selection = textbox.index("sel.first")
        end_selection = textbox.index("sel.last")

        # Create a tag
        textbox.tag_add(f"size{tag_no}", start_selection, end_selection)
        textbox.tag_config(f"size{tag_no}", font=(font_type, size))

        # Check if there are any old tags with the same selection and format type
        for i in range(len(tags)):
            tag = tags[i].split("​")
            if tag[1] == start_selection and tag[2] == end_selection and tag[3] == font_type and tag[0].startswith("size"):
                # Remove the old tag
                textbox.tag_delete(tag[0])
                # Remove the old tag from the list
                tags.pop(i)

        tags.append("​".join([f"size{tag_no}", start_selection, end_selection, font_type, str(size)]))

    tag_no += 1

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

filemenu.add_command(label="View File", command=view_file)

filemenu.add_separator()

filemenu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
root.bind_all("<Control-s>", save_file)

filemenu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=save_as)
root.bind_all("<Control-S>", save_as)

filemenu.add_separator()

filemenu.add_command(label="Edit Mode",  accelerator="Alt+E", command=edit_mode)
root.bind_all("<Alt-e>", edit_mode)

filemenu.add_command(label="View Mode", accelerator="Alt+V", command=view_mode)
root.bind_all("<Alt-v>", view_mode)

filemenu.add_separator()

filemenu.add_command(label="Exit", accelerator="Ctrl+W", command=quit_app)
root.bind_all("<Control-w>", quit_app)

# Edit menu items
editmenu.add_command(label="Undo", accelerator="Ctrl+Z", command=undo)
root.bind_all("<Control-z>", undo)

editmenu.add_command(label="Redo", accelerator="Ctrl+Shift+Z", command=redo)
root.bind_all("<Control-Z>", redo)

editmenu.add_separator()

editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=cut)

editmenu.add_command(label="Copy",  accelerator="Ctrl+C", command=copy)

editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=paste)

editmenu.add_separator()

editmenu.add_command(label="Select All", accelerator="Ctrl+A", command=select_all)

editmenu.add_command(label="Deselect All", accelerator="Ctrl+Shift+A", command=deselect_all)
root.bind_all("<Control-A>", deselect_all)

editmenu.add_separator()

editmenu.add_command(label="Edit Preferences")

# Format menu items
textfontmenu.add_command(label="Arial")

textsizemenu.add_command(label="Increase Font Size", accelerator="Ctrl+Shift+-", command=increase_font)
root.bind_all("<Control-+>", increase_font)

textsizemenu.add_command(label="Decrease Font Size", accelerator="Ctrl+Shift++", command=decrease_font)
root.bind_all("<Control-_>", decrease_font)

formatmenu.add_command(label="Text Colour", accelerator="Alt+C", command=text_colour_change)
root.bind_all("<Alt-c>", text_colour_change)

textstylemenu.add_command(label="Normal", accelerator="Alt+N", command=normal_text_style)
root.bind_all("<Alt-n>", normal_text_style)

textstylemenu.add_command(label="Bold", accelerator= "Alt+B", command=bold_text_style)
root.bind_all("<Alt-b>", bold_text_style)

textstylemenu.add_command(label="Italic", accelerator= "Alt+I", command=italic_text_style)
root.bind_all("<Alt-i>", bold_text_style)

helpmenu.add_command(label="About Encryptext", command=about_menu)

helpmenu.add_command(label="Encryptext on GitHub", command=documentation)

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

root.bind_all("<,>", track_changes)
root.bind_all("<.>", track_changes)
root.bind_all("<?>", track_changes)
root.bind_all("<'>", track_changes)
root.bind_all('<">', track_changes)
root.bind_all("<!>", track_changes)
root.bind_all("<(>", track_changes)
root.bind_all("<)>", track_changes)
root.bind_all("<[>", track_changes)
root.bind_all("<]>", track_changes)
root.bind_all("<{>", track_changes)
root.bind_all("<}>", track_changes)
root.bind_all("</>", track_changes)

"""
Window Items
"""
title = StringVar()
title.set("Untitled")
title_of_file = Label(textvariable=title, font=("Arial", 18, "bold"), anchor='center')
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
root.protocol("WM_DELETE_WINDOW", quit_app)

# Run the window (display it)
root.mainloop()
