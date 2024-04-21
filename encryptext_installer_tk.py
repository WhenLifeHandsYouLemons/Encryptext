# Imports
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

version = "1.9.4"

# Main window configurations
root = tk.Tk()
root.title("Encryptext Installer")
width = 750
height = 550
root.geometry(f"{width}x{height}")  # You can set this to the desired size
root.resizable(False, False)

# Create a function to raise a page to the top
def swapPage(cur_page, next_page):
    pages[cur_page].destroy()
    pages[next_page] = createPage(next_page)

def createPage(page_no):
    page = tk.Frame(root)

    if page_no == 0:
        # Bottom bar
        next_cancel_bar = tk.Frame(page, height=bar_height, background="#CCC")
        ttk.Button(next_cancel_bar, text="Cancel", command=root.destroy).pack(side="right", fill="none", anchor="e", pady=10, padx=10)
        ttk.Button(next_cancel_bar, text="Next", command=lambda: swapPage(0, 1)).pack(side="right", fill="none", anchor="e", pady=10)
        next_cancel_bar.pack(anchor="nw", side="bottom", fill="x")

        # Left image
        tk.Label(page, image=img).pack(side="left", fill="y")

        # Main items
        main_content = tk.Frame(page, background="#FFF")
        ttk.Label(main_content, text="Welcome to the Encryptext Setup Wizard", font=("Arial Bold", 20), wraplength=width-final_size[0], justify="left", padding=10).pack(side="top", fill="x", anchor="nw")
        ttk.Label(main_content, text=f"This will install Encryptext version {version} on your computer.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(main_content, text="It is recommended that you close all other applications before continuing.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        ttk.Label(main_content, text="Click Next to continue, or Cancel to exit Setup.", font=("Arial", 11), justify="left").pack(side="top", fill="x", anchor="nw")
        main_content.pack(side="top", fill="both", expand=True)
    elif page_no == 1:
        # Bottom bar
        back_next_cancel_bar = tk.Frame(page, height=bar_height, background="#CCC")
        ttk.Button(back_next_cancel_bar, text="Cancel", command=root.destroy).pack(side="right", fill="none", anchor="e", pady=10, padx=10)
        ttk.Button(back_next_cancel_bar, text="Next", command=lambda: swapPage(1, 2)).pack(side="right", fill="none", anchor="e", pady=10)
        ttk.Button(back_next_cancel_bar, text="Back", command=lambda: swapPage(1, 0)).pack(side="right", fill="none", anchor="e", pady=10)
        back_next_cancel_bar.pack(anchor="nw", side="bottom", fill="x")

        # Main items
        main_content = tk.Frame(page, background="#FFF", height=501)
        main_content.pack(side="top", fill="both", expand=True)

    page.pack(fill="both", side="top")
    return page

# Create multiple pages
pages = []
for i in range(8):  # Change this to the number of pages you want
    page = tk.Frame(root)
    pages.append(page)

# Widget information here
bar_height = 50
orig_image_size = (1024, 1024)
final_size = (250, height-bar_height)
final_size_ratio = final_size[0] / final_size[1]
crop_image_size = (orig_image_size[0] * final_size_ratio, orig_image_size[1])
orig_image_center = (orig_image_size[0] / 2, orig_image_size[0] / 2)
crop_image_tuple = (int(orig_image_center[0] - (orig_image_size[0] / 4)), 0, int(orig_image_center[0] + (orig_image_size[0] / 4)), orig_image_size[1])

img = ImageTk.PhotoImage(Image.open("installer_image.jpg").crop(crop_image_tuple).resize(final_size))

style = ttk.Style()
style.configure("TButton", background="#CCC", padding=3)
style.configure("TLabel", background="#FFF", padding=(10, 5), wraplength=width-final_size[0])

# Create the first page to start
pages[0] = createPage(0)

root.mainloop()
