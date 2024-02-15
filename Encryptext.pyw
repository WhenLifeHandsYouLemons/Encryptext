"""
Imports
"""
import sys
from os.path import abspath, join
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
import traceback    # For the error messages when in exe form
import webbrowser   # For opening the help page
from cryptography.fernet import Fernet  # For encryption features
# For Markdown preview features
from tkinterweb import HtmlFrame
import markdown

# Used for getting files when using one-file mode .exe format
def getTrueFilename(filename):
    try:
        base = sys._MEIPASS
    except Exception:
        base = abspath(".")
    return join(base, filename)

"""
Window Settings
"""
# Create the window
root = tk.Tk("Encryptext")

def previewWindowCreation(hidden=False, add_frame=True):
    global md_preview_window, frame

    md_preview_window = tk.Tk("Preview")
    if hidden:
        md_preview_window.withdraw()
    md_preview_window.title("Preview")
    md_preview_window.geometry("800x500")
    md_preview_window.iconbitmap(getTrueFilename("app_icon.ico"))

    if add_frame:
        frame = HtmlFrame(md_preview_window, messages_enabled=False)
        frame.load_html(markdown.markdown(textbox.get("1.0", tk.END)))
        frame.pack(fill="both", expand=True)
        md_preview_window.bind_all("<Control-e>", updatePreview)
        md_preview_window.bind_all("<Alt-P>", closePreview)

# Rename the window
root.title("Encryptext")
# Resize the window (manually resizable too)
root.geometry("800x500")
# Change the icon
root.iconbitmap(getTrueFilename("app_icon.ico"))

"""
Variables
"""
debug = False

save_location = ""
file_extension = ""

font_size = 11
font_type = "Arial"
max_font_size = 96
min_font_size = 8

# Uses random random-length strings of characters to determine where formatting starts and stops# FORMAT ITEM SEPARATOR HERE
format_item_separator = ''# FORMAT ITEM SEPARATOR HERE# FORMAT SEPARATOR HERE
format_separator = ''# FORMAT SEPARATOR HERE# FORMAT STRING HERE
format_string = ''# FORMAT STRING HERE

supported_file_types = [
    ("Encryptext", "*.etx"),
    ("Plain Text", "*.txt"),
    ("Python", "*.py"),
    ("HTML", "*.html"),
    ("CSS", "*.css"),
    ("JavaScript", "*.js"),
    ("JSON", "*.json"),
    ("Markdown", "*.md"),
    ("Comma-Separated Values", "*.csv"),
    ("Windows Initialization File", "*.ini"),
    ("Log File", "*.log"),
    ("All Files", "*.*"),
]
# ENCRYPTION KEY HERE
encrypt_key = b''# ENCRYPTION KEY HERE

if debug:
    encrypt_key = Fernet.generate_key()
fernet = Fernet(encrypt_key)

# Have atleast 3 versions of history
history = ["", "", ""]
# Set the current history version to 1 (centered)
current_version = 1
max_history = 50

tags = []
tag_no = 0

"""
Functions
"""

def updateTags():
    global tags

    tags_used = textbox.tag_names()
    i = 0
    for tag in tags_used:
        indices = textbox.tag_ranges(tag)
        for start, end in zip(indices[::2], indices[1::2]):
            tags[i][1] = str(start)
            tags[i][2] = str(end)

            i += 1

    formatted_tags = [format_item_separator.join(tag) for tag in tags]
    formatted_tags = format_separator.join(formatted_tags)

    return formatted_tags

def quitApp(Event=None):
    # Check if the textbox is empty
    if len(textbox.get("1.0", tk.END)) != 1:
        quit_confirm = messagebox.askyesno("Quit", "Quit Encryptext?\n\nAny unsaved changes will be lost.")
        if quit_confirm:
            try:
                md_preview_window.destroy()
                pref_window.destroy()
            finally:
                root.destroy()
                sys.exit()
    else:
        try:
            md_preview_window.destroy()
            pref_window.destroy()
        finally:
            root.destroy()
            sys.exit()

