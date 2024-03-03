# Created by Sooraj
# https://encryptext.sooraj.dev
# Free for everyone. Forever.
"""
Imports
"""
import sys
from os.path import abspath, join
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
from traceback import format_exc, print_exc # For the error messages when in exe form
from webbrowser import open_new # For opening the help page
from cryptography.fernet import Fernet  # For encryption features
# For Markdown preview features
import tkinterweb
from markdown import markdown

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
        frame = tkinterweb.HtmlFrame(md_preview_window, messages_enabled=False)

        current_tab = getCurrentTab()
        if current_tab == -1:
            return None

        frame.load_html(markdown(textboxes[current_tab].get("1.0", tk.END)))
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
debug = True
# UPDATE MODE HERE
update = True# UPDATE MODE HERE
version = "1.7.1"

update_file_title = " DO NOT SAVE THIS FILE "

file_save_locations = []
file_extensions = []

default_font_size = 11
default_font_type = "Arial"
max_font_size = 96
min_font_size = 8
font_sizes = []
font_type = []

# Uses random random-length strings of characters to determine where formatting starts and stops# FORMAT ITEM SEPARATOR HERE
format_item_separator = ''# FORMAT ITEM SEPARATOR HERE# FORMAT SEPARATOR HERE
format_separator = ''# FORMAT SEPARATOR HERE# FORMAT STRING HERE
format_string = ''# FORMAT STRING HERE

supported_file_types = [
    ("Accepted Files", "*.etx *.md *.txt *.py *.html *.css *.js *.json *.csv *.ini *.log"),
    ("Encrypted File", "*.etx"),
    ("Markdown File", "*.md"),
    ("Plain Text File", "*.txt"),
    ("Python File", "*.py"),
    ("HTML File", "*.html"),
    ("CSS File", "*.css"),
    ("JavaScript File", "*.js"),
    ("JSON File", "*.json"),
    ("Comma-Separated Values File", "*.csv"),
    ("Windows Initialization File", "*.ini"),
    ("Log File", "*.log"),
    ("All Files", "*.*")
]
# ENCRYPTION KEY HERE
encrypt_key = b''# ENCRYPTION KEY HERE

# For debug purposes, set static key and separators
if debug:
    encrypt_key = b'4P7ySeLwmoC61q8Nsm7SiEpGW_Y9eISDlg07f699uAo='
    format_item_separator = "@@@"
    format_separator = "^^^"
    format_string = "&&&"

fernet = Fernet(encrypt_key)

# Have atleast 3 versions of history
file_histories = []
# Set the current history version to 1 (centered)
current_versions = []
max_history = 50

file_format_tags = []
file_format_tag_nums = []

textboxes = []

"""
Functions
"""

def updateTags():
    global file_format_tags

    current_tab = getCurrentTab()
    if current_tab == -1:
        return ""

    tags_used = textboxes[current_tab].tag_names()
    i = 0
    for tag in tags_used:
        indices = textboxes[current_tab].tag_ranges(tag)
        for start, end in zip(indices[::2], indices[1::2]):
            file_format_tags[current_tab][i][1] = str(start)
            file_format_tags[current_tab][i][2] = str(end)

            i += 1

    formatted_tags = [format_item_separator.join(tag) for tag in file_format_tags[current_tab]]
    formatted_tags = format_separator.join(formatted_tags)

    return formatted_tags

