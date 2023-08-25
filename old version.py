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
if debug_mode == "On":
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

title = StringVar()
title.set("")
title_of_file = Label(textvariable=title, font=("Arial", 15, "bold"), justify='center')
title_of_file.pack(side=TOP, fill=X)

textbox = Text(root, state=NORMAL, font=(font_type, font_size, "normal"))

scroll_bar_vertical = Scrollbar(root, orient=VERTICAL)
scroll_bar_vertical.pack(side=RIGHT, fill=Y)
scroll_bar_vertical.config(command=textbox.yview)

textbox.config(yscrollcommand=scroll_bar_vertical.set)
textbox.pack(side=BOTTOM, fill=BOTH, expand=1)

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
        encrypted_text_to_save = fernet.encrypt(text_to_save.encode())
        encrypted_text_to_save = str(encrypted_text_to_save)
        encrypted_text_to_save = encrypted_text_to_save.split("'")
        encrypted_text_to_save = encrypted_text_to_save[1]
        if debug_mode == "On":
            print(encrypted_text_to_save)
        file1.write(encrypted_text_to_save)
        file1.close()
        print("File saved.")
    else:
        save_as_file()

def save_as_file(Event=None):
    global textbox
    text_to_save_as = textbox.get("1.0", END)
    files = supported_file_types
    global save_location
    save_location = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
    if save_location != "":
        file1 = open(save_location, "w+")
        encrypted_text_to_save_as = fernet.encrypt(text_to_save_as.encode())
        encrypted_text_to_save_as = str(encrypted_text_to_save_as)
        encrypted_text_to_save_as = encrypted_text_to_save_as.split("'")
        encrypted_text_to_save_as = encrypted_text_to_save_as[1]
        if debug_mode == "On":
            print(encrypted_text_to_save_as)
        file1.write(encrypted_text_to_save_as)
        file1.close()
        print("File saved.")

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
        textbox.tag_config(current_tag, font=(font_type, font_size))
        used_tags.append(i)

    # textbox.tag_add("example_tag_name", "1.0", END)
    # textbox.tag_config("example_tag_name", background="lime green", font=("Helvetica", 50, "italic"))

def decrease_font(Event=None):
    global font_size
    if font_size == min_font_size:
        messagebox.showerror("Error", "Font size cannot go lower than 3. Please change the min_font_size variable to decrease the limit.")
    else:
        font_size = font_size - 1
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
        textbox.tag_config(current_tag, font=(font_type, font_size))
        used_tags.append(i)
        # textbox.config(font=(font_type, font_size))

def specific_size_font(Event=None):
    print()

def change_text_colour(Event=None):
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


root.protocol("WM_DELETE_WINDOW", quit_app)
root.mainloop()