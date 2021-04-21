"""
Made By - Sooraj Sannabhadti
GitHub - https://github.com/WhenLifeHandsYouLemons
Twitter - https://twitter.com/LemonsHandYou
Instagram - https://www.instagram.com/whenlifehandsyoulemons1/
Latest Release - https://github.com/WhenLifeHandsYouLemons/Custom-Text-Editor/releases
"""
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
import time

# text.config(font="Helvetica")

settings = []
with open("C:/Users/2005s/Documents/Visual Studio Code/Python/Tkinter/Custom-Text-Editor/Settings.txt", "r") as f:
    content = f.read()
    lines = content.splitlines()
    for line in lines:
        settings.append(line)

first_time_opening_app = settings[0]
encryption_key = settings[1]

if first_time_opening_app == "firstTimeOpeningApp=True":
    print("\nFirst time, eh?")
    # time.sleep(2)
    # print("\nDon't worry, I'll set up a few things before you can get started.")
    # time.sleep(4)
    # print("\nThis will only happen the first time you open this program.")
    # time.sleep(3)
    # print("\nHelpful hint: If you lose this .exe file, then you basically lose access to all your files because they are encrpyted automatically.")
    # time.sleep(10)
    # print("\nAnd the encryption key is stored somewhere that only this exact program will know where to find it.")
    # time.sleep(8)
    # print("\nTry not to lose it on the first day, yeah?")
    # time.sleep(1)
    # print("\nAlmost done!")
    key = Fernet.generate_key()
    key = key.decode("utf-8")
    settings.pop(1)
    settings.pop(0)
    settings.insert(0, key)
    settings.insert(0, "firstTimeOpeningApp=False")
    time.sleep(5)
else:
    print("\nAh, welcome back.")
    key = encryption_key
    time.sleep(2)

fernet = Fernet(key)

save_location = ""
font_size = 11
font_type = "Arial"
max_font_size = 100
min_font_size = 3
used_tags = []
formatting = []
format_start_string = "H6ETuTu9od"

root = Tk("Text Editor")
if settings[2] == "debugMode=On":
    debug = Tk("Debug Windows")
    debug.grid()
    undostate0 = Text(debug, state=NORMAL, font=(font_type, font_size, "normal"))
    undostate1 = Text(debug, state=NORMAL, font=(font_type, font_size, "normal"))
    redostate0 = Text(debug, state=NORMAL, font=(font_type, font_size, "normal"))
    redostate1 = Text(debug, state=NORMAL, font=(font_type, font_size, "normal"))
    undostate0.grid(row=0, column=0)
    undostate1.grid(row=0, column=1)
    redostate0.grid(row=1, column=0)
    redostate1.grid(row=1, column=1)
else:
    undostate0 = Text(root, state=NORMAL, font=(font_type, font_size, "normal"))
    undostate1 = Text(root, state=NORMAL, font=(font_type, font_size, "normal"))
    redostate0 = Text(root, state=NORMAL, font=(font_type, font_size, "normal"))
    redostate1 = Text(root, state=NORMAL, font=(font_type, font_size, "normal"))

root.geometry("500x500")
root.wm_title("Custom Text Editor Interface Edition")

title = StringVar()
title.set("")
title_of_file = Label(textvariable=title, font=("Arial", 15, "bold"))
title_of_file.pack(side=TOP, fill=X)

textbox = Text(root, state=NORMAL, font=(font_type, font_size, "normal"))

scroll_bar_vertical = Scrollbar(root, orient=VERTICAL)
scroll_bar_vertical.pack(side=RIGHT, fill=Y)
scroll_bar_vertical.config(command=textbox.yview)

textbox.config(yscrollcommand=scroll_bar_vertical.set)
textbox.pack(side=BOTTOM, fill=BOTH, expand=1)

