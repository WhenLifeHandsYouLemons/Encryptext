from tkinter import *
# from tkinter.filedialog import askopenfilename
# from tkinter.filedialog import asksaveasfilename
# from tkinter.messagebox import askyesno
# from tkinter.messagebox import showerror
from tkinter import filedialog
from tkinter import messagebox

save_location = ""

root = Tk("Text Editor")

title_of_file = Label(text="Untitled", font=("Arial", 15, "bold"))
title_of_file.pack(side=TOP, fill=X)

text = Text(root)
text.pack(side=LEFT, fill=BOTH)

scroll_bar = Scrollbar(root)
scroll_bar.pack(side=RIGHT, fill=Y)
scroll_bar.config(command=text.yview)

text.config(yscrollcommand=scroll_bar.set)

root.wm_title("Untitled")

def get_file_name():
    separated_location = save_location.split("/")
    separated_file_name = separated_location[-1].split(".")
    file_name = separated_file_name = [0]
    title_of_file = Label(text=file_name, font=("Arial", 15, "bold"))

def quit_app(Event=None):
    confirm_exit_box = messagebox.askyesno("Quit","Any unsaved changes will be lost forever.\nClicking 'No' will automatically save the file before exiting the editor.")
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

def save_file(Event=None):
    global text
    if save_location != "":
        text_to_save = text.get("1.0", "end-1c")
        file1 = open(save_location, "w+")
        file1.write(text_to_save)
        file1.close()
    else:
        # messagebox.showinfo("Error: Save location not initialised","Please use the Save As function to save the file for the first time.\nOnce you use the Save As function for this file, you will not need to use the Save As function for this file.")
        save_as_file()

def save_as_file(Event=None):
    global text
    text_to_save_as = text.get("1.0", "end-1c")
    files = [("Text Document", "*.txt"),
             ("Python Files", "*.py"),
             ("HTML Files", "*.html"),
             ("Cascading Style Sheets Files", "*.css"),
             ("Custom Text Editor Window Edition Files", "*.ctewe"),
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
        if save_location:
            infile = open(save_location,"r")
            text.delete("1.0",END)
            for line in infile:
                text.insert(END,line)
            infile.close()
    except Exception as e:
        messagebox.showerror("Exception",e)

def new_file(Event=None):
    global save_location
    save_location = ""
    text.delete("1.0",END)
    print("")

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", accelerator="Ctrl+N", command=new_file)
root.bind_all("<Control-n>", new_file)
filemenu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
root.bind_all("<Control-s>", save_file)
filemenu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
root.bind_all("<Control-o>", open_file)
filemenu.add_command(label="Save As", accelerator="Alt+S", command=save_as_file)
root.bind_all("<Alt-s>", save_as_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", accelerator="Ctrl+W", command=quit_app)
root.bind_all("<Control-w>", quit_app)
menubar.add_cascade(label="File", menu=filemenu)

optionmenu = Menu(menubar, tearoff=0)
optionmenu.add_command(label="Copy",  accelerator="Ctrl+C")
optionmenu.add_command(label="Paste", accelerator="Ctrl+V")
menubar.add_cascade(label="Options", menu=optionmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Documentation")
helpmenu.add_command(label="About")
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

root.mainloop()