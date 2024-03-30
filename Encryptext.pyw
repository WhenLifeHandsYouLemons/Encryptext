# Created by Sooraj S
# https://encryptext.sooraj.dev
# Free for everyone. Forever.

"""
Imports
"""
import sys
from os.path import abspath, join, expanduser
#! from os import getenv     # Not useful right now, but could be useful if translations are available
import json
import tkinter as tk
from tkinter import font
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

debug = False
# UPDATE MODE HERE
update = False# UPDATE MODE HERE

try:
    settings_path = join(expanduser("~"), ".encryptext", "settings.json")
    with open(settings_path, "r", encoding="utf-8") as file:
        settings = json.load(file)
except FileNotFoundError:
    settings = {
        "version": "'Encryptext Offline Mode'",
        "recentFilePaths": [],
        "maxRecentFiles": 0,
        "otherSettings": {
            "theme": "light",
            "fontStyle": "Arial",
            "fontScaleFactor": 1,
            "language": "en_US",
            "autoSave": False,
            "autoSaveInterval": 0,
            "showLineNumbers": False,
            "wrapLines": True,
            "highlightActiveLine": False,
            "closeAllTabs": False
        }
    }

version = settings["version"]
font_scale_factor = settings["otherSettings"]["fontScaleFactor"]

"""
Custom Classes
"""
# From: https://www.reddit.com/r/learnpython/comments/6dndqz/comment/di42keo/
class WrappedLabel(ttk.Label):
    """a type of Label that automatically adjusts the wrap to the size"""
    def __init__(self, master=None, **kwargs):
        ttk.Label.__init__(self, master, **kwargs)
        self.bind("<Configure>", lambda e: self.config(wraplength=self.winfo_width()))