def get_file_name(Event=None):
    if save_location != "":
        separated_location = save_location.split("/")
        separated_file_name = separated_location[-1].split(".")
        file_name = separated_file_name[0]
        title.set(file_name)
    else:
        title.set("Untitled")

get_file_name()

def quit_app(Event=None):
    save = "\n".join(settings)
    with open("C:/Users/2005s/Documents/Visual Studio Code/Python/Tkinter/Custom-Text-Editor/Settings.txt", "w") as f:
        f.write(save)
    if len(textbox.get("1.0", END)) != 1:
        confirm_exit_box = messagebox.askyesno("Quit Program","Are you sure you want to quit? Any unsaved changes will be lost forever.\n\nClicking 'No' will automatically save the file before exiting the editor.\nClicking 'Yes' will close the editor without saving.")
        if confirm_exit_box == 1:
            root.quit()
        else:
            if save_location == "":
                save_as_file()
                if save_location == "":
                    return
                else:
                    root.quit()
            else:
                save_file()
                root.quit()
    else:
        root.quit()

def save_file(Event=None):
    global textbox
    if save_location != "":
        text_to_save = textbox.get("1.0", END)
        file1 = open(save_location, "w+")
        file1.write(text_to_save)
        file1.close()
    else:
        # messagebox.showerror("Error: Save location not initialised","Please use the Save As function to save the file for the first time.\nOnce you use the Save As function for this file, you will not need to use the Save As function for this file.")
        save_as_file()
    print("File saved.")

def save_as_file(Event=None):
    global textbox
    text_to_save_as = textbox.get("1.0", END)
    files = [("Custom Text Editor Interface Edition Files", "*.cteie"),
             ("Text Document", "*.txt"),
             ("Python Files", "*.py"),
             ("HTML Files", "*.html"),
             ("Cascading Style Sheets Files", "*.css"),
             ("All Files", "*.*")]
    global save_location
    save_location = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
    if save_location != "":
        file1 = open(save_location, "w+")
        # encrypted_text_to_save_as = fernet.encrypt(text_to_save_as.encode())
        file1.write(text_to_save_as)
        file1.close()

def open_file(Event=None):
    try:
        global save_location
        files = [("Custom Text Editor Interface Edition Files", "*.cteie"),
                 ("Text Document", "*.txt"),
                 ("Python Files", "*.py"),
                 ("HTML Files", "*.html"),
                 ("Cascading Style Sheets Files", "*.css"),
                 ("All Files", "*.*")]
        save_location = filedialog.askopenfilename(title="Select file",filetypes=files)
        if save_location != "":
            infile = open(save_location,"r")
            textbox.config(state=NORMAL)
            textbox.delete("1.0",END)
            for line in infile:
                textbox.insert(END,line)
            infile.close()
        get_file_name()
        print("Opened file for editing.")
    except Exception:
        messagebox.showerror("Error Opening File", "File format is not supported.")

def new_file(Event=None):
    if len(textbox.get("1.0", END)) != 1:
        confirm_exit_box = messagebox.askyesno("New File","Any unsaved changes will be lost forever.\nClicking 'No' will automatically save the file before exiting the editor.")
    global save_location
    save_location = ""
    textbox.config(state=NORMAL)
    textbox.delete("1.0",END)
    print("Created new file.")
    get_file_name()

def view_file(Event=None):
    try:
        global save_location
        save_location = filedialog.askopenfilename(title = "Select file",filetypes = (("All Files","*.*"),("Text Files","*.txt"),("Python Files","*.py")))
        if save_location != "":
            infile = open(save_location,"r")
            textbox.config(state=NORMAL)
            textbox.delete("1.0",END)
            for line in infile:
                textbox.insert(END,line)
            infile.close()
            textbox.config(state=DISABLED)
        get_file_name()
        print("Opened file for viewing.")
    except Exception as e:
        messagebox.showerror("Exception",e)

def edit_mode(Event=None):
    textbox.config(state=NORMAL)

def view_mode(Event=None):
    textbox.config(state=DISABLED)