def openFile(Event=None, current=False):
    # Make save_location global to change it for the whole program
    global save_location, tags, history, current_version, tag_no, file_extension

    # Reset tag number
    tag_no = 0

    # Check if the textbox is empty
    if len(textbox.get("1.0", tk.END)) != 1 and not current:
        new_file_confirm = messagebox.askyesno("Open File", "Open a file?\n\nAny unsaved changes will be lost.")
    else:
        new_file_confirm = True

    if new_file_confirm:
        # Show a file selector and let user choose file
        if not current:
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
            textbox.config(state=tk.NORMAL)

            # Clear the textbox
            textbox.delete("1.0", tk.END)

            # Clear the history
            history = ["", "", ""]
            current_version = 1

            # If the file is a .etx file, decrypt it
            if file_extension == "etx":
                try:
                    # Convert the text to bytes
                    file = bytes(file.read(), "utf-8")

                    # Convert to string and remove the b'' from the string
                    if not debug:
                        # Decrypt the file
                        file = fernet.decrypt(file).decode()
                    else:
                        file = file.decode()

                    # Split the formatting and the visible text
                    file = file.split(format_string)

                    # Go through the formats and remove duplicates
                    formattings = file[0].split(format_separator)
                    formats = []
                    if formattings != [""]:
                        formattings.reverse()
                        for format_style in formattings:
                            format_style = format_style.split(format_item_separator)
                            add = True

                            if formats == []:
                                format_style[0] = f"{''.join(i for i in format_style[0] if not i.isdigit())}{tag_no}"
                                formats.append(format_style)
                                tag_no += 1
                            else:
                                format_type = "".join(i for i in format_style[0] if not i.isdigit())
                                for f in formats:
                                    if format_type == "".join(i for i in f[0] if not i.isdigit()) and format_style[1] == f[1] and format_style[2] == f[2]:
                                        add = False
                                        break

                                if add:
                                    format_style[0] = f"{''.join(i for i in format_style[0] if not i.isdigit())}{tag_no}"
                                    formats.append(format_style)
                                    tag_no += 1

                        # Need to sort the formats list to have the bold at the end
                        # The bold has to be the last formatting to be applied otherwise it won't show up
                        new_formats = []
                        i = len(formats) - 1
                        while i >= 0:
                            if formats[i][0].startswith("bold"):
                                new_formats.append(formats[i])
                            else:
                                new_formats.insert(0, formats[i])
                            i -= 1

                        formats = new_formats.copy()
                        # Saves memory
                        new_formats.clear()

                    # Format the visible text properly
                    text = file[1]
                    text = text.replace("\\n", "\n")

                    # Write the file contents to the textbox
                    # Removes the extra newline that tkinter adds
                    textbox.insert(tk.END, text[:-1])

                    # Add all the formatting to the text and add it to the tags list
                    if formats != []:
                        for i in range(len(formats)):
                            format = formats[i]

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

                            tags.append(format)
                except Exception as e:
                    if debug:
                        messagebox.showerror("Error Opening File", traceback.format_exc())
                        traceback.print_exc()
                    else:
                        messagebox.showerror("Error Opening File", f"Access denied.\nPlease use the Encryptext program that you used to write this file to open it correctly.")
            else:
                # Write the file contents to the textbox
                textbox.insert(tk.END, file.read()[:-1])

                # Close the file
                file.close()
            if file_extension == "md":
                global md_preview_window
                try:
                    md_preview_window.deiconify()
                    updatePreview()
                except:
                    previewWindowCreation()