class PreferenceWindow(tk.Toplevel):
    win_open = False

    def __init__(self, close=False) -> None:
        if not self.win_open and not close:
            self.pref_window = tk.Toplevel()

            self.pref_window.title("Preferences")
            self.pref_window.geometry("450x600")
            self.pref_window.iconbitmap(getTrueFilename("app_icon.ico"))
            self.pref_window.protocol("WM_DELETE_WINDOW", self.closeWindow)

            self.win_open = True

            self.option_pady = 3

            # Recent file number
            self.selected_recent_files = tk.IntVar(value=settings["maxRecentFiles"])
            self.title = WrappedLabel(self.pref_window, text="Preferences", font=(settings["otherSettings"]["fontStyle"], int(round(18*font_scale_factor))))
            self.recent_file_label = WrappedLabel(self.pref_window, text="Number of recent files to store: ", anchor="nw", font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
            self.recent_file_val = ttk.Spinbox(self.recent_file_label, textvariable=self.selected_recent_files, from_=0, to=20, width=5, font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))

            # Font style picker
            self.selected_font_style = tk.StringVar(value=settings["otherSettings"]["fontStyle"])
            self.font_style_label = WrappedLabel(self.pref_window, text="Display font style: ", font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
            font_options = sorted(list(font.families()))
            self.font_style_val = ttk.Combobox(self.font_style_label, textvariable=self.selected_font_style, values=font_options, state="readonly", font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))

            # Font size number
            self.selected_font_sf = tk.DoubleVar(value=settings["otherSettings"]["fontScaleFactor"])
            self.font_sf_label = WrappedLabel(self.pref_window, text="Display font size scale factor: ", font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
            self.font_sf_val = ttk.Spinbox(self.font_sf_label, textvariable=self.selected_font_sf, from_=0.5, to=2, increment=0.05, width=5, font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))

            # Theme selector
            self.selected_theme = tk.StringVar(value=settings["otherSettings"]["theme"])
            self.theme_label = WrappedLabel(self.pref_window, text="Theme: ", font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
            self.light_theme_val = ttk.Radiobutton(self.theme_label, text="Light", value="light", variable=self.selected_theme)
            self.dark_theme_val = ttk.Radiobutton(self.theme_label, text="Dark", value="dark", variable=self.selected_theme)

            # Auto-save selector
            self.selected_auto_save = tk.StringVar(value=str(settings["otherSettings"]["autoSave"]).lower())
            self.auto_save_val = ttk.Checkbutton(self.pref_window, text="Auto-save", variable=self.selected_auto_save, onvalue="true", offvalue="false")

            # Auto-save interval number
            self.selected_auto_save_interval_val = tk.IntVar(value=settings["otherSettings"]["autoSaveInterval"])
            self.auto_save_interval_label = WrappedLabel(self.pref_window, text="Auto-save interval: ", font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
            self.auto_save_interval_val = ttk.Spinbox(self.auto_save_interval_label, textvariable=self.selected_auto_save_interval_val, from_=1, to=300, increment=15, width=5, font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))

            # Language picker
            self.selected_language = tk.StringVar(value=settings["otherSettings"]["language"])
            self.language_label = WrappedLabel(self.pref_window, text="Display language: ", font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
            #! getenv("LANG").split(".")[0]      # Can be useful to get the user's default language
            lang_options = ["en_US"]
            self.language_val = ttk.Combobox(self.language_label, textvariable=self.selected_language, values=lang_options, state="readonly", font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))

            # show checkboxes for other true/false options
            self.selected_show_line_no = tk.StringVar(value=str(settings["otherSettings"]["showLineNumbers"]).lower())
            self.show_line_no_val = ttk.Checkbutton(self.pref_window, text="Show line numbers", variable=self.selected_show_line_no, onvalue="true", offvalue="false")
            self.selected_wrap_line = tk.StringVar(value=str(settings["otherSettings"]["wrapLines"]).lower())
            self.wrap_line_val = ttk.Checkbutton(self.pref_window, text="Wrap text", variable=self.selected_wrap_line, onvalue="true", offvalue="false")
            self.selected_show_active_line = tk.StringVar(value=str(settings["otherSettings"]["highlightActiveLine"]).lower())
            self.show_active_line_val = ttk.Checkbutton(self.pref_window, text="Highlight active line", variable=self.selected_show_active_line, onvalue="true", offvalue="false")
            self.selected_close_all_tabs = tk.StringVar(value=str(settings["otherSettings"]["closeAllTabs"]).lower())
            self.close_all_tabs_val = ttk.Checkbutton(self.pref_window, text="Close all tabs", variable=self.selected_close_all_tabs, onvalue="true", offvalue="false")

            # Info text
            self.info_text = WrappedLabel(self.pref_window, text="Reopen Encryptext to see changes after saving.", anchor="sw", font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))

            # Save button
            self.save_button = ttk.Button(self.pref_window, text="Save Preferences", command=self.savePreferences)

            # Add all items to the display
            self.title.pack(side="top", fill="x", anchor="nw", padx=5, pady=10)
            ttk.Separator(self.pref_window, orient="horizontal").pack(side="top", fill="x", padx=5, pady=5)

            self.recent_file_label.pack(side="top", anchor="w", fill="x", padx=5)
            self.recent_file_val.pack(side="right", padx=20, pady=self.option_pady)
            ttk.Separator(self.pref_window, orient="horizontal").pack(side="top", fill="x", padx=100, pady=10)

            self.font_style_label.pack(side="top", fill="x", padx=5, anchor="nw")
            self.font_style_val.pack(side="right", padx=20, pady=self.option_pady)
            self.font_sf_label.pack(side="top", fill="x", padx=5, anchor="nw")
            self.font_sf_val.pack(side="right", padx=20, pady=self.option_pady)
            ttk.Separator(self.pref_window, orient="horizontal").pack(side="top", fill="x", padx=100, pady=10)

            self.theme_label.pack(side="top", fill="x", padx=5, anchor="n")
            self.dark_theme_val.pack(side="right", padx=20, pady=self.option_pady)
            self.light_theme_val.pack(side="right", padx=20, pady=self.option_pady)
            ttk.Separator(self.pref_window, orient="horizontal").pack(side="top", fill="x", padx=100, pady=10)

            self.auto_save_val.pack(side="top", anchor="nw", padx=5, pady=self.option_pady)
            self.auto_save_interval_label.pack(side="top", fill="x", padx=5, anchor="nw")
            self.auto_save_interval_val.pack(side="right", padx=20, pady=self.option_pady)
            ttk.Separator(self.pref_window, orient="horizontal").pack(side="top", fill="x", padx=100, pady=10)

            self.language_label.pack(side="top", fill="x", padx=5, anchor="nw")
            self.language_val.pack(side="right", padx=20, pady=self.option_pady)
            ttk.Separator(self.pref_window, orient="horizontal").pack(side="top", fill="x", padx=100, pady=10)

            self.show_line_no_val.pack(side="top", anchor="nw", padx=5, pady=self.option_pady)
            self.wrap_line_val.pack(side="top", anchor="nw", padx=5, pady=self.option_pady)
            self.show_active_line_val.pack(side="top", anchor="nw", padx=5, pady=self.option_pady)
            self.close_all_tabs_val.pack(side="top", anchor="nw", padx=5, pady=self.option_pady)

            self.save_button.pack(side="bottom", anchor="e", pady=10, padx=10)
            self.info_text.pack(side="bottom", anchor="n", padx=5, pady=self.option_pady, fill="x")
        elif self.win_open:
            self.pref_window.focus()

    def savePreferences(self) -> None:
        global settings

        # Save preferences that have been selected
        settings["maxRecentFiles"] = self.selected_recent_files.get()
        settings["otherSettings"]["fontStyle"] = self.selected_font_style.get()
        settings["otherSettings"]["fontScaleFactor"] = self.selected_font_sf.get()
        settings["otherSettings"]["theme"] = self.selected_theme.get()
        settings["otherSettings"]["autoSave"] = self.selected_auto_save.get()
        settings["otherSettings"]["autoSaveInterval"] = self.selected_auto_save_interval_val.get()
        settings["otherSettings"]["language"] = self.language_val.get()
        settings["otherSettings"]["showLineNumbers"] = self.selected_show_line_no.get()
        settings["otherSettings"]["wrapLines"] = self.selected_wrap_line.get()
        settings["otherSettings"]["highlightActiveLine"] = self.selected_show_active_line.get()
        settings["otherSettings"]["closeAllTabs"] = self.selected_close_all_tabs.get()

        # Close the preferences window automatically
        self.closeWindow()

    def closeWindow(self) -> None:
        self.pref_window.destroy()
        self.win_open = False