def increase_font(Event=None):
    global font_size
    if font_size == max_font_size:
        messagebox.showerror("Error", "Font size cannot go higher than 100. Please change the max_font_size variable to increase the limit.")
    else:
        font_size = font_size + 1
        textbox.config(font=(font_type, font_size))

    # textbox.tag_add("start", "1.0", END)
    # textbox.tag_config("start", background="lime green", font=("Helvetica", 50, "italic"))

def decrease_font(Event=None):
    global font_size
    if font_size == min_font_size:
        messagebox.showerror("Error", "Font size cannot go lower than 3. Please change the min_font_size variable to decrease the limit.")
    else:
        font_size = font_size - 1
        textbox.config(font=(font_type, font_size))

def specific_size_font(Event=None):
    print()

def change_text_colour():
    colour_code = colorchooser.askcolor(title ="Choose a colour")
    colour_code = colour_code[-1]
    start_selection = textbox.index("sel.first")
    end_selection = textbox.index("sel.last")
    not_valid = True
    i = 0
    while not_valid == True:
        if len(used_tags) == 0:
            not_valid = False
        elif used_tags[-1] >= i:
            i = i + 1
        else:
            not_valid = False
    current_tag = f"selection{i}"
    textbox.tag_add(current_tag, start_selection, end_selection)
    textbox.tag_config(current_tag, foreground=colour_code)
    used_tags.append(i)

def documentation(Event=None):
    webbrowser.open_new("https://github.com/WhenLifeHandsYouLemons/Custom-Text-Editor/wiki/Documentation")

def about_menu(Event=None):
    messagebox.showinfo("About Custom Text Editor Interface Edition","A custom text editor made for a fun side project. Comes with a terminal version and an encryptor which adds an extra layer of security by asking for a password before showing the text editor.\n\nCreated by Sooraj.S")

def copy_event(Event=None):
    textbox.event_generate("<<Copy>>")

def paste_event(Event=None):
    textbox.event_generate("<<Paste>>")

def cut_event(Event=None):
    textbox.event_generate("<<Cut>>")

def track_changes(Event=None):
    get_current_text = undostate0.get("1.0", END)
    undostate1.delete("1.0", END)
    total_lines = 0
    for line in get_current_text:
        total_lines = total_lines + 1
    current_line = 0
    for line in get_current_text:
        undostate1.insert(END,line)
        current_line = current_line + 1
        if current_line == total_lines - 1:
            print("Skipped a line!")
            break
    # undostate1.insert(END, get_current_text)

    get_current_text = textbox.get("1.0", END)
    undostate0.delete("1.0", END)
    total_lines = 0
    for line in get_current_text:
        total_lines = total_lines + 1
    current_line = 0
    for line in get_current_text:
        undostate0.insert(END,line)
        current_line = current_line + 1
        if current_line == total_lines - 1:
            print("Skipped a line!")
            break
    # undostate0.insert(END, get_current_text)

    redostate0.delete("1.0", END)
    redostate1.delete("1.0", END)
    print("Change to document has been tracked.")
    print(undostate1.get("1.0", END))

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

