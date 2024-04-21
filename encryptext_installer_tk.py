# Imports
from os import path, environ
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import platform

version = "1.9.4"

# Main window configurations
root = tk.Tk()
root.title("Setup - Encryptext")
root.iconbitmap("images/app_icon.ico")
width = 750
height = 550
root.geometry(f"{width}x{height}")  # You can set this to the desired size
root.resizable(False, False)


def swapPage(cur_page: int, next_page: int) -> None:
    """
    Swaps the current page with the next page in the GUI.

    Parameters:
    cur_page (int): The index of the current page.
    next_page (int): The index of the next page.

    Returns:
    None
    """
    pages[cur_page].destroy()
    pages[next_page] = createPage(next_page)

def createPage(page_no: int) -> tk.Frame:
    page = tk.Frame(root)

    # Splash page
    if page_no == 0:
        # Bottom bar
        next_cancel_bar = tk.Frame(page, height=bar_height, background="#CCC")
        ttk.Button(next_cancel_bar, text="Cancel", command=root.destroy).pack(side="right", fill="none", anchor="e", pady=10, padx=10)
        ttk.Button(next_cancel_bar, text="Next", command=lambda: swapPage(0, 1) if platform.system() != "Linux" else swapPage(0, 2)).pack(side="right", fill="none", anchor="e", pady=10)
        next_cancel_bar.pack(anchor="nw", side="bottom", fill="x")

        # Left image
        tk.Label(page, image=splash_image, background="#FFF").pack(side="left", fill="y")

        # Main items
        main_content = tk.Frame(page, background="#FFF")
        ttk.Label(main_content, style="A.TLabel", text="Welcome to the Encryptext Setup Wizard", font=("Arial Bold", 20), wraplength=width-final_splash_size[0], justify="left").pack(side="top", fill="x", anchor="nw", padx=5, pady=10)
        ttk.Label(main_content, style="A.TLabel", text=f"This will install Encryptext version {version} on your computer.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(main_content, style="A.TLabel", text="It is recommended that you close all other applications before continuing.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(main_content, style="A.TLabel", text="Click Next to continue, or Cancel to exit Setup.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        main_content.pack(side="top", fill="both", expand=True)

    # Install type (all or current user)
    elif page_no == 1:
        # Bottom bar
        back_next_cancel_bar = tk.Frame(page, height=bar_height, background="#CCC")
        ttk.Button(back_next_cancel_bar, text="Cancel", command=root.destroy).pack(side="right", fill="none", anchor="e", pady=10, padx=10)
        ttk.Button(back_next_cancel_bar, text="Next", command=lambda: swapPage(1, 2)).pack(side="right", fill="none", anchor="e", pady=10)
        ttk.Button(back_next_cancel_bar, text="Back", command=lambda: swapPage(1, 0)).pack(side="right", fill="none", anchor="e", pady=10)
        back_next_cancel_bar.pack(anchor="nw", side="bottom", fill="x")

        # Main items
        main_content = tk.Frame(page, background="#FFF")

        header = tk.Frame(main_content, padx=10, pady=5, background="#FFF")
        left_head = tk.Frame(header, padx=10, pady=5, background="#FFF")

        ttk.Label(left_head, text="Choose Installation Options", font=("Arial Bold", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(left_head, text="        Choose for which users to install Encryptext.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        tk.Label(header, image=thumb_image, background="#FFF").pack(side="right", fill="none")

        left_head.pack(side="left", fill="x")
        header.pack(side="top", fill="x")
        center = tk.Frame(main_content, padx=50, pady=5, background="#FFF")

        ttk.Label(center, text="Please select whether you wish to install Encryptext for all users or just the current user.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Radiobutton(center, text="Anyone who uses this computer (all users)", value="global", variable=user_type, command=lambda: changeInstallPath("CHECKUSERTYPE")).pack(side="top", fill="x", anchor="nw")
        ttk.Radiobutton(center, text=f"Only for me (for '{cur_user}')", value="current", variable=user_type, command=lambda: changeInstallPath("CHECKUSERTYPE")).pack(side="top", fill="x", anchor="nw")

        center.pack(side="top", fill="both", expand=True)

        ttk.Label(main_content, text="Installation for all users requires Administrative privileges.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw", padx=50, pady=5)
        main_content.pack(anchor="n", side="top", fill="both", expand=True)

    # Install location
    elif page_no == 2:
        # Bottom bar
        back_next_cancel_bar = tk.Frame(page, height=bar_height, background="#CCC")
        ttk.Button(back_next_cancel_bar, text="Cancel", command=root.destroy).pack(side="right", fill="none", anchor="e", pady=10, padx=10)
        ttk.Button(back_next_cancel_bar, text="Next", command=lambda: swapPage(2, 3)).pack(side="right", fill="none", anchor="e", pady=10)
        ttk.Button(back_next_cancel_bar, text="Back", command=lambda: swapPage(2, 1) if platform.system() != "Linux" else swapPage(2, 0)).pack(side="right", fill="none", anchor="e", pady=10)
        back_next_cancel_bar.pack(anchor="nw", side="bottom", fill="x")

        # Main items
        main_content = tk.Frame(page, background="#FFF")

        header = tk.Frame(main_content, padx=10, pady=5, background="#FFF")
        left_head = tk.Frame(header, padx=10, pady=5, background="#FFF")

        ttk.Label(left_head, text="Select Destination Location", font=("Arial Bold", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(left_head, text="        Where should Encryptext be installed?", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        tk.Label(header, image=thumb_image, background="#FFF").pack(side="right", fill="none")

        left_head.pack(side="left", fill="x")
        header.pack(side="top", fill="x")
        center = tk.Frame(main_content, padx=50, pady=5, background="#FFF")

        ttk.Label(center, image=folder_image, compound="left", text="  Setup will install Encryptext into the following folder.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(center, text="To continue, click Next. If you would like to select a different folder, click Browse", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")

        entry_area = tk.Frame(center, background="#FFF", pady=10, padx=10)

        ttk.Entry(entry_area, font=("Arial", 11), textvariable=install_path).pack(side="left", fill="x", anchor="nw", expand=True)
        ttk.Button(entry_area, style="A.TButton", text="Browse...", command=changeInstallPath).pack(side="left", fill="none", padx=10)

        entry_area.pack(side="top", fill="x")
        center.pack(side="top", fill="both", expand=True)

        ttk.Label(main_content, text="At least 40.0 MB of free disk space is required.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw", padx=50, pady=5)
        main_content.pack(anchor="n", side="top", fill="both", expand=True)

    # Additional items selection
    elif page_no == 3:
        # Bottom bar
        back_next_cancel_bar = tk.Frame(page, height=bar_height, background="#CCC")
        ttk.Button(back_next_cancel_bar, text="Cancel", command=root.destroy).pack(side="right", fill="none", anchor="e", pady=10, padx=10)
        ttk.Button(back_next_cancel_bar, text="Next", command=lambda: swapPage(3, 4) if start_menu_folder.get() else swapPage(3, 5)).pack(side="right", fill="none", anchor="e", pady=10)
        ttk.Button(back_next_cancel_bar, text="Back", command=lambda: swapPage(3, 2)).pack(side="right", fill="none", anchor="e", pady=10)
        back_next_cancel_bar.pack(anchor="nw", side="bottom", fill="x")

        # Main items
        main_content = tk.Frame(page, background="#FFF")

        header = tk.Frame(main_content, padx=10, pady=5, background="#FFF")
        left_head = tk.Frame(header, padx=10, pady=5, background="#FFF")

        ttk.Label(left_head, text="Select Additional Tasks", font=("Arial Bold", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(left_head, text="        Which additional tasks should be performed?", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        tk.Label(header, image=thumb_image, background="#FFF").pack(side="right", fill="none")

        left_head.pack(side="left", fill="x")
        header.pack(side="top", fill="x")
        center = tk.Frame(main_content, padx=50, pady=5, background="#FFF")

        ttk.Label(center, style="B.TLabel", text="Select the additional tasks you would like Setup to perform while installing Encryptext, then click next.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")

        if platform.system() == "Windows":
            state = "normal"
        else:
            state = "disabled"
        ttk.Checkbutton(center, text="Create Start Menu folder", onvalue=True, offvalue=False, variable=start_menu_folder, state=state).pack(side="top", fill="x", anchor="nw")
        ttk.Checkbutton(center, text="Create Desktop shortcut", onvalue=True, offvalue=False, variable=desktop_shortcut).pack(side="top", fill="x", anchor="nw")

        center.pack(side="top", fill="both", expand=True)
        main_content.pack(anchor="n", side="top", fill="both", expand=True)

    # Start menu folder location
    elif page_no == 4:
        # Bottom bar
        back_next_cancel_bar = tk.Frame(page, height=bar_height, background="#CCC")
        ttk.Button(back_next_cancel_bar, text="Cancel", command=root.destroy).pack(side="right", fill="none", anchor="e", pady=10, padx=10)
        ttk.Button(back_next_cancel_bar, text="Next", command=lambda: swapPage(4, 5)).pack(side="right", fill="none", anchor="e", pady=10)
        ttk.Button(back_next_cancel_bar, text="Back", command=lambda: swapPage(4, 3)).pack(side="right", fill="none", anchor="e", pady=10)
        back_next_cancel_bar.pack(anchor="nw", side="bottom", fill="x")

        # Main items
        main_content = tk.Frame(page, background="#FFF")

        header = tk.Frame(main_content, padx=10, pady=5, background="#FFF")
        left_head = tk.Frame(header, padx=10, pady=5, background="#FFF")

        ttk.Label(left_head, text="Select Start Menu Folder", font=("Arial Bold", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(left_head, text="        Where should Setup place the program's shortcuts?", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        tk.Label(header, image=thumb_image, background="#FFF").pack(side="right", fill="none")

        left_head.pack(side="left", fill="x")
        header.pack(side="top", fill="x")
        center = tk.Frame(main_content, padx=50, pady=5, background="#FFF")

        ttk.Label(center, image=folder_image, compound="left", text="  Setup will create the program's shortcuts in the following Start Menu folder.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(center, text="To continue, click Next. If you would like to select a different folder, click Browse", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")

        entry_area = tk.Frame(center, background="#FFF", pady=10, padx=10)

        ttk.Entry(entry_area, font=("Arial", 11), textvariable=start_menu_name).pack(side="left", fill="x", anchor="nw", expand=True)
        ttk.Button(entry_area, style="A.TButton", text="Browse...", command=changeStartMenuName).pack(side="left", fill="none", padx=10)

        entry_area.pack(side="top", fill="x")
        center.pack(side="top", fill="both", expand=True)
        main_content.pack(anchor="n", side="top", fill="both", expand=True)

    # License agreement page
    elif page_no == 5:
        # Bottom bar
        back_next_cancel_bar = tk.Frame(page, height=bar_height, background="#CCC")
        ttk.Button(back_next_cancel_bar, text="Cancel", command=root.destroy).pack(side="right", fill="none", anchor="e", pady=10, padx=10)
        ttk.Button(back_next_cancel_bar, text="Next", command=lambda: swapPage(5, 6) if agreement_accept.get() else swapPage(5, 5)).pack(side="right", fill="none", anchor="e", pady=10)
        ttk.Button(back_next_cancel_bar, text="Back", command=lambda: swapPage(5, 4) if start_menu_folder.get() else swapPage(5, 3)).pack(side="right", fill="none", anchor="e", pady=10)
        back_next_cancel_bar.pack(anchor="nw", side="bottom", fill="x")

        # Main items
        main_content = tk.Frame(page, background="#FFF")

        header = tk.Frame(main_content, padx=10, pady=5, background="#FFF")
        left_head = tk.Frame(header, padx=10, pady=5, background="#FFF")

        ttk.Label(left_head, text="License Agreement", font=("Arial Bold", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(left_head, text="        Please read the following important information before continuing.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        tk.Label(header, image=thumb_image, background="#FFF").pack(side="right", fill="none")

        left_head.pack(side="left", fill="x")
        header.pack(side="top", fill="x")
        center = tk.Frame(main_content, padx=50, pady=5, background="#FFF")

        ttk.Label(center, style="B.TLabel", text="Please read the following License Agreement. You must accept the terms of this agreement before continuing with the installation.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        license_box = tk.Text(center, height=15, font=("Arial", 11), wrap="word", border=1, relief="solid", padx=5, pady=5)
        license_box.pack(side="top", fill="both", anchor="nw")
        license_box.insert(tk.END, license_text)
        license_box.configure(state="disabled")
        ttk.Radiobutton(center, text="I accept the agreement", value=True, variable=agreement_accept, command=lambda: changeInstallPath("CHECKUSERTYPE")).pack(side="top", fill="x", anchor="nw")
        ttk.Radiobutton(center, text="I do not accept the agreement", value=False, variable=agreement_accept, command=lambda: changeInstallPath("CHECKUSERTYPE")).pack(side="top", fill="x", anchor="nw")

        center.pack(side="top", fill="both", expand=True)
        main_content.pack(anchor="n", side="top", fill="both", expand=True)

    # Final confirm page
    elif page_no == 6:
        # Bottom bar
        back_next_cancel_bar = tk.Frame(page, height=bar_height, background="#CCC")
        ttk.Button(back_next_cancel_bar, text="Cancel", command=root.destroy).pack(side="right", fill="none", anchor="e", pady=10, padx=10)
        ttk.Button(back_next_cancel_bar, text="Install", command=lambda: swapPage(6, 7)).pack(side="right", fill="none", anchor="e", pady=10)
        ttk.Button(back_next_cancel_bar, text="Back", command=lambda: swapPage(6, 5)).pack(side="right", fill="none", anchor="e", pady=10)
        back_next_cancel_bar.pack(anchor="nw", side="bottom", fill="x")

        # Main items
        main_content = tk.Frame(page, background="#FFF")

        header = tk.Frame(main_content, padx=10, pady=5, background="#FFF")
        left_head = tk.Frame(header, padx=10, pady=5, background="#FFF")

        ttk.Label(left_head, text="Ready to Install", font=("Arial Bold", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(left_head, text="        Setup is now ready to begin installing Encryptext on your computer.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        tk.Label(header, image=thumb_image, background="#FFF").pack(side="right", fill="none")

        left_head.pack(side="left", fill="x")
        header.pack(side="top", fill="x")
        center = tk.Frame(main_content, padx=50, pady=5, background="#FFF")

        ttk.Label(center, style="B.TLabel", text="Click Install to continue with the installation, or click Back if you want to review or change any settings.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        confirm_options_box = tk.Text(center, height=20, font=("Arial", 11), wrap="word", relief="flat", background="#EEE")
        confirm_options_box.pack(side="top", fill="both", anchor="nw")
        confirm_options_box.insert(tk.END, getFinalOptions())
        confirm_options_box.configure(state="disabled")

        center.pack(side="top", fill="both", expand=True)
        main_content.pack(anchor="n", side="top", fill="both", expand=True)

    # Installing page
    elif page_no == 7:
        # Bottom bar
        back_next_cancel_bar = tk.Frame(page, height=bar_height, background="#CCC")
        ttk.Button(back_next_cancel_bar, text="Cancel", command=root.destroy, state="disabled").pack(side="right", fill="none", anchor="e", pady=10, padx=10)
        back_next_cancel_bar.pack(anchor="nw", side="bottom", fill="x")

        # Main items
        main_content = tk.Frame(page, background="#FFF")

        header = tk.Frame(main_content, padx=10, pady=5, background="#FFF")
        left_head = tk.Frame(header, padx=10, pady=5, background="#FFF")

        ttk.Label(left_head, text="Installing", font=("Arial Bold", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(left_head, text="        Please wait while Setup installs Encryptext on your computer.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        tk.Label(header, image=thumb_image, background="#FFF").pack(side="right", fill="none")

        left_head.pack(side="left", fill="x")
        header.pack(side="top", fill="x")
        center = tk.Frame(main_content, padx=50, pady=5, background="#FFF")

        ttk.Label(center, style="B.TLabel", text="Building custom application...", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        # global progress_bar
        progress_bar = ttk.Progressbar(center, value=0, mode="indeterminate", orient="horizontal")
        progress_bar.pack(side="top", fill="x", padx=10, pady=20)
        progress_bar.start()
        progress_bar.after(0, lambda: installApp(progress_bar))

        center.pack(side="top", fill="both", expand=True)
        main_content.pack(anchor="n", side="top", fill="both", expand=True)

    # Install complete page
    elif page_no == 8:
        # Bottom bar
        finish_bar = tk.Frame(page, height=bar_height, background="#CCC")
        ttk.Button(finish_bar, text="Finish", command=root.destroy).pack(side="right", fill="none", anchor="e", pady=10, padx=10)
        finish_bar.pack(anchor="nw", side="bottom", fill="x")

        # Left image
        tk.Label(page, image=splash_image, background="#FFF").pack(side="left", fill="y")

        # Main items
        main_content = tk.Frame(page, background="#FFF")
        ttk.Label(main_content, style="A.TLabel", text="Completing the Encryptext Setup Wizard", font=("Arial Bold", 20), wraplength=width-final_splash_size[0], justify="left").pack(side="top", fill="x", anchor="nw", padx=5, pady=10)
        ttk.Label(main_content, style="A.TLabel", text="Setup has finished installing Encryptext on your computer. The application may be launched by selecting the installed shortcuts.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(main_content, style="A.TLabel", text="Click Finish to exit Setup.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        main_content.pack(side="top", fill="both", expand=True)

    page.pack(fill="both", side="top", expand=True)
    return page

# Create multiple pages
pages = []
for i in range(10):  # Change this to the number of pages you want
    page = tk.Frame(root)
    pages.append(page)

# Widget information here
bar_height = 50
orig_image_size = (1024, 1024)
final_splash_size = (250, height-bar_height)
thumb_size = (50, 50)
icon_size = (int(512 / 15), int(410 / 15))
final_size_ratio = final_splash_size[0] / final_splash_size[1]
orig_image_center = (orig_image_size[0] / 2, orig_image_size[0] / 2)
crop_splash_image = (int(orig_image_center[0] - (orig_image_size[0] / 4)), 0, int(orig_image_center[0] + (orig_image_size[0] / 4)), orig_image_size[1])
crop_thumb_image = (int(orig_image_center[0] - (orig_image_size[0] / 4)), 0, int(orig_image_center[0] + (orig_image_size[0] / 4)), orig_image_size[1])

splash_image = ImageTk.PhotoImage(Image.open("images/installer_splash_image.jpg").crop(crop_splash_image).resize(final_splash_size))
thumb_image = ImageTk.PhotoImage(Image.open("images/app_icon.ico").resize(thumb_size))
folder_image = ImageTk.PhotoImage(Image.open("images/folder_image.png").resize(icon_size))

style = ttk.Style()
style.configure("TButton", background="#CCC", padding=3)
style.configure("TLabel", background="#FFF", padding=(10, 5))
style.configure("A.TButton", background="#FFF")
style.configure("A.TLabel", background="#FFF", padding=(10, 5), wraplength=width-final_splash_size[0]-20)
style.configure("B.TLabel", background="#FFF", padding=(10, 5), wraplength=width-150)
style.configure("TRadiobutton", background="#FFF", padding=(25, 5), font=("Arial", 11))
style.configure("TCheckbutton", background="#FFF", padding=(25, 5), font=("Arial", 11))

# Installer info
user_type = tk.StringVar(root, "current")
install_path = tk.StringVar(root, "")
cur_user = path.expanduser("~").split("\\")[-1]

desktop_shortcut = tk.BooleanVar(root, True)
start_menu_folder = tk.BooleanVar(root, False)

start_menu_name = tk.StringVar(root, "Encryptext")
start_menu_path = path.join(path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs")

license_text = """MIT License

Copyright (c) 2023 Sooraj Sannabhadti

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
agreement_accept = tk.BooleanVar(root, False)

completed = False

def changeInstallPath(path_str: str = None) -> None:
    """
    Changes the installation path for the Encryptext application.

    Args:
        path_str (str, optional): The new installation path. If not provided, a file dialog will be displayed to choose a directory.

    Returns:
        None
    """
    global install_path

    if path_str == "CHECKUSERTYPE":
        if platform.system() == "Linux":
            path_str = "/opt"
        elif platform.system() == "Windows":
            if user_type.get() == "current":
                path_str = path.join(environ["LocalAppData"], "Encryptext")
            else:
                # From: https://stackoverflow.com/a/1283667
                path_str = path.join(environ["ProgramW6432"], "Encryptext")
        elif platform.system() == "Darwin":
            if user_type.get() == "current":
                path_str = path.join(path.expanduser("~"), "Applications", "Encryptext")
            else:
                path_str = path.join("Applications", "Encryptext")
        else:
            path_str = "/Encryptext"
    elif path_str is None:
        path_str = filedialog.askdirectory(initialdir=install_path, mustexist=True)

    if path_str != "":
        install_path.set(path_str)

def changeStartMenuName(name: str = None) -> None:
    """
    Changes the name of the start menu entry for the program.

    Args:
        name (str, optional): The new name for the start menu entry. If not provided, a file dialog will be shown to select a directory.

    Returns:
        None
    """
    global start_menu_name

    if name == None:
        name = filedialog.askdirectory(initialdir=start_menu_path, mustexist=True)

    if name != "":
        start_menu_name.set(name.split("AppData/Roaming/Microsoft/Windows/Start Menu/Programs/")[-1])

def getFinalOptions() -> str:
    """
    Returns the final options selected by the user for installation.

    Returns:
        str: A formatted string containing the installation location, start menu folder (if selected),
             additional tasks, and whether to create a desktop shortcut.
    """
    insert1 = f"""Start Menu folder:
    {start_menu_name.get()}"""
    insert2 = f"""Create Start Menu folder: {'Yes' if start_menu_folder.get() else 'No'}"""

    return f"""Installation location:
    {install_path.get()}

{insert1 if start_menu_folder.get() else ''}

Additional tasks:
    {insert2}
    Create Desktop shortcut: {'Yes' if desktop_shortcut.get() else 'No'}"""

def checkInstallCompletion(bar):
    #TODO: Change what happens in here
    print(bar["value"])
    if completed:
        swapPage(7, 8)
    else:
        bar.after(1000, lambda: checkInstallCompletion(bar))

def installApp(bar):
    global completed
    bar.after(1000, lambda: checkInstallCompletion(bar))

    #TODO: Add some installation stuff here
    print("Installing...")
    completed = True

# Set the default install path
changeInstallPath("CHECKUSERTYPE")

# Create the first page to start
pages[0] = createPage(0)

root.mainloop()