def quitApp(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        try:
            md_preview_window.destroy()
            pref_window.destroy()
        finally:
            root.destroy()
            sys.exit()

    # Check if any of the tab's textboxes are not empty
    quit_confirm = True
    for textbox in textboxes:
        if len(textbox.get("1.0", tk.END)) != 1 or textbox.get("1.0", tk.END) != "\n":
            quit_confirm = False

    # If there's one that's not empty, then show warning
    if not quit_confirm:
        quit_confirm = messagebox.askyesno("Quit", "Quit Encryptext?\n\nAny unsaved changes will be lost.")

    if quit_confirm:
        try:
            md_preview_window.destroy()
            pref_window.destroy()
        finally:
            root.destroy()
            sys.exit()

def openFile(Event=None, current=False):
    # Make save_location global to change it for the whole program
    global file_save_locations, file_format_tags, file_histories, current_versions, file_format_tag_nums, file_extensions

    current_tab = getCurrentTab()
    if current_tab == -1:
        addNewTab()

    # Reset tag number
    file_format_tag_nums[current_tab] = 0

    # Check if the current textbox is empty
    if len(textboxes[current_tab].get("1.0", tk.END)) > 2 and textboxes[current_tab].get("1.0", tk.END) != "\n\n" and not current:
        new_file_confirm = messagebox.askyesno("Open File", "Open a file?\n\nAny unsaved changes will be lost.")
    else:
        new_file_confirm = True

    if new_file_confirm:
        # Show a file selector and let user choose file
        if not current:
            file_save_locations[current_tab] = filedialog.askopenfilename(title="Select file", filetypes=supported_file_types)

        if file_save_locations[current_tab] != "":
            # Get the file exntension
            file_extensions[current_tab] = file_save_locations[current_tab].split(".")[-1]
            # Get file name
            file_name = file_save_locations[current_tab].split("/")[-1]

            # Set the title of the window to the file name
            tab_panes.tab(tab_panes.tabs()[getCurrentTab()], text=f" {file_name} ")

            # Open the file and read its contents into an array
            file = open(file_save_locations[current_tab], "r")

            # Set the current textbox to be writable
            textboxes[current_tab].config(state=tk.NORMAL)

            # Clear the current textbox
            textboxes[current_tab].delete("1.0", tk.END)

            # Clear the history
            file_histories[current_tab] = ["", "", ""]
            current_versions[current_tab] = 1

            # If the file is a .etx file, decrypt it
            if file_extensions[current_tab] == "etx":
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
                                format_style[0] = f"{''.join(i for i in format_style[0] if not i.isdigit())}{file_format_tag_nums[current_tab]}"
                                formats.append(format_style)
                                file_format_tag_nums[current_tab] += 1
                            else:
                                format_type = "".join(i for i in format_style[0] if not i.isdigit())
                                for f in formats:
                                    if format_type == "".join(i for i in f[0] if not i.isdigit()) and format_style[1] == f[1] and format_style[2] == f[2]:
                                        add = False
                                        break

                                if add:
                                    format_style[0] = f"{''.join(i for i in format_style[0] if not i.isdigit())}{file_format_tag_nums[current_tab]}"
                                    formats.append(format_style)
                                    file_format_tag_nums[current_tab] += 1

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

                    # Write the file contents to the current textbox
                    # Removes the extra newline that tkinter adds
                    textboxes[current_tab].insert(tk.END, text[:-1])

                    # Add all the formatting to the text and add it to the tags list
                    if formats != []:
                        for i in range(len(formats)):
                            format = formats[i]

                            textboxes[current_tab].tag_add(format[0], format[1], format[2])

                            if "colour" in format[0]:
                                textboxes[current_tab].tag_config(format[0], foreground=format[3])
                            elif "size" in format[0]:
                                textboxes[current_tab].tag_config(format[0], font=(format[3], int(format[4])))
                            else:
                                # Get format type
                                if "bold" in format[0]:
                                    textboxes[current_tab].tag_config(format[0], font=(format[3], int(format[4]), "bold"))
                                elif "italic" in format[0]:
                                    textboxes[current_tab].tag_config(format[0], font=(format[3], int(format[4]), "italic"))
                                elif "normal" in format[0]:
                                    textboxes[current_tab].tag_config(format[0], font=(format[3], int(format[4]), "normal"))

                            file_format_tags[current_tab].append(format)
                except Exception as e:
                    if debug:
                        messagebox.showerror("Error Opening File", format_exc())
                        print_exc()
                    else:
                        messagebox.showerror("Error Opening File", f"Access denied.\nPlease use the Encryptext program that you used to write this file to open it correctly.")
            else:
                # Write the file contents to the current textbox
                textboxes[current_tab].insert(tk.END, file.read()[:-1])

                # Close the file
                file.close()
            if file_extensions[current_tab] == "md":
                global md_preview_window
                try:
                    md_preview_window.deiconify()
                    updatePreview()
                except:
                    previewWindowCreation()

def newFile(Event=None):
    global file_save_locations, file_histories, current_versions

    current_tab = getCurrentTab()
    if current_tab == -1:
        addNewTab()

    # Check if the current textbox is empty
    if len(textboxes[current_tab].get("1.0", tk.END)) != 1:
        new_file_confirm = messagebox.askyesno("New File", "Create new file?\n\nAny unsaved changes will be lost.")
        if new_file_confirm:
            file_save_locations[current_tab] = ""
            textboxes[current_tab].config(state=tk.NORMAL)
            textboxes[current_tab].delete("1.0", tk.END)

            file_histories[current_tab] = ["", "", ""]
            current_versions[current_tab] = 1

            tab_panes.tab(tab_panes.tabs()[getCurrentTab()], text=" Untitled ")
        else: pass
    else:
        file_save_locations[current_tab] = ""
        textboxes[current_tab].config(state=tk.NORMAL)
        textboxes[current_tab].delete("1.0", tk.END)

        file_histories[current_tab] = ["", "", ""]
        current_versions[current_tab] = 1

        tab_panes.tab(tab_panes.tabs()[getCurrentTab()], text=" Untitled ")

def saveFile(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    # If it's a new file
    if file_save_locations[current_tab] == "":
        saveFileAs()
    else:
        # Get the text from the current textbox
        text = textboxes[current_tab].get("1.0", tk.END)

        # If the file is a .etx file, encrypt it
        if file_save_locations[current_tab].split(".")[-1] == "etx":
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
        file = open(file_save_locations[current_tab], "w")
        file.write(text)
        file.close()

def saveFileAs(Event=None):
    global file_save_locations

    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    # Get the text from the current textbox
    text = textboxes[current_tab].get("1.0", tk.END)

    # Show a file selector and let user choose file
    file_save_locations[current_tab] = filedialog.asksaveasfilename(title="Save file as", filetypes=supported_file_types, defaultextension=supported_file_types)

    if file_save_locations[current_tab] != "":
        # If the file is a .etx file, encrypt it
        if file_save_locations[current_tab].split(".")[-1] == "etx":
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
        file = open(file_save_locations[current_tab], "w")
        file.write(text)
        file.close()

        # Open the new file
        openFile(current=True)

def undo(Event=None):
    global file_histories

    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    # Check if the previous version is the same as the current version
    if file_histories[current_tab][current_versions[current_tab] - 1] != textboxes[current_tab].get("1.0", tk.END):
        # Update the current version
        file_histories[current_tab][current_versions[current_tab]] = textboxes[current_tab].get("1.0", tk.END)
        # Remove the last newline character
        file_histories[current_tab][current_versions[current_tab]] = file_histories[current_tab][current_versions[current_tab]][:-1]

        # Check if the final version is blank
        if file_histories[current_tab][-1] != "":
            if len(file_histories[current_tab]) - current_versions[current_tab] < max_history:
                # Add a new version
                file_histories[current_tab].append("")

        # Shift every version up one
        for i in range(len(file_histories[current_tab]) - 1, 0, -1):
            file_histories[current_tab][i] = file_histories[current_tab][i - 1]

        # Clear the first version
        file_histories[current_tab][0] = ""

        # Update the current textbox
        textboxes[current_tab].delete("1.0", tk.END)
        textboxes[current_tab].insert(tk.END, file_histories[current_tab][current_versions[current_tab]])

def redo(Event=None):
    global file_histories, current_versions

    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    # Check if the next version is the same as the current version
    if file_histories[current_tab][current_versions[current_tab] + 1] != textboxes[current_tab].get("1.0", tk.END):
        # Update the current version
        file_histories[current_tab][current_versions[current_tab]] = textboxes[current_tab].get("1.0", tk.END)
        # Remove the last newline character
        file_histories[current_tab][current_versions[current_tab]] = file_histories[current_tab][current_versions[current_tab]][:-1]

        # Check if the first version is blank
        if file_histories[current_tab][0] != "":
            if current_versions[current_tab] < max_history:
                # Add a new version
                file_histories[current_tab].insert(0, "")
                # Update the current version
                current_versions[current_tab] += 1

        # Shift every version down one
        for i in range(0, len(file_histories[current_tab]) - 1):
            file_histories[current_tab][i] = file_histories[current_tab][i + 1]

        # Clear the last version
        file_histories[current_tab][-1] = ""

        # Update the current textbox
        textboxes[current_tab].delete("1.0", tk.END)
        textboxes[current_tab].insert(tk.END, file_histories[current_tab][current_versions[current_tab]])

def updatePreview(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    try:
        # Update the preview
        frame.load_html(markdown(textboxes[current_tab].get("1.0", tk.END)))
    except:
        # Only update it if it's markdown or none
        if file_extensions[current_tab] == "md":
            # If the preview window was opened manually
            previewWindowCreation()

def trackChanges(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    if Event.keysym in ["space", "Return", "quoteleft", "asciitilde", "exclam", "at", "numbersign", "dollar", "percent", "asciicircum", "ampersand", "asterisk", "parenleft", "parenright", "underscore", "plus", "braceleft", "braceright", "bar", "colon", "less", "greater", "question", "minus", "equal", "bracketleft", "bracketright", "backslash", "semicolon", "quoteright", "comma", "period", "slash", "Tab"]:
        global file_histories, current_versions

        # Check if the first version is empty
        if file_histories[current_tab][0] != "":
            if current_versions[current_tab] < max_history:
                # Add a new version
                file_histories[current_tab].insert(0, "")
                # Update the current version
                current_versions[current_tab] += 1

        # Shift every version down one
        for i in range(0, len(file_histories[current_tab]) - 1):
            file_histories[current_tab][i] = file_histories[current_tab][i + 1]

        # Update the current version
        file_histories[current_tab][current_versions[current_tab]] = textboxes[current_tab].get("1.0", tk.END)
        # Remove the last newline character
        file_histories[current_tab][current_versions[current_tab]] = file_histories[current_tab][current_versions[current_tab]][:-1]

    # Update the preview
    updatePreview()

def cut(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    textboxes[current_tab].event_generate("<<Cut>>")

def copy(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    textboxes[current_tab].event_generate("<<Copy>>")

def paste(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    textboxes[current_tab].event_generate("<<Paste>>")

def viewFile(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    # Open the file
    openFile()

    # Set the textbox to be read-only
    textboxes[current_tab].config(state=tk.DISABLED)

def viewingMode(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    # Set the textbox to be read-only
    textboxes[current_tab].config(state=tk.DISABLED)

def editingMode(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    # Don't allow the encryption key tab to be edited
    tab_title = tab_panes.tab(tab_panes.tabs()[getCurrentTab()])["text"]
    if tab_title == update_file_title:
        return None

    # Set the textbox to be writable
    textboxes[current_tab].config(state=tk.NORMAL)

def openPreview(Event=None):
    try:
        md_preview_window.deiconify()
    except:
        previewWindowCreation()

def closePreview(Event=None):
    try:
        md_preview_window.withdraw()
    except: pass

def selectAll(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    textboxes[current_tab].event_generate("<<SelectAll>>")

def deselectAll(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    textboxes[current_tab].event_generate("<<SelectNone>>")

def openPreferences():
    global pref_window, frame

    pref_window = tk.Tk("Preferences")
    pref_window.title("Preferences")
    pref_window.geometry("500x600")
    pref_window.iconbitmap(getTrueFilename("app_icon.ico"))
    pref_window.protocol("WM_DELETE_WINDOW", pref_window.destroy)

    pref_window.mainloop()

def updateMenu(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        addNewTab()

    messagebox.showinfo("Update Encryptext", """1. Run the new version's installer\n2. When it asks whether you're installing or updating, choose updating.\n3. When it asks for the old enryption key and other strings, copy and paste the ones shown in the text editor here.\n\nClick 'Ok' to view the keys.\n\nDO NOT SAVE THE DOCUMENT WITH THE KEYS.""")

    key = encrypt_key.decode()

    # Change the title
    tab_panes.tab(tab_panes.tabs()[getCurrentTab()], text=update_file_title)

    # Add the needed strings to the box
    textboxes[current_tab].delete("1.0", tk.END)
    textboxes[current_tab].insert("1.0", f"Encryption Key: {key}\nFormat Item Separator: {format_item_separator}\nFormat Separator String: {format_separator}\nFormat String: {format_string}")

    # Enter viewing mode so that the string can't be accidentally changed
    viewingMode()

def aboutMenu(Event=None):
    messagebox.showinfo("About Encryptext", f"Unlock a new level of security and versatility with Encryptext, the text editor designed for the modern user. Seamlessly blending essential features with modern encryption technology, Encryptext ensures your documents are safeguarded like never before.\n\nFree for everyone. Forever. ❤\n\nVersion {version}")

def documentation(Event=None):
    open_new("https://github.com/WhenLifeHandsYouLemons/Encryptext")

def changeToBold(Event=None):
    global file_format_tag_nums

    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    # Get the position of current selection
    start_selection = textboxes[current_tab].index("sel.first")
    end_selection = textboxes[current_tab].index("sel.last")

    # Create a tag
    textboxes[current_tab].tag_add(f"bold{file_format_tag_nums[current_tab]}", start_selection, end_selection)
    textboxes[current_tab].tag_config(f"bold{file_format_tag_nums[current_tab]}", font=(font_type[current_tab], font_sizes[current_tab], "bold"))
    file_format_tags[current_tab].append([f"bold{file_format_tag_nums[current_tab]}", start_selection, end_selection, font_type[current_tab], str(font_sizes[current_tab])])

    file_format_tag_nums[current_tab] += 1

def changeToItalic(Event=None):
    global file_format_tag_nums

    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    # Get the position of current selection
    start_selection = textboxes[current_tab].index("sel.first")
    end_selection = textboxes[current_tab].index("sel.last")

    # Create a tag
    textboxes[current_tab].tag_add(f"italic{file_format_tag_nums[current_tab]}", start_selection, end_selection)
    textboxes[current_tab].tag_config(f"italic{file_format_tag_nums[current_tab]}", font=(font_type[current_tab], font_sizes[current_tab], "italic"))
    file_format_tags[current_tab].append([f"italic{file_format_tag_nums[current_tab]}", start_selection, end_selection, font_type[current_tab], str(font_sizes[current_tab])])

    file_format_tag_nums[current_tab] += 1

def changeToNormal(Event=None):
    global file_format_tag_nums

    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    # Get the position of current selection
    start_selection = textboxes[current_tab].index("sel.first")
    end_selection = textboxes[current_tab].index("sel.last")

    # Create a tag
    textboxes[current_tab].tag_add(f"normal{file_format_tag_nums[current_tab]}", start_selection, end_selection)
    textboxes[current_tab].tag_config(f"normal{file_format_tag_nums[current_tab]}", font=(font_type[current_tab], font_sizes[current_tab], "normal"))
    file_format_tags[current_tab].append([f"normal{file_format_tag_nums[current_tab]}", start_selection, end_selection, font_type[current_tab], str(font_sizes[current_tab])])

    file_format_tag_nums[current_tab] += 1

def changeTextColour(Event=None):
    global file_format_tag_nums

    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    colour_code = colorchooser.askcolor(title="Choose a colour")
    colour_code = colour_code[-1]

    # Get the position of current selection
    start_selection = textboxes[current_tab].index("sel.first")
    end_selection = textboxes[current_tab].index("sel.last")

    # Create a tag
    textboxes[current_tab].tag_add(f"colour{file_format_tag_nums[current_tab]}", start_selection, end_selection)
    textboxes[current_tab].tag_config(f"colour{file_format_tag_nums[current_tab]}", foreground=colour_code)

    file_format_tags[current_tab].append([f"colour{file_format_tag_nums[current_tab]}",start_selection,end_selection,colour_code,font_type[current_tab],str(font_sizes[current_tab]),])

    file_format_tag_nums[current_tab] += 1

def increaseFont(Event=None):
    global file_format_tag_nums, font_sizes

    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    if font_sizes[current_tab] == max_font_size:
        messagebox.showerror("Error", "Font size cannot go higher than 96.")
    else:
        try:
            start_selection = textboxes[current_tab].index("sel.first")
            end_selection = textboxes[current_tab].index("sel.last")
            textboxes[current_tab].tag_add(f"size{file_format_tag_nums[current_tab]}", start_selection, end_selection)

            font_sizes[current_tab] += 1
            size = font_sizes[current_tab]
            textboxes[current_tab].tag_config(f"size{file_format_tag_nums[current_tab]}", font=(font_type[current_tab], size))

            file_format_tags[current_tab].append([f"size{file_format_tag_nums[current_tab]}", start_selection, end_selection, font_type[current_tab], str(size)])
            file_format_tag_nums[current_tab] += 1
        except:
            pass

def decreaseFont(Event=None):
    global file_format_tag_nums, font_sizes

    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    if font_sizes[current_tab] == min_font_size:
        messagebox.showerror("Error", "Font size cannot go lower than 8.")
    else:
        try:
            start_selection = textboxes[current_tab].index("sel.first")
            end_selection = textboxes[current_tab].index("sel.last")
            textboxes[current_tab].tag_add(f"size{file_format_tag_nums[current_tab]}", start_selection, end_selection)

            font_sizes[current_tab] -= 1
            size = font_sizes[current_tab]
            textboxes[current_tab].tag_config(f"size{file_format_tag_nums[current_tab]}", font=(font_type[current_tab], size))

            file_format_tags[current_tab].append([f"size{file_format_tag_nums[current_tab]}", start_selection, end_selection, font_type[current_tab], str(size)])
            file_format_tag_nums[current_tab] += 1
        except:
            pass

def showQuickMenu(Event=None):
    try:
        rightclickmenu.tk_popup(Event.x_root, Event.y_root)
    finally:
        rightclickmenu.grab_release()

def addNewTab(Event=None):
    # Create new textbox
    textboxes.append(tk.Text(tab_panes, state=tk.NORMAL, font=(default_font_type, default_font_size, "normal"), cursor="xterm"))

    # Create new tab info slot in arrays
    file_save_locations.append("")
    file_extensions.append("")
    file_histories.append(["", "", ""])
    current_versions.append(1)
    file_format_tags.append([])
    file_format_tag_nums.append(0)
    font_sizes.append(default_font_size)
    font_type.append(default_font_type)

    # Create scroll bar and link it
    scroll_bars = []
    scroll_bars.append(tk.Scrollbar(textboxes[-1], orient=tk.VERTICAL, cursor="arrow"))
    scroll_bars[-1].pack(side=tk.RIGHT, fill=tk.Y)
    scroll_bars[-1].config(command=textboxes[-1].yview)

    textboxes[-1].config(yscrollcommand=scroll_bars[-1].set)

    # Add to display
    textboxes[-1].pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    tab_panes.add(textboxes[-1], text=" Untitled ")

    # Allow right-click menu to show up
    # textboxes[-1].bind("<Button-3>", showQuickMenu)

    # Fix Ctrl+T switching last char in textbox
    # https://stackoverflow.com/a/54185644
    bindtags = textboxes[-1].bindtags()
    textboxes[-1].bindtags((bindtags[2], bindtags[0], bindtags[1], bindtags[3]))

    # Sets the tab focus to the newly created tab
    tab_panes.select(tab_panes.tabs()[-1])
    textboxes[-1].focus()

    return "break"

def closeCurrentTab(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    # Remove any tab info from arrays
    tab_panes.forget(current_tab)
    textboxes.pop(current_tab)
    file_save_locations.pop(current_tab)
    file_extensions.pop(current_tab)
    file_histories.pop(current_tab)
    current_versions.pop(current_tab)
    file_format_tags.pop(current_tab)
    file_format_tag_nums.pop(current_tab)

def getCurrentTab() -> int:
    try:
        return tab_panes.index("current")
    except: # Returns -1 if there are no tabs
        return -1

"""
Window Items
"""
tab_panes = ttk.Notebook(root, cursor="hand2", padding=5)
tab_panes.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
tab_panes.enable_traversal()

# Create the first tab
addNewTab()

# To make it more seamless
# The preview window was the focused one before
root.focus_force()

previewWindowCreation(hidden=True)

"""
Menu Bar
"""
# Quick menu
rightclickmenu = tk.Menu(root, tearoff=0)

rightclickmenu.add_command(label="Cut")
rightclickmenu.add_command(label="Copy")
rightclickmenu.add_command(label="Paste")
rightclickmenu.add_command(label="Reload")
rightclickmenu.add_separator()
rightclickmenu.add_command(label="Rename")

# Top bar menu
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

filemenu.add_command(label="New Tab", accelerator="Ctrl+T", command=addNewTab)
root.bind("<Control-t>", addNewTab)

filemenu.add_command(label="Close Tab", accelerator="Alt+W", command=closeCurrentTab)
root.bind_all("<Alt-w>", closeCurrentTab)

filemenu.add_separator()

filemenu.add_command(label="Exit", accelerator="Ctrl+W", command=quitApp)
root.bind_all("<Control-w>", quitApp)
md_preview_window.bind_all("<Control-w>", closePreview)

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

editmenu.add_command(label="Select All", accelerator="Ctrl+A", command=selectAll)

editmenu.add_command(label="Deselect All", accelerator="Ctrl+Shift+A", command=deselectAll)
root.bind_all("<Control-A>", deselectAll)

editmenu.add_separator()

editmenu.add_command(label="Open Markdown Preview", accelerator="Ctrl+P", command=openPreview)
root.bind_all("<Control-p>", openPreview)

editmenu.add_command(label="Close Markdown Preview", accelerator="Ctrl+Shift+P", command=closePreview)
root.bind_all("<Control-P>", closePreview)
md_preview_window.bind_all("<Control-P>", closePreview)

editmenu.add_command(label="Update Markdown Preview", accelerator="Ctrl+E", command=updatePreview)
root.bind_all("<Control-e>", updatePreview)
md_preview_window.bind_all("<Control-e>", updatePreview)

editmenu.add_separator()

editmenu.add_command(label="Edit Preferences", command=openPreferences)

# Format menu items
textfontmenu.add_command(label="Arial")

textsizemenu.add_command(label="Increase Font Size", accelerator="Ctrl+Shift++", command=increaseFont)
root.bind_all("<Control-+>", increaseFont)

textsizemenu.add_command(label="Decrease Font Size", accelerator="Ctrl+Shift+-", command=decreaseFont)
root.bind_all("<Control-_>", decreaseFont)

formatmenu.add_command(label="Text Colour", accelerator="Alt+C", command=changeTextColour)
root.bind_all("<Alt-c>", changeTextColour)

textstylemenu.add_command(label="Normal", accelerator="Alt+N", command=changeToNormal)
root.bind_all("<Alt-n>", changeToNormal)

textstylemenu.add_command(label="Bold", accelerator="Alt+B", command=changeToBold)
root.bind_all("<Alt-b>", changeToBold)

textstylemenu.add_command(label="Italic", accelerator="Alt+I", command=changeToItalic)
root.bind_all("<Alt-i>", changeToItalic)

if update:
    helpmenu.add_command(label="Update Encryptext", command=updateMenu)

helpmenu.add_command(label="About Encryptext", command=aboutMenu)

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