def newFile(Event=None):
    global save_location, history, current_version

    # Check if the textbox is empty
    if len(textbox.get("1.0", tk.END)) != 1:
        new_file_confirm = messagebox.askyesno("New File", "Create new file?\n\nAny unsaved changes will be lost.")
        if new_file_confirm:
            save_location = ""
            textbox.config(state=tk.NORMAL)
            textbox.delete("1.0", tk.END)

            history = ["", "", ""]
            current_version = 1

            title.set("Untitled")
        else: pass
    else:
        save_location = ""
        textbox.config(state=tk.NORMAL)
        textbox.delete("1.0", tk.END)

        history = ["", "", ""]
        current_version = 1

        title.set("Untitled")

def saveFile(Event=None):
    # If it's a new file
    if save_location == "":
        saveFileAs()
    else:
        # Get the text from the textbox
        text = textbox.get("1.0", tk.END)

        # If the file is a .etx file, encrypt it
        if save_location.split(".")[-1] == "etx":
            full_text = format_string.join([updateTags(), text])
            if not debug:
                text = fernet.encrypt(full_text.encode())
            else:
                text = full_text.encode()

            # Convert the text to a string
            text = str(text)
            # Remove the b'' from the string
            text = text[2:-1]

        # Write the text to the file and close it
        file = open(save_location, "w")
        file.write(text)
        file.close()

def saveFileAs(Event=None):
    global save_location

    # Get the text from the textbox
    text = textbox.get("1.0", tk.END)

    # Show a file selector and let user choose file
    save_location = filedialog.asksaveasfilename(title="Save file as", filetypes=supported_file_types, defaultextension=supported_file_types)

    if save_location != "":
        # If the file is a .etx file, encrypt it
        if save_location.split(".")[-1] == "etx":
            full_text = format_string.join([updateTags(), text])
            if not debug:
                text = fernet.encrypt(full_text.encode())
            else:
                text = full_text.encode()

            # Convert the text to a string
            text = str(text)
            # Remove the b'' from the string
            text = text[2:-1]

        # Write the text to the file and close it
        file = open(save_location, "w")
        file.write(text)
        file.close()

        # Open the new file
        openFile(current=True)

def undo(Event=None):
    global history

    # Check if the previous version is the same as the current version
    if history[current_version - 1] != textbox.get("1.0", tk.END):
        # Update the current version
        history[current_version] = textbox.get("1.0", tk.END)
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
        textbox.delete("1.0", tk.END)
        textbox.insert(tk.END, history[current_version])

def redo(Event=None):
    global history
    global current_version

    # Check if the next version is the same as the current version
    if history[current_version + 1] != textbox.get("1.0", tk.END):
        # Update the current version
        history[current_version] = textbox.get("1.0", tk.END)
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
        textbox.delete("1.0", tk.END)
        textbox.insert(tk.END, history[current_version])

def updatePreview(Event=None):
    try:
        # Update the preview
        frame.load_html(markdown.markdown(textbox.get("1.0", tk.END)))
    except:
        # Only update it if it's markdown or none
        if file_extension == "md":
            # If the preview window was opened manually
            previewWindowCreation()

def trackChanges(Event=None):
    if Event.keysym in ["space", "Return"]:
        global history, current_version

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
        history[current_version] = textbox.get("1.0", tk.END)
        # Remove the last newline character
        history[current_version] = history[current_version][:-1]

    # Update the preview
    updatePreview()

def cut(Event=None):
    textbox.event_generate("<<Cut>>")

def copy(Event=None):
    textbox.event_generate("<<Copy>>")

def paste(Event=None):
    textbox.event_generate("<<Paste>>")

def viewFile(Event=None):
    # Open the file
    openFile()

    # Set the textbox to be read-only
    textbox.config(state=tk.DISABLED)

def viewingMode(Event=None):
    # Set the textbox to be read-only
    textbox.config(state=tk.DISABLED)

def editingMode(Event=None):
    # Set the textbox to be writable
    textbox.config(state=tk.NORMAL)

def openPreview(Event=None):
    try:
        md_preview_window.deiconify()
    except:
        previewWindowCreation()