class PreviewWindow(tk.Toplevel):
    win_open = False

    def __init__(self, close=False) -> None:
        if not self.win_open and not close:
            self.preview_window = tk.Toplevel()

            self.preview_window.title("Preview")
            self.preview_window.geometry("800x500")
            self.preview_window.iconbitmap(getTrueFilename("app_icon.ico"))
            self.preview_window.protocol("WM_DELETE_WINDOW", self.closeWindow)

            self.win_open = True

            self.preview_window.bind("<Control-w>", self.closeWindow)
            self.preview_window.bind_all("<Control-P>", preview_window.closeWindow)
            self.preview_window.bind_all("<Control-e>", updatePreview)

            self.addFrame()
        elif self.win_open:
            self.preview_window.focus()

    def closeWindow(self, other_args=None) -> None:
        self.preview_window.destroy()
        self.win_open = False

    def addFrame(self) -> None:
        self.frame = tkinterweb.HtmlFrame(self.preview_window, messages_enabled=False)

        current_tab = getCurrentTab()
        if current_tab == -1:
            return None

        self.frame.load_html(markdown(textboxes[current_tab].get("1.0", tk.END)))
        self.frame.pack(fill="both", expand=True)

    def updateFrame(self, text: str) -> None:
        self.frame.load_html(markdown(text))

    def key_bind(self, keys: str, func) -> None:
        self.preview_window.bind(keys, func)

"""
Window Settings
"""
# Create the window
root = tk.Tk()
pref_window = PreferenceWindow(close=True)
preview_window = PreviewWindow(close=True)