def undo_event(Event=None):
    lists = []
    lists.append(textbox.get("1.0", END))
    print(lists)
    get_current_text = redostate0.get("1.0", END)
    redostate1.delete("1.0", END)
    total_lines = 0
    for line in get_current_text:
        total_lines = total_lines + 1
    current_line = 0
    for line in get_current_text:
        redostate1.insert(END, line)
        current_line = current_line + 1
        if current_line == total_lines - 1:
            print("Skipped a line!")
            break
    # redostate1.insert(END, get_current_text)

    get_current_text = textbox.get("1.0", END)
    redostate0.delete("1.0", END)
    total_lines = 0
    for line in get_current_text:
        total_lines = total_lines + 1
    current_line = 0
    for line in get_current_text:
        redostate0.insert(END, line)
        current_line = current_line + 1
        if current_line == total_lines - 1:
            print("Skipped a line!")
            break
    # redostate0.insert(END, get_current_text)

    get_current_text = undostate0.get("1.0", END)
    textbox.delete("1.0", END)
    total_lines = 0
    for line in get_current_text:
        total_lines = total_lines + 1
    current_line = 0
    for line in get_current_text:
        textbox.insert(END, line)
        current_line = current_line + 1
        if current_line == total_lines - 1:
            break
    # textbox.insert(END, get_current_text)

    get_current_text = undostate1.get("1.0", END)
    undostate0.delete("1.0", END)
    total_lines = 0
    for line in get_current_text:
        total_lines = total_lines + 1
    current_line = 0
    for line in get_current_text:
        undostate0.insert(END, line)
        current_line = current_line + 1
        if current_line == total_lines - 1:
            print("Skipped a line!")
            break
    # undostate0.insert(END, get_current_text)

def redo_event(Event=None):
    get_current_text = undostate0.get("1.0", END)
    undostate1.delete("1.0", END)
    total_lines = 0
    for line in get_current_text:
        total_lines = total_lines + 1
    current_line = 0
    for line in get_current_text:
        undostate1.insert(END, line)
        current_line = current_line + 1
        if current_line == total_lines - 1:
            print("Skipped a line!")
            break
    # undostate1.insert(END, get_current_text)

    get_current_text = textbox.get("1.0", END)
    undostate0.delete("1.0", END)
    total_lines = 0
    for line in get_current_text:
        total_lines = total_lines + 1
    current_line = 0
    for line in get_current_text:
        undostate0.insert(END, line)
        current_line = current_line + 1
        if current_line == total_lines - 1:
            print("Skipped a line!")
            break
    # undostate0.insert(END, get_current_text)

    get_current_text = redostate0.get("1.0", END)
    textbox.delete("1.0", END)
    total_lines = 0
    for line in get_current_text:
        total_lines = total_lines + 1
    current_line = 0
    for line in get_current_text:
        textbox.insert(END, line)
        current_line = current_line + 1
        if current_line == total_lines - 1:
            print("Skipped a line!")
            break
    # textbox.insert(END, get_current_text)

    get_current_text = redostate1.get("1.0", END)
    redostate0.delete("1.0", END)
    total_lines = 0
    for line in get_current_text:
        total_lines = total_lines + 1
    current_line = 0
    for line in get_current_text:
        redostate0.insert(END, line)
        current_line = current_line + 1
        if current_line == total_lines - 1:
            print("Skipped a line!")
            break
    # redostate0.insert(END, get_current_text)

def select_all(Event=None):
    textbox.event_generate("<<SelectAll>>")

def deselect_all(Event=None):
    textbox.event_generate("<<SelectNone>>")

def normal_text_style(Event=None):
    start_selection = textbox.index("sel.first")
    end_selection = textbox.index("sel.last")
    not_valid = True
    i = 0
    while not_valid == True:
        if len(used_tags) == 0:
            not_valid = False
        elif used_tags[-1] >= i:
            i = i + 1
        else:
            not_valid = False
    current_tag = f"selection{i}"
    textbox.tag_add(current_tag, start_selection, end_selection)
    textbox.tag_config(current_tag, font=(font_type, font_size, "normal"))
    used_tags.append(i)

def bold_text_style(Event=None):
    start_selection = textbox.index("sel.first")
    end_selection = textbox.index("sel.last")
    not_valid = True
    i = 0
    while not_valid == True:
        if len(used_tags) == 0:
            not_valid = False
        elif used_tags[-1] >= i:
            i = i + 1
        else:
            not_valid = False
    current_tag = f"selection{i}"
    textbox.tag_add(current_tag, start_selection, end_selection)
    textbox.tag_config(current_tag, font=(font_type, font_size, "bold"))
    used_tags.append(i)

