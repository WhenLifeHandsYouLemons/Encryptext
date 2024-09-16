#!/usr/bin/python'

# Created by Sooraj S
# https://encryptext.sooraj.dev
# Free for everyone. Forever.

# Imports
import json
from os import listdir, makedirs, path, environ, remove, rename, rmdir
from secrets import choice
from shutil import rmtree
from string import ascii_letters, digits
import sys
from subprocess import PIPE, run
import time
import tkinter as tk
from tkinter import filedialog, ttk
from cryptography.fernet import Fernet as F
from PIL import Image, ImageTk
import platform
import threading as t

# Used for getting files when using one-file mode
def getTrueFilename(filename):
    """
    Returns the true filename by joining the base path with the given filename.

    Parameters:
    filename (str): The name of the file.

    Returns:
    str: The true filename.

    """
    try:
        base = sys._MEIPASS
    except Exception:
        base = path.abspath(".")
    return path.join(base, filename)

version = "INSERT VERSION NUMBER HERE"

# Main window configurations
root = tk.Tk()
root.title("Setup - Encryptext")
root.iconbitmap(getTrueFilename("images/app_icon.ico"))
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
    """
    Creates a page for the Encryptext Setup Wizard.

    Parameters:
        page_no (int): The page number to create.

    Returns:
        tk.Frame: The created page as a Tkinter Frame.

    Raises:
        None
    """
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
        progress_bar = ttk.Progressbar(center, value=0, mode="determinate", orient="horizontal")
        progress_bar.pack(side="top", fill="x", padx=10, pady=20)
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

# Widget information
bar_height = 50
orig_image_size = (1024, 1024)
final_splash_size = (250, height-bar_height)
thumb_size = (50, 50)
icon_size = (int(512 / 15), int(410 / 15))
final_size_ratio = final_splash_size[0] / final_splash_size[1]
orig_image_center = (orig_image_size[0] / 2, orig_image_size[0] / 2)
crop_splash_image = (int(orig_image_center[0] - (orig_image_size[0] / 4)), 0, int(orig_image_center[0] + (orig_image_size[0] / 4)), orig_image_size[1])
crop_thumb_image = (int(orig_image_center[0] - (orig_image_size[0] / 4)), 0, int(orig_image_center[0] + (orig_image_size[0] / 4)), orig_image_size[1])

splash_image = ImageTk.PhotoImage(Image.open(getTrueFilename("images/installer_splash_image.jpg")).crop(crop_splash_image).resize(final_splash_size))
thumb_image = ImageTk.PhotoImage(Image.open(getTrueFilename("images/app_icon.ico")).resize(thumb_size))
folder_image = ImageTk.PhotoImage(Image.open(getTrueFilename("images/folder_image.png")).resize(icon_size))

style = ttk.Style()
style.configure("TButton", background="#CCC", padding=3)
style.configure("TLabel", background="#FFF", padding=(10, 5))
style.configure("A.TButton", background="#FFF")
style.configure("A.TLabel", background="#FFF", padding=(10, 5), wraplength=width-final_splash_size[0]-25)
style.configure("B.TLabel", background="#FFF", padding=(10, 5), wraplength=width-150)
style.configure("TRadiobutton", background="#FFF", padding=(25, 5), font=("Arial", 11))
style.configure("TCheckbutton", background="#FFF", padding=(25, 5), font=("Arial", 11))

# Installer information
home_dir = path.expanduser("~")

user_type = tk.StringVar(root, "current")
install_path = tk.StringVar(root, "")
cur_user = home_dir.split("\\")[-1]

desktop_shortcut = tk.BooleanVar(root, True)
start_menu_folder = tk.BooleanVar(root, True)