# Rename the window
root.title("Encryptext")
# Resize the window (manually resizable too)
root.geometry("800x500")
# Change the icon
root.iconbitmap(getTrueFilename("app_icon.ico"))

"""
Variables
"""
update_file_title = " DO NOT SAVE THIS FILE "

file_save_locations = []
file_extensions = []

default_font_size = 11
default_font_type = "Arial"
max_font_size = 96
min_font_size = 8
font_sizes = []
font_type = []

button_style = ttk.Style()
button_style.configure("TButton", font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
notebook_style = ttk.Style()
notebook_style.configure("TNotebook", tabposition="nw", padding=5)
notebook_tab_style = ttk.Style()
notebook_tab_style.configure("TNotebook.Tab", font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))), expand=-1)
radio_button_style = ttk.Style()
radio_button_style.configure("TRadiobutton", font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
check_button_style = ttk.Style()
check_button_style.configure("TCheckbutton", font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))

recent_files = settings["recentFilePaths"]

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

saved = []
prev_key = ""

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
    global settings

    current_tab = getCurrentTab()
    if current_tab == -1:
        # Save any settings changes
        settings["recentFilePaths"] = recent_files
        try:
            with open(settings_path, "w") as file:
                settings = str(settings).replace("'", '"').replace("False", "false").replace("True", "true")
                file.write(str(settings))
        except FileNotFoundError: pass

        try:
            md_preview_window.destroy()
            pref_window.closeWindow()
        finally:
            root.destroy()
            sys.exit()

    # Check if any of the tabs are not saved yet
    quit_confirm = True
    for save_status in saved:
        if save_status == False:
            quit_confirm = False

    # If there's one that's not empty, then show warning
    if not quit_confirm:
        quit_confirm = messagebox.askyesno("Quit", "Quit Encryptext?\n\nAny unsaved changes will be lost.")

    if quit_confirm:
        # Save any settings changes
        settings["recentFilePaths"] = recent_files
        try:
            with open(settings_path, "w") as file:
                settings = str(settings).replace("'", '"').replace("False", "false").replace("True", "true")
                file.write(str(settings))
        except FileNotFoundError: pass

        try:
            md_preview_window.destroy()
            pref_window.closeWindow()
        finally:
            root.destroy()
            sys.exit()

def openFile(Event=None, current=False, file_path=None):
    # Make save_location global to change it for the whole program
    global file_save_locations, file_format_tags, file_histories, current_versions, file_format_tag_nums, file_extensions

    current_tab = getCurrentTab()
    if current_tab == -1:
        addNewTab()

    # Check if the current textbox is empty
    if len(textboxes[current_tab].get("1.0", tk.END)) > 2 and textboxes[current_tab].get("1.0", tk.END) != "\n\n" and not current and saved[current_tab] == False:
        open_file_confirm = messagebox.askyesno("Open File", "Open a file?\n\nAny unsaved changes will be lost.")
    else:
        open_file_confirm = True

    if open_file_confirm:
        # Show a file selector and let user choose file
        save_location = file_save_locations[current_tab]
        if file_path != None:
            save_location = file_path
        elif not current:
            save_location = filedialog.askopenfilename(title="Select file", filetypes=supported_file_types)

        if save_location != "":
            # Open the file and read its contents into an array
            try:
                file = open(save_location, "r")
            except FileNotFoundError:
                messagebox.showerror("Error Opening File", f"File not found.\nThe file that you tried to open doesn't exist!")
                return None

            # Don't change the file save location before confirming
            file_save_locations[current_tab] = save_location

            # Reset tag number
            file_format_tag_nums[current_tab] = 0

            # Get the file exntension
            file_extensions[current_tab] = file_save_locations[current_tab].split(".")[-1]
            # Get file name
            file_name = file_save_locations[current_tab].split("/")[-1]

            # Set the title of the window to the file name
            tab_panes.tab(tab_panes.tabs()[getCurrentTab()], text=f" {file_name} ")

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
                    file_format_tags[current_tab] = []
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

                    # Set save status to True
                    setSaveStatus(True, current_tab)

                    # Change recent files list
                    if save_location in recent_files:
                        recent_files.pop(recent_files.index(save_location))
                        recent_files.insert(0, save_location)
                    else:
                        recent_files.insert(0, save_location)
                        # Check that there's only the set number of file paths stored
                        if len(recent_files) > settings["maxRecentFiles"]:
                            recent_files.pop()
                    createMenuBar()
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

                # Set save status to True
                setSaveStatus(True, current_tab)

                # Change recent files list
                if save_location in recent_files:
                    recent_files.pop(recent_files.index(save_location))
                    recent_files.insert(0, save_location)
                else:
                    recent_files.insert(0, save_location)
                    # Check that there's only the set number of file paths stored
                    if len(recent_files) > settings["maxRecentFiles"]:
                        recent_files.pop()
                createMenuBar()
            if file_extensions[current_tab] == "md":
                global md_preview_window
                try:
                    md_preview_window.deiconify()
                    updatePreview()
                except:
                    preview_window.__init__()
        else:
            text = textboxes[current_tab].get("1.0", tk.END)
            textboxes[current_tab].delete("1.0", tk.END)
            textboxes[current_tab].insert(tk.END, text[:-2])
            for i in range(len(file_format_tags[current_tab])):
                format = file_format_tags[current_tab][i]
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

