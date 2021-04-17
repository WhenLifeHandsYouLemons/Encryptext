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
import webbrowser


# text.config(font="Helvetica")


save_location = ""
font_size = 15
font_type = "Arial"
bold_or_not = "bold"
max_font_size = 100
min_font_size = 3

root = Tk("Text Editor")
root.geometry("500x500")
root.wm_title("Custom Text Editor Interface Edition")

title = StringVar()
title.set("")
title_of_file = Label(textvariable=title, font=(font_type, font_size, bold_or_not))
title_of_file.pack(side=TOP, fill=X)

textbox = Text(root, state=NORMAL)

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
        text_to_save = textbox.get("1.0", "end-1c")
        file1 = open(save_location, "w+")
        file1.write(text_to_save)
        file1.close()
    else:
        # messagebox.showerror("Error: Save location not initialised","Please use the Save As function to save the file for the first time.\nOnce you use the Save As function for this file, you will not need to use the Save As function for this file.")
        save_as_file()
    print("File saved.")

def save_as_file(Event=None):
    global textbox
    text_to_save_as = textbox.get("1.0", "end-1c")
    files = [("Custom Text Editor Window Edition Files", "*.ctewe"),
             ("Text Document", "*.txt"),
             ("Python Files", "*.py"),
             ("HTML Files", "*.html"),
             ("Cascading Style Sheets Files", "*.css"),
             ("All Files", "*.*")]
    global save_location
    save_location = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
    if save_location != "":
        file1 = open(save_location, "w+")
        file1.write(text_to_save_as)
        file1.close()

def open_file(Event=None):
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
        get_file_name()
        print("Opened file for editing.")
    except Exception as e:
        messagebox.showerror("Exception",e)

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
        textbox.config(font=(font_type, font_size, bold_or_not))

    textbox.tag_add("start", "2.8", END)
    textbox.tag_config("start", background="lime green", foreground="red", font=("Helvetica", 50, "bold"))

def decrease_font(Event=None):
    global font_size
    if font_size == min_font_size:
        messagebox.showerror("Error", "Font size cannot go lower than 3. Please change the min_font_size variable to decrease the limit.")
    else:
        font_size = font_size - 1
        textbox.config(font=(font_type, font_size, bold_or_not))

def documentation(Event=None):
    webbrowser.open_new("https://github.com/WhenLifeHandsYouLemons/Custom-Text-Editor/wiki/Documentation")

def about_menu(Event=None):
    messagebox.showinfo("About Custom Text Editor Windows Edition","A custom text editor made for a fun side project. Comes with a terminal version and an encryptor which adds an extra layer of security by asking for a password before showing the text editor.\n\nCreated using the Python programming language and the Tkinter module.")

def copy_event(Event=None):
    textbox.event_generate("<<Copy>>")

def paste_event(Event=None):
    textbox.event_generate("<<Paste>>")

def cut_event(Event=None):
    textbox.event_generate("<<Cut>>")

def undo_event(Event=None):
    textbox.get("", END)
    textbox.delete("1.0", END)

def redo_event(Event=None):
    textbox.event_generate("<<Redo>>")

def select_all(Event=None):
    textbox.event_generate("<<SelectAll>>")

def deselect_all(Event=None):
    textbox.event_generate("<<SelectNone>>")

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New File", accelerator="Ctrl+N", command=new_file)
root.bind_all("<Control-n>", new_file)
filemenu.add_command(label="Open...", accelerator="Ctrl+O", command=open_file)
root.bind_all("<Control-o>", open_file)
filemenu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
root.bind_all("<Control-s>", save_file)
filemenu.add_command(label="Save As...", accelerator="Alt+S", command=save_as_file)
root.bind_all("<Alt-s>", save_as_file)
filemenu.add_command(label="View", accelerator="Ctrl+Shift+V", command=view_file)
root.bind_all("<Control-Shift-v>", view_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", accelerator="Ctrl+W", command=quit_app)
root.bind_all("<Control-w>", quit_app)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", accelerator="Ctrl+Z", command=undo_event)
root.bind_all("<Control-z>", undo_event)
editmenu.add_command(label="Redo", accelerator="Ctrl+Y", command=redo_event)
root.bind_all("<Control-y>", redo_event)
editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=cut_event)
root.bind_all("<Control-x>", cut_event)
editmenu.add_command(label="Copy",  accelerator="Ctrl+C", command=copy_event)
root.bind_all("<Control-c>", copy_event)
editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=paste_event)
root.bind_all("<Control-v>", paste_event)
editmenu.add_command(label="Select All", accelerator="Ctrl+A", command=select_all)
root.bind_all("<Control-a>", select_all)
editmenu.add_command(label="Deselect All", accelerator="Ctrl+Shift+A", command=deselect_all)
root.bind_all("<Control-Shift-a>", deselect_all)
editmenu.add_separator()
editmenu.add_command(label="Edit Mode",  accelerator="Alt+E", command=edit_mode)
root.bind_all("<Alt-e>", edit_mode)
editmenu.add_command(label="View Mode", accelerator="Alt+V", command=view_mode)
root.bind_all("<Alt-v>", view_mode)
editmenu.add_separator()
editmenu.add_command(label="Change Font",  accelerator="Alt+F", command=edit_mode)
root.bind_all("<Alt-f>", edit_mode)
editmenu.add_command(label="Increase Font", accelerator="Alt+I", command=increase_font)
root.bind_all("<Alt-i>", increase_font)
editmenu.add_command(label="Decrease Font", accelerator="Alt+D", command=decrease_font)
root.bind_all("<Alt-d>", decrease_font)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Documentation", accelerator="Ctrl+Shift+D", command=documentation)
root.bind_all("<Control-Shift-d>", documentation)
helpmenu.add_command(label="About", accelerator="Ctrl+Shift+A", command=about_menu)
root.bind_all("<Control-Shift-a>", about_menu)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

root.protocol("WM_DELETE_WINDOW", quit_app)


root.mainloop()