def closePreview(Event=None):
    try:
        md_preview_window.withdraw()
    except: pass

def select_all(Event=None):
    textbox.event_generate("<<SelectAll>>")

def deselect_all(Event=None):
    textbox.event_generate("<<SelectNone>>")

def openPreferences():
    global pref_window, frame

    pref_window = tk.Tk("Preferences")
    pref_window.title("Preferences")
    pref_window.geometry("500x600")
    pref_window.iconbitmap(getTrueFilename("app_icon.ico"))
    pref_window.protocol("WM_DELETE_WINDOW", pref_window.destroy)

    pref_window.mainloop()

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
    tags.append([f"bold{tag_no}", start_selection, end_selection, font_type, str(font_size)])

    tag_no += 1

def italic_text_style(Event=None):
    global tag_no
    # Get the position of current selection
    start_selection = textbox.index("sel.first")
    end_selection = textbox.index("sel.last")

    # Create a tag
    textbox.tag_add(f"italic{tag_no}", start_selection, end_selection)
    textbox.tag_config(f"italic{tag_no}", font=(font_type, font_size, "italic"))
    tags.append([f"italic{tag_no}", start_selection, end_selection, font_type, str(font_size)])

    tag_no += 1

def normal_text_style(Event=None):
    global tag_no
    # Get the position of current selection
    start_selection = textbox.index("sel.first")
    end_selection = textbox.index("sel.last")

    # Create a tag
    textbox.tag_add(f"normal{tag_no}", start_selection, end_selection)
    textbox.tag_config(f"normal{tag_no}", font=(font_type, font_size, "normal"))
    tags.append([f"normal{tag_no}", start_selection, end_selection, font_type, str(font_size)])

    tag_no += 1

def text_colour_change(Event=None):
    global tag_no
    colour_code = colorchooser.askcolor(title="Choose a colour")
    colour_code = colour_code[-1]

    # Get the position of current selection
    start_selection = textbox.index("sel.first")
    end_selection = textbox.index("sel.last")

    # Create a tag
    textbox.tag_add(f"colour{tag_no}", start_selection, end_selection)
    textbox.tag_config(f"colour{tag_no}", foreground=colour_code)

    tags.append([f"colour{tag_no}",start_selection,end_selection,colour_code,font_type,str(font_size),])

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

        tags.append([f"size{tag_no}", start_selection, end_selection, font_type, str(size)])

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

        tags.append([f"size{tag_no}", start_selection, end_selection, font_type, str(size)])

    tag_no += 1

"""
Window Items
"""
title = tk.StringVar()
title.set("Untitled")
title_of_file = tk.Label(textvariable=title, font=("Arial", 18, "bold"), anchor="center")
title_of_file.pack(side=tk.TOP, fill=tk.X)

textbox = tk.Text(root, state=tk.NORMAL, font=(font_type, font_size, "normal"))

scroll_bar_vertical = tk.Scrollbar(root, orient=tk.VERTICAL)
scroll_bar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
scroll_bar_vertical.config(command=textbox.yview)

textbox.config(yscrollcommand=scroll_bar_vertical.set)
textbox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

# To make it more seamless
# The preview window was the focused one before
root.focus_force()

previewWindowCreation(hidden=True)

"""
Menu Bar
"""
menubar = tk.Menu(root, tearoff=0)

# Menu items
filemenu = tk.Menu(menubar, tearoff=0)
editmenu = tk.Menu(menubar, tearoff=0)
formatmenu = tk.Menu(menubar, tearoff=0)
textfontmenu = tk.Menu(formatmenu, tearoff=0)
textsizemenu = tk.Menu(formatmenu, tearoff=0)
textstylemenu = tk.Menu(formatmenu, tearoff=0)
helpmenu = tk.Menu(menubar, tearoff=0)

# File menu items
filemenu.add_command(label="New File", accelerator="Ctrl+N", command=newFile)
root.bind_all("<Control-n>", newFile)