def newFile(Event=None):
    global file_save_locations, file_histories, current_versions

    current_tab = getCurrentTab()
    if current_tab == -1:
        addNewTab()

    # Check if the current textbox is empty
    confirmed = False
    if saved[current_tab] == False:
        new_file_confirm = messagebox.askyesno("New File", "Create new file?\n\nAny unsaved changes will be lost.")
        if new_file_confirm:
            confirmed = True
    else:
        confirmed = True

    if confirmed:
        file_save_locations[current_tab] = ""
        textboxes[current_tab].config(state=tk.NORMAL)
        textboxes[current_tab].delete("1.0", tk.END)

        file_histories[current_tab] = ["", "", ""]
        current_versions[current_tab] = 1
        setSaveStatus(True, current_tab)

        tab_panes.tab(tab_panes.tabs()[getCurrentTab()], text=" Untitled ")

        updatePreview()

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

        # Set save status to True
        setSaveStatus(True, current_tab)

        trackChanges(override=True)

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

        setSaveStatus(False, current_tab)

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

        setSaveStatus(False, current_tab)

def updatePreview(Event=None, override=False):
    current_tab = getCurrentTab()
    if current_tab == -1:
        try:
            preview_window.updateFrame("")
        except:
            return None
    else:
        try:
            # Update the preview
            preview_window.updateFrame(textboxes[current_tab].get("1.0", tk.END))
        except:
            # Only update it if it's markdown or none
            if file_extensions[current_tab] == "md" and not override:
                # If the preview window was opened manually
                preview_window.__init__()

def trackChanges(Event=None, override=False):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    # Set save status to False if it's been changed
    key_ignore = ["Control_L", "Control_R", "Alt_L", "Alt_R", "Shift_L", "Shift_R"]
    try:
        if (Event.state <= 1 and Event.keysym not in key_ignore):
            setSaveStatus(False, current_tab)
    except: pass

    try:
        if (Event.keysym in ["space", "Return", "quoteleft", "asciitilde", "exclam", "at", "numbersign", "dollar", "percent", "asciicircum", "ampersand", "asterisk", "parenleft", "parenright", "underscore", "plus", "braceleft", "braceright", "bar", "colon", "less", "greater", "question", "minus", "equal", "bracketleft", "bracketright", "backslash", "semicolon", "quoteright", "comma", "period", "slash", "Tab"]) or (override):
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
    except: pass

    # Update the preview
    updatePreview(override=True)