def italic_text_style(Event=None):
    start_selection = textbox.index("sel.first")
    end_selection = textbox.index("sel.last")
    not_valid = True
    i = 0
    while not_valid == True:
        if len(used_tags) == 0:
            not_valid = False
        elif used_tags[-1] >= i:
            i = i + 1
        else:
            not_valid = False
    current_tag = f"selection{i}"
    textbox.tag_add(current_tag, start_selection, end_selection)
    textbox.tag_config(current_tag, font=(font_type, font_size, "italic"))
    used_tags.append(i)

def save_with_format(Event=None):
    print()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New File", accelerator="Ctrl+N", command=new_file)
root.bind_all("<Control-n>", new_file)
filemenu.add_command(label="Open...", accelerator="Ctrl+O", command=open_file)
root.bind_all("<Control-o>", open_file)
filemenu.add_command(label="View File", command=view_file)
filemenu.add_separator()
filemenu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
root.bind_all("<Control-s>", save_file)
filemenu.add_command(label="Save As...", accelerator="Alt+S", command=save_as_file)
root.bind_all("<Alt-s>", save_as_file)
filemenu.add_separator()
filemenu.add_command(label="Edit Mode",  accelerator="Alt+E", command=edit_mode)
root.bind_all("<Alt-e>", edit_mode)
filemenu.add_command(label="View Mode", accelerator="Alt+V", command=view_mode)
root.bind_all("<Alt-v>", view_mode)
filemenu.add_separator()
filemenu.add_command(label="Exit", accelerator="Ctrl+W", command=quit_app)
root.bind_all("<Control-w>", quit_app)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", accelerator="Ctrl+Z", command=undo_event)
root.bind_all("<Control-z>", undo_event)
editmenu.add_command(label="Redo", accelerator="Ctrl+Y", command=redo_event)
root.bind_all("<Control-y>", redo_event)
editmenu.add_separator()
editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=cut_event)
editmenu.add_command(label="Copy",  accelerator="Ctrl+C", command=copy_event)
editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=paste_event)
editmenu.add_separator()
editmenu.add_command(label="Select All", accelerator="Ctrl+A", command=select_all)
editmenu.add_command(label="Deselect All", accelerator="Alt+A", command=deselect_all)
root.bind_all("<Alt-a>", deselect_all)
editmenu.add_separator()
editmenu.add_command(label="Edit Preferences")
menubar.add_cascade(label="Edit", menu=editmenu)

formatmenu = Menu(menubar, tearoff=0)

textfontmenu = Menu(formatmenu, tearoff=0)
textfontmenu.add_command(label="Arial")
formatmenu.add_cascade(label="Font", menu=textfontmenu)

textsizemenu = Menu(formatmenu, tearoff=0)
textsizemenu.add_command(label="3")
textsizemenu.add_command(label="Increase Font Size", accelerator="Alt+.", command=increase_font)
root.bind_all("<Alt-.>", increase_font)
textsizemenu.add_command(label="Decrease Font Size", accelerator="Alt+,", command=decrease_font)
root.bind_all("<Alt-,>", decrease_font)
formatmenu.add_cascade(label="Text Size", menu=textsizemenu)

formatmenu.add_command(label="Text Colour", command=change_text_colour)

textstylemenu = Menu(formatmenu, tearoff=0)
textstylemenu.add_command(label="Normal", command=normal_text_style)
textstylemenu.add_command(label="Bold", accelerator= "Ctrl+B", command=bold_text_style)
root.bind_all("<Control-b>", bold_text_style)
textstylemenu.add_command(label="Italic", command=italic_text_style)
formatmenu.add_cascade(label="Text Style", menu=textstylemenu)

menubar.add_cascade(label="Format", menu=formatmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About CTEIE", command=about_menu)
helpmenu.add_command(label="Documentation", command=documentation)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

root.protocol("WM_DELETE_WINDOW", quit_app)


root.mainloop()