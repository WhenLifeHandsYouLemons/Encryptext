from tkinter import *
# from tkinter.filedialog import askopenfilename
# from tkinter.filedialog import asksaveasfilename
# from tkinter.messagebox import askyesno
# from tkinter.messagebox import showerror
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
import webbrowser
from cryptography.fernet import Fernet

# text.config(font="Helvetica")

# The first line is first_time_opening_app, second is encryption_key, third is debug_mode
settings = []
with open("C:/Users/User/Documents/GitHub/Encryptext/Settings.txt", "r") as f:
    content = f.read()
    lines = content.splitlines()
    for line in lines:
        settings.append(line)

first_time_opening_app = settings[0]
encryption_key = settings[1]
debug_mode = settings[2]

if first_time_opening_app == "True":
    print("\nFirst time, eh?")
    # time.sleep(2)
    # print("\nDon't worry, I'll set up a few things before you can get started.")
    # time.sleep(4)
    # print("\nThis will only happen the first time you open this program.")
    # time.sleep(3)
    # print("\nHelpful hint: If you lose this .exe file, then you basically lose access to all your files because they are encrpyted automatically.")
    # time.sleep(10)
    # print("\nAlmost done!")
    # Generates a key to encodes the file
    key = Fernet.generate_key()
    key = key.decode("utf-8")
    if debug_mode == "On":
        print(key)
        print(settings)
    settings.pop(1)
    settings.pop(0)
    settings.insert(0, f"{key}")
    settings.insert(0, "False")
else:
    print("\nWelcome back.")
    key = encryption_key

# This initialises the key to encode and decode
fernet = Fernet(key)

save_location = ""
font_size = 11
font_type = "Arial"
max_font_size = 400
min_font_size = 6
used_tags = []
formatting = []
format_start_string = "H6ETuTu9od"

supported_file_types = [("Custom Text Editor Interface Edition Files", "*.cteie"),
                        ("Text Document", "*.txt"),
                        ("Python Files", "*.py"),
                        ("HTML Files", "*.html"),
                        ("Cascading Style Sheets Files", "*.css"),
                        ("MD Files", "*.md"),
                        ("All Files", "*.*")]

root = Tk("Text Editor")

title = StringVar()
title.set("")
textbox = Text(root, state=NORMAL, font=(font_type, font_size, "normal"))
textbox.pack(side=BOTTOM, fill=BOTH, expand=1)

def save_with_format(Event=None):
    print()


root.mainloop()