def cut(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    textboxes[current_tab].event_generate("<<Cut>>")

    setSaveStatus(False, current_tab)

def copy(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    textboxes[current_tab].event_generate("<<Copy>>")

    setSaveStatus(False, current_tab)

def paste(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    textboxes[current_tab].event_generate("<<Paste>>")

    setSaveStatus(False, current_tab)

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
    preview_window.__init__()

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
    pref_window.__init__()

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

    setSaveStatus(False, current_tab)

    return "break"

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

    setSaveStatus(False, current_tab)

    return "break"

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

    setSaveStatus(False, current_tab)

    return "break"

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

    setSaveStatus(False, current_tab)

    return "break"

def increaseFont(Event=None):
    global file_format_tag_nums, font_sizes

    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    if font_sizes[current_tab] >= max_font_size:
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

            setSaveStatus(False, current_tab)
        except: pass

    return "break"

def decreaseFont(Event=None):
    global file_format_tag_nums, font_sizes

    current_tab = getCurrentTab()
    if current_tab == -1:
        return None

    if font_sizes[current_tab] <= min_font_size:
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

            setSaveStatus(False, current_tab)
        except: pass

    return "break"

def showQuickMenu(Event=None):
    try:
        rightclickmenu.tk_popup(Event.x_root, Event.y_root)
    finally:
        rightclickmenu.grab_release()

def addNewTab(Event=None):
    # Create new textbox
    if settings["otherSettings"]["wrapLines"] == True:
        wrap_mode = "word"
    else:
        wrap_mode = "none"
    textboxes.append(tk.Text(tab_panes, state=tk.NORMAL, font=(default_font_type, default_font_size, "normal"), cursor="xterm", wrap=wrap_mode))

    # Create new tab info slot in arrays
    file_save_locations.append("")
    file_extensions.append("")
    file_histories.append(["", "", ""])
    current_versions.append(1)
    file_format_tags.append([])
    file_format_tag_nums.append(0)
    font_sizes.append(default_font_size)
    font_type.append(default_font_type)
    saved.append(True)

    # Create scroll bar and link it
    scroll_bars = []
    scroll_bars.append([tk.Scrollbar(textboxes[-1], orient=tk.VERTICAL, cursor="arrow")])
    scroll_bars[-1][0].config(command=textboxes[-1].yview)
    textboxes[-1].config(yscrollcommand=scroll_bars[-1][0].set)

    if settings["otherSettings"]["wrapLines"] == False:
        scroll_bars[-1].append(tk.Scrollbar(textboxes[-1], orient=tk.HORIZONTAL, cursor="arrow"))
        scroll_bars[-1][1].config(command=textboxes[-1].xview)
        textboxes[-1].config(xscrollcommand=scroll_bars[-1][1].set)

    # Add to display
    textboxes[-1].pack(side=tk.TOP, fill=tk.BOTH)
    scroll_bars[-1][0].pack(side=tk.RIGHT, fill=tk.Y)

    if settings["otherSettings"]["wrapLines"] == False:
        scroll_bars[-1][1].pack(side=tk.BOTTOM, fill=tk.X)

    tab_panes.add(textboxes[-1], text=" Untitled ")

    # Allow right-click menu to show up
    textboxes[-1].bind("<Button-3>", showQuickMenu)

    # Fix Ctrl+T switching last char in textbox
    # https://stackoverflow.com/a/54185644
    bindtags = textboxes[-1].bindtags()
    textboxes[-1].bindtags((bindtags[2], bindtags[0], bindtags[1], bindtags[3]))

    # Track document changes and update markdown preview
    textboxes[-1].bind('<Key>', trackChanges)

    # Sets the tab focus to the newly created tab
    tab_panes.select(tab_panes.tabs()[-1])
    textboxes[-1].focus()

    updatePreview()

    return "break"

def closeCurrentTab(Event=None):
    current_tab = getCurrentTab()
    if current_tab == -1:
        quitApp()

    # If their settings are configured to close all tabs
    if settings["otherSettings"]["closeAllTabs"] == True:
        quitApp()
        return None

    close_tab_confirm = True
    if saved[current_tab] == False:
        close_tab_confirm = False

    if not close_tab_confirm:
        close_tab_confirm = messagebox.askyesno("Close Tab", "Close current tab?\n\nAny unsaved changes will be lost.")

    if close_tab_confirm:
        # Remove any tab info from arrays
        tab_panes.forget(current_tab)
        textboxes.pop(current_tab)
        file_save_locations.pop(current_tab)
        file_extensions.pop(current_tab)
        file_histories.pop(current_tab)
        current_versions.pop(current_tab)
        file_format_tags.pop(current_tab)
        file_format_tag_nums.pop(current_tab)
        saved.pop(current_tab)

    updatePreview()

def getCurrentTab() -> int:
    try:
        return tab_panes.index("current")
    except: # Returns -1 if there are no tabs
        return -1

def setSaveStatus(save: bool, current_tab: int) -> None:
    saved[current_tab] = save
    cur_tab_id = tab_panes.tabs()[current_tab]
    tab_title = tab_panes.tab(cur_tab_id)["text"]
    if not save:
        if "*" not in tab_title:
            tab_panes.tab(cur_tab_id, text=f"{tab_panes.tab(cur_tab_id)['text']}*")
    else:
        if "*" in tab_title:
            tab_panes.tab(cur_tab_id, text=tab_panes.tab(cur_tab_id)['text'].split("*")[0])

def captureSpecialKeys(Event=None):
    cur_key = Event.keysym
    mod_key = Event.state

    # Run function based on what key was pressed
    if cur_key == "s":
        saveFile()
    elif cur_key == "S":
        saveFileAs()
    elif cur_key == "n" and mod_key == 4:
        newFile()
    elif cur_key == "o":
        openFile()
    elif cur_key == "e" and mod_key == 131072:
        editingMode()
    elif cur_key == "v" and mod_key == 131072:
        viewingMode()
    elif cur_key == "t":
        addNewTab()
    elif cur_key == "w":
        closeCurrentTab()
    elif cur_key == "z":
        undo()
    elif cur_key == "Z":
        redo()
    elif cur_key == "A":
        deselectAll()
    elif cur_key == "p":
        openPreview()
    elif cur_key == "P":
        preview_window.closeWindow()
    elif cur_key == "+":
        increaseFont()
    elif cur_key == "_":
        decreaseFont()
    elif cur_key == "i":
        changeToItalic()
    elif cur_key == "b":
        changeToBold()
    elif cur_key == "n":
        changeToNormal()

    return "break"

"""
Window Items
"""
tab_panes = ttk.Notebook(root, cursor="hand2")
tab_panes.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
tab_panes.enable_traversal()
tab_panes.bind("<<NotebookTabChanged>>", updatePreview) # https://stackoverflow.com/a/44092163

# Create the first tab
addNewTab()

# To make it more seamless
# The preview window was the focused one before
root.focus_force()

"""
Menu Bar
"""
# Binding all Ctrl and Alt keys to run custom function first
root.bind("<Control-Key>", captureSpecialKeys)
root.bind("<Alt-Key>", captureSpecialKeys)

def createMenuBar():
    # Top bar menu
    menubar = tk.Menu(root, tearoff=False, font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))

    # Menu items
    filemenu = tk.Menu(menubar, tearoff=False, font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
    recentfilemenu = tk.Menu(filemenu, tearoff=False, font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
    editmenu = tk.Menu(menubar, tearoff=False, font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
    formatmenu = tk.Menu(menubar, tearoff=False, font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
    textfontmenu = tk.Menu(formatmenu, tearoff=False, font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
    textsizemenu = tk.Menu(formatmenu, tearoff=False, font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
    textstylemenu = tk.Menu(formatmenu, tearoff=False, font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))
    helpmenu = tk.Menu(menubar, tearoff=False, font=(settings["otherSettings"]["fontStyle"], int(round(11*font_scale_factor))))

    # File menu items
    filemenu.add_command(label="New File", accelerator="Ctrl+N", command=newFile)
    filemenu.add_command(label="Open File", accelerator="Ctrl+O", command=openFile)

    # Create buttons for every recent file path stored
    for i in recent_files:
        # From: https://stackoverflow.com/a/10865170
        recentfilemenu.add_command(label=i, command=lambda i=i: openFile(file_path=i))

    if len(recent_files) == 0:
        state = "disabled"
    else:
        state = "enabled"
    filemenu.add_cascade(label="Open Recent", menu=recentfilemenu, state=state)
    filemenu.add_command(label="View File", command=viewFile)
    filemenu.add_separator()
    filemenu.add_command(label="Save", accelerator="Ctrl+S", command=saveFile)
    filemenu.add_command(label="Save As", command=saveFileAs)
    filemenu.add_separator()
    filemenu.add_command(label="Edit Mode", accelerator="Alt+E", command=editingMode)
    filemenu.add_command(label="View Mode", accelerator="Alt+V", command=viewingMode)
    filemenu.add_separator()
    filemenu.add_command(label="New Tab", accelerator="Ctrl+T", command=addNewTab)
    filemenu.add_command(label="Close Tab", accelerator="Ctrl+W", command=closeCurrentTab)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=quitApp)

    # Edit menu items
    editmenu.add_command(label="Undo", accelerator="Ctrl+Z", command=undo)
    editmenu.add_command(label="Redo", accelerator="Ctrl+Shift+Z", command=redo)
    editmenu.add_separator()
    editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=cut)
    editmenu.add_command(label="Copy", accelerator="Ctrl+C", command=copy)
    editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=paste)
    editmenu.add_separator()
    editmenu.add_command(label="Select All", accelerator="Ctrl+A", command=selectAll)
    editmenu.add_command(label="Deselect All", accelerator="Ctrl+Shift+A", command=deselectAll)
    editmenu.add_separator()
    editmenu.add_command(label="Open Markdown Preview", accelerator="Ctrl+P", command=openPreview)
    editmenu.add_command(label="Close Markdown Preview", accelerator="Ctrl+Shift+P", command=preview_window.closeWindow)
    editmenu.add_command(label="Update Markdown Preview", accelerator="Ctrl+E", command=updatePreview)
    editmenu.add_separator()
    editmenu.add_command(label="Edit Preferences", command=openPreferences)

    # Format menu items
    formatmenu.add_command(label="Text Colour", command=changeTextColour)

    textfontmenu.add_command(label="Arial")

    textsizemenu.add_command(label="Increase Font Size", accelerator="Ctrl+Shift++", command=increaseFont)
    textsizemenu.add_command(label="Decrease Font Size", accelerator="Ctrl+Shift+-", command=decreaseFont)

    textstylemenu.add_command(label="Normal", accelerator="Alt+N", command=changeToNormal)
    textstylemenu.add_command(label="Bold", accelerator="Ctrl+B", command=changeToBold)
    textstylemenu.add_command(label="Italic", accelerator="Ctrl+I", command=changeToItalic)

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

createMenuBar()

# Quick menu
rightclickmenu = tk.Menu(root, tearoff=False)

rightclickmenu.add_command(label="Cut", command=cut)
rightclickmenu.add_command(label="Copy", command=copy)
rightclickmenu.add_command(label="Paste", command=paste)
rightclickmenu.add_separator()
rightclickmenu.add_command(label="Undo", command=undo)
rightclickmenu.add_command(label="Redo", command=redo)
rightclickmenu.add_separator()
rightclickmenu.add_command(label="Text Colour", command=changeTextColour)
rightclickmenu.add_command(label="Normal", command=changeToNormal)
rightclickmenu.add_command(label="Bold", command=changeToBold)
rightclickmenu.add_command(label="Italic", command=changeToItalic)
rightclickmenu.add_separator()
rightclickmenu.add_command(label="Open Preview", command=openPreview)
rightclickmenu.add_command(label="Close Preview", command=preview_window.closeWindow)
rightclickmenu.add_command(label="Update Preview", command=updatePreview)

"""
Window Display
"""
# When closing the app, run the quit_app function
root.protocol("WM_DELETE_WINDOW", quitApp)

# Display the window
root.mainloop()