start_menu_name = tk.StringVar(root, "Encryptext")
start_menu_path = path.join(home_dir, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs")

license_text = """MIT License

Copyright (c) 2023 Sooraj Sannabhadti

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
agreement_accept = tk.BooleanVar(root, False)

created = False
update = False

os_type = platform.system()

if os_type == "Windows":
    end_file_type = "exe"
elif os_type == "Darwin":
    end_file_type = ""
elif os_type == "Linux":
    end_file_type = "bin"
else:
    end_file_type = ""

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
                path_str = path.join(home_dir, "Applications", "Encryptext")
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

def checkInstallCompletion(bar: ttk.Progressbar, prev_val: int = 0) -> None:
    """
    Check the completion status of the installation process and update the progress bar.

    Args:
        bar (ttk.Progressbar): The progress bar widget to update.
        prev_val (int, optional): The previous value of the progress bar. Defaults to 0.
    """
    # Update the window so it isn't stuck
    root.update()

    try:
        # Load output file
        with open(path.join(install_path.get(), "installer_output.log"), 'r') as output_file:
            text = output_file.readlines()

        # This is just a rough approximation of how long the process might take
        # As pyinstaller doesn't provide ETAs for compilation, we have to guess
        # based on the output text that we store in a log file and then delete
        # once it finishes installing.
        val = int((int(text[-1].split(": ")[0].split(" ")[0]) / 117000) * 100)
    except:
        val = prev_val
    bar["value"] = val

    if created:
        swapPage(7, 8)
    else:
        time.sleep(1)
        checkInstallCompletion(bar, val)

def installApp(bar: ttk.Progressbar) -> None:
    """
    Installs the Encryptext application.

    Args:
        bar (ttk.Progressbar): The progress bar widget.

    Returns:
        None
    """
    def addToFile(file: str, split_str: str, join_str: str) -> str:
        """
        Adds the key to the file by splitting the file string using the split_str,
        joining the split parts using the join_str, and returning the modified file string.

        Args:
            file (str): The file string to modify.
            split_str (str): The string used to split the file string.
            join_str (str): The string used to join the split parts.

        Returns:
            str: The modified file string.
        """
        file = file.split(split_str)
        file = join_str.join(file)

        return file

    global update, install_path

    # Get the actual string so it's easier to access
    installed_path = install_path.get()

    # Open the Encryptext.pyw file and read it into a variable
    with open(getTrueFilename("Encryptext.pyw"), "r", encoding="utf8") as file:
        text = file.read()

    # Add version number to the file
    text = addToFile(text, "VERSION NUMBER HERE", version)

    # Change debug mode to False if it's True
    try:
        text = text.split("debug = True")
        text = "debug = False".join(text)
    except: pass

    # Adds computed hash to file
    hash_str = "INSERT COMPUTED HASH HERE"
    text = addToFile(text, "HASH STRING HERE", hash_str)

    if update:
        # Communicate to old program
        return_attributes = ""
        try:
            exec_files = [f for f in listdir(installed_path) if f.endswith(f'.{end_file_type}')]
            return_attributes = run([f"{path.join(installed_path, exec_files[0])}", hash_str], stdout=PIPE)
            return_attributes = return_attributes.stdout.decode().split("(")[-1].split(")")[0].split(", ")
        except IndexError:
            raise Exception("Encryptext hasn't been installed before! Please install the program before trying to update.")
        except Exception as e:
            raise Exception("Something went wrong! Please try again or file a crash report on GitHub. Error: {e}")

        # Encryption key
        key = str(return_attributes[3].split("'")[1])

        # For separators
        format_item_separator = str(return_attributes[0].split("'")[1])
        format_separator = str(return_attributes[1].split("'")[1])
        format_string = str(return_attributes[2].split("'")[1])
    else:
        # Create a key and remove the b'' from the string
        key = F.generate_key().decode()

        # For separators
        possible_characters = ascii_letters + digits

        possible_lengths = [i for i in range(15, 46, 1)]

        # Create a format item separator string
        format_item_separator = "".join([choice(possible_characters) for i in range(choice(possible_lengths))])
        # Create a format separator string
        format_separator = "".join([choice(possible_characters) for i in range(choice(possible_lengths))])
        # Create a format string
        format_string = "".join([choice(possible_characters) for i in range(choice(possible_lengths))])

    # Add the strings to the file
    text = addToFile(text, "ENCRYPTION KEY HERE", key)
    text = addToFile(text, "FORMAT ITEM SEPARATOR HERE", format_item_separator)
    text = addToFile(text, "FORMAT SEPARATOR HERE", format_separator)
    text = addToFile(text, "FORMAT STRING HERE", format_string)

    settings_file_path = path.join(installed_path, "settings.json")

    text = addToFile(text, "SETTINGS FILE LOCATION HERE", settings_file_path)

    data = {
        "recentFilePaths": [],
        "maxRecentFiles": 5,
        "otherSettings": {
            "theme": "light",
            "fontStyle": "Arial",
            "fontScaleFactor": 1,
            "language": "en_US",
            "autoSave": False,
            "autoSaveInterval": 15,
            "showLineNumbers": False,
            "wrapLines": True,
            "highlightActiveLine": False,
            "closeAllTabs": False
        }
    }

    # Otherwise the values will already be the default ones
    try:
        with open(settings_file_path, "r", encoding="utf-8") as file:
            file = json.load(file)

        data = {
            "recentFilePaths": file["recentFilePaths"],
            "maxRecentFiles": file["maxRecentFiles"],
            "otherSettings": {
                "theme": file["otherSettings"]["theme"],
                "fontStyle": file["otherSettings"]["fontStyle"],
                "fontScaleFactor": file["otherSettings"]["fontScaleFactor"],
                "language": file["otherSettings"]["language"],
                "autoSave": file["otherSettings"]["autoSave"],
                "autoSaveInterval": file["otherSettings"]["autoSaveInterval"],
                "showLineNumbers": file["otherSettings"]["showLineNumbers"],
                "wrapLines": file["otherSettings"]["wrapLines"],
                "highlightActiveLine": file["otherSettings"]["highlightActiveLine"],
                "closeAllTabs": file["otherSettings"]["closeAllTabs"]
            }
        }
    except: pass

    makedirs(installed_path, exist_ok=True)

    # Write JSON data
    with open(settings_file_path, 'w') as file:
        json.dump(data, file)

    # Removes the program file from any previous installations to not cause issues
    # This happens right before any files are going to be written to disk
    try:
        remove(path.join(installed_path, f"encryptext_v{version}.pyw"))
    except: pass

    # Write the file back to the Encryptext.py file
    with open(path.join(installed_path, f"encryptext_v{version}.pyw"), "w", encoding="utf8") as file:
        file.write(text)

    # Removes the pyinstaller files from any previous installations to not cause issues
    # This happens right before any files are going to be written to disk
    try:
        rmdir(path.join(installed_path, "dist"))
        rmdir(path.join(installed_path, "build"))
    except: pass

    # Create and start app compilation thread
    app_thread = t.Thread(target=appCreation)
    app_thread.start()

    # Run the progress bar
    checkInstallCompletion(bar)

    # Wait for app compilation to finish
    app_thread.join()

    # Remove old version if it's the same version number before moving new one out
    try:
        remove(path.join(installed_path, f"encryptext_v{version}.{end_file_type}"))
    except: pass

    # Moves the exec out of the dist folder
    rename(path.join(installed_path, "dist", f"encryptext.{end_file_type}"), path.join(installed_path, f"encryptext_v{version}.{end_file_type}"))

    # Create desktop shortcut for Windows
    if os_type == "Windows":
        if desktop_shortcut.get():
            # https://stackoverflow.com/a/69597224
            try:
                from win32com.client import Dispatch

                shortcut_path = path.join(home_dir, "Desktop", f"Encryptext_v{version}.lnk")
                target_path = path.join(installed_path, f"encryptext_v{version}.{end_file_type}")

                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = target_path
                shortcut.save()
            except Exception as e:
                print(f"Couldn't create Desktop shortcut! Error: {e}")

        if start_menu_folder.get():
            # Create Start Menu shortcut for Windows
            try:
                # Create Start Menu folder for Encryptext
                makedirs(path.join(home_dir, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Encryptext"), exist_ok=True)

                shortcut_path = path.join(home_dir, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Encryptext", f"Encryptext {version}.lnk")
                target_path = path.join(installed_path, f"encryptext_v{version}.{end_file_type}")

                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = target_path
                shortcut.save()
            except Exception as e:
                print(f"Couldn't create Start Menu shortcut! Error: {e}")
    elif os_type == "Linux":
        #TODO: Shortcuts for Linux
        pass
    elif os_type == "Darwin":
        #TODO: Shortcuts for MacOS
        pass

    # Removes the files from pyinstaller
    rmdir(path.join(installed_path, "dist"))
    rmtree(path.join(installed_path, "build"))
    remove(path.join(installed_path, f"encryptext_v{version}.pyw"))
    remove(path.join(installed_path, "installer_output.log"))

    return True

def appCreation() -> bool:
    """
    Compiles the application using PyInstaller.

    Returns:
        bool: True if the application was successfully compiled, None otherwise.
    """
    global install_path, created

    # Get the actual string so it's easier to access
    installed_path = install_path.get()

    # Compile the application
    file_path = path.join(installed_path, f"encryptext_v{version}.pyw")
    icon_path = getTrueFilename("app_icon.ico")
    # Fix for tkinterweb not working
    # https://github.com/pyinstaller/pyinstaller/issues/6658#issuecomment-1062817361
    subproc_env = environ.copy()
    subproc_env.pop('TCL_LIBRARY', None)
    subproc_env.pop('TK_LIBRARY', None)

    # https://stackoverflow.com/a/72523249
    # https://stackoverflow.com/a/13790741
    # https://stackoverflow.com/a/8529412
    command = ["pyinstaller",
                "--onefile",
                "--clean",
                "--windowed",
                "--log-level",
                "DEBUG",
                "--icon",
                icon_path,
                "--add-data",
                f"{icon_path};.",
                "--add-data",
                f"{getTrueFilename('ttkbootstrap')};ttkbootstrap",
                "--add-data",
                f"{getTrueFilename('tkinter')};tkinter",
                "--add-data",
                f"{getTrueFilename('tkinterweb')};tkinterweb",
                "--name",
                "encryptext",
                "--exclude-module",
                "pywin32",
                "--exclude-module",
                "Pillow",
                file_path
    ]
    # Redirect both stdout and stderr to /dev/null or NUL depending on the platform
    with open(path.join(installed_path, "installer_output.log"), 'w') as output_file:
        run(command,
            shell=True,
            env=subproc_env,
            stdout=output_file,
            stderr=output_file,
            cwd=installed_path)

    created = True
    return True

# Set the default install path
changeInstallPath("CHECKUSERTYPE")

# Create the first page to start
pages[0] = createPage(0)

root.mainloop()