filemenu.add_command(label="Open File", accelerator="Ctrl+O", command=openFile)
root.bind_all("<Control-o>", openFile)

filemenu.add_command(label="View File", command=viewFile)

filemenu.add_separator()

filemenu.add_command(label="Save", accelerator="Ctrl+S", command=saveFile)
root.bind_all("<Control-s>", saveFile)

filemenu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=saveFileAs)
root.bind_all("<Control-S>", saveFileAs)

filemenu.add_separator()

filemenu.add_command(label="Edit Mode", accelerator="Alt+E", command=editingMode)
root.bind_all("<Alt-e>", editingMode)

filemenu.add_command(label="View Mode", accelerator="Alt+V", command=viewingMode)
root.bind_all("<Alt-v>", viewingMode)

filemenu.add_separator()

filemenu.add_command(label="Exit", accelerator="Ctrl+W", command=quitApp)
root.bind_all("<Control-w>", quitApp)
# md_preview_window.bind_all("<Control-w>", closePreview)

# Edit menu items
editmenu.add_command(label="Undo", accelerator="Ctrl+Z", command=undo)
root.bind_all("<Control-z>", undo)

editmenu.add_command(label="Redo", accelerator="Ctrl+Shift+Z", command=redo)
root.bind_all("<Control-Z>", redo)

editmenu.add_separator()

editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=cut)

editmenu.add_command(label="Copy", accelerator="Ctrl+C", command=copy)

editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=paste)

editmenu.add_separator()

editmenu.add_command(label="Select All", accelerator="Ctrl+A", command=select_all)

editmenu.add_command(label="Deselect All", accelerator="Ctrl+Shift+A", command=deselect_all)
root.bind_all("<Control-A>", deselect_all)

editmenu.add_separator()

editmenu.add_command(label="Open Markdown Preview", accelerator="Alt+P", command=openPreview)
root.bind_all("<Alt-p>", openPreview)

editmenu.add_command(label="Close Markdown Preview", accelerator="Alt+Shift+P", command=closePreview)
root.bind_all("<Alt-P>", closePreview)
md_preview_window.bind_all("<Alt-P>", closePreview)

editmenu.add_command(label="Update Markdown Preview", accelerator="Ctrl+E", command=updatePreview)
root.bind_all("<Control-e>", updatePreview)
md_preview_window.bind_all("<Control-e>", updatePreview)

editmenu.add_separator()

editmenu.add_command(label="Edit Preferences", command=openPreferences)

# Format menu items
textfontmenu.add_command(label="Arial")

textsizemenu.add_command(label="Increase Font Size", accelerator="Ctrl+Shift++", command=increase_font)
root.bind_all("<Control-+>", increase_font)

textsizemenu.add_command(label="Decrease Font Size", accelerator="Ctrl+Shift+-", command=decrease_font)
root.bind_all("<Control-_>", decrease_font)

formatmenu.add_command(label="Text Colour", accelerator="Alt+C", command=text_colour_change)
root.bind_all("<Alt-c>", text_colour_change)

textstylemenu.add_command(label="Normal", accelerator="Alt+N", command=normal_text_style)
root.bind_all("<Alt-n>", normal_text_style)

textstylemenu.add_command(label="Bold", accelerator="Alt+B", command=bold_text_style)
root.bind_all("<Alt-b>", bold_text_style)

textstylemenu.add_command(label="Italic", accelerator="Alt+I", command=italic_text_style)
root.bind_all("<Alt-i>", italic_text_style)

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

# Track document changes and update markdown preview
root.bind('<Key>', trackChanges)

"""
Window Display
"""
# When closing the app, run the quit_app function
root.protocol("WM_DELETE_WINDOW", quitApp)
md_preview_window.protocol("WM_DELETE_WINDOW", md_preview_window.destroy)

# Display the window
md_preview_window.mainloop()
root.mainloop()
