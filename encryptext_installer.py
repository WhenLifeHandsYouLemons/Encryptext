#!/usr/bin/python'

from os import rename, remove, rmdir, makedirs, listdir, path, environ
from shutil import rmtree
import sys
from subprocess import run, PIPE
from time import sleep
import json
from cryptography.fernet import Fernet as F
from random import choice, randint
from string import ascii_letters, digits
import threading as t
# https://github.com/rsalmei/alive-progress
from alive_progress import alive_bar, styles

version = "1.9.0"

print("\nStarting installer...")
print("Please wait...")

home_dir = path.expanduser("~")
dir_path = path.join(home_dir, ".encryptext")

# Used for getting files when using one-file mode .exe format
def getTrueFilename(filename):
    try:
        base = sys._MEIPASS
    except Exception:
        base = path.abspath(".")
    return path.join(base, filename)

# Creates an executable file
def appCreation():
    file_path = path.join(dir_path, f"encryptext_v{version}.pyw")
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
                "--name",
                "encryptext",
                "--collect-all",
                "tkinterweb",
                "--exclude-module",
                "pywin32",
                file_path
    ]
    # Redirect both stdout and stderr to /dev/null or NUL depending on the platform
    with open(path.join(dir_path, "installer_output.log"), 'w') as output_file:
        run(command,
            shell=True,
            env=subproc_env,
            stdout=output_file,
            stderr=output_file,
            cwd=dir_path)

app_thread = t.Thread(target=appCreation)

def checkProgress(prev_val):
    # Needs to return a value between 0 and 1
    val = 0

    # Load output file
    with open(path.join(dir_path, "installer_output.log"), 'r') as output_file:
        text = output_file.readlines()

    try:
        # This is just a rough approximation of how long the process might take
        # As pyinstaller doesn't provide ETAs for compilation, we have to guess
        # based on the output text that we store in a log file and then delete
        # once it finishes installing.
        val = int(text[-1].split(": ")[0].split(" ")[0]) / 117000
        return val
    except:
        return prev_val

# https://github.com/rsalmei/alive-progress
def progress_bar(percent_done):
    # Choose a random bar and spinner theme
    bar_themes = []
    for key, val in enumerate(styles.BARS):
        bar_themes.append(val)

    spin_themes = []
    for key, val in enumerate(styles.SPINNERS):
        spin_themes.append(val)

    with alive_bar(total=100, manual=True, bar=choice(bar_themes), spinner=choice(spin_themes), enrich_print=False) as bar:
        while percent_done < 1:
            # Update the progress bar
            bar(percent_done)

            if app_thread.is_alive():
                percent_done = checkProgress(percent_done)
            else:
                percent_done = 1

        bar(1)

    print("\nCleaning up...")

update = input("\nAre you updating or installing Encryptext? [(u)pdating/(i)nstalling] ")
while update != "u" and update != "i":
    update = input("\nAre you updating or installing Encryptext? [(u)pdating/(i)nstalling] ")

# Open the Encryptext.pyw file and read it into a variable
file = open(getTrueFilename("Encryptext.pyw"), "r", encoding="utf8")
file = file.read()
text = file

# Adds computed hash to file
hash_str = "INSERT COMPUTED HASH HERE"
file = text.split("# HASH STRING HERE")
hash_line = file[1].split("'")
hash_line[1] = hash_str
file[1] = "'".join(hash_line)

text = "".join(file)

# Communicate to old program
return_attributes = ""
if update == "u":
    try:
        exe_files = [f for f in listdir(dir_path) if f.endswith('.exe')]
        return_attributes = run([f"{path.join(dir_path, exe_files[0])}", hash_str], stdout=PIPE)
        return_attributes = return_attributes.stdout.decode().split("(")[-1].split(")")[0].split(", ")
    except IndexError:
        raise Exception("Encryptext hasn't been installed before! Please install the program before trying to update.")
    except:
        raise Exception("Something went wrong! Please try again or file a crash report on GitHub.")

# Find where the encryption key is stored in the file
file = text.split("# ENCRYPTION KEY HERE")

if update == "i":
    # Create a key and remove the b'' from the string
    key = F.generate_key().decode()
else:
    key = str(return_attributes[3].split("'")[1])

# Add the key to the file
key_line = file[1]
key_line = key_line.split("'")
key_line[1] = key
key_line = "'".join(key_line)
file[1] = key_line

text = "".join(file)

print("Encryption key set!")

possible_characters = ascii_letters + digits

# Find where the format item separator string is stored in the file
file = text.split("# FORMAT ITEM SEPARATOR HERE")

if update == "i":
    # Create a format item separator string
    format_item_separator = "".join([choice(possible_characters) for i in range(randint(15, 45))])
else:
    format_item_separator = str(return_attributes[0].split("'")[1])

# Add the format item separator string to the file
key_line = file[1]
key_line = key_line.split("'")
key_line[1] = format_item_separator
key_line = "'".join(key_line)
file[1] = key_line

text = "".join(file)

# Find where the format separator string is stored in the file
file = text.split("# FORMAT SEPARATOR HERE")

if update == "i":
    # Create a format separator string
    format_separator = "".join([choice(possible_characters) for i in range(randint(15, 45))])
else:
    format_separator = str(return_attributes[1].split("'")[1])

# Add the format separator string to the file
key_line = file[1]
key_line = key_line.split("'")
key_line[1] = format_separator
key_line = "'".join(key_line)
file[1] = key_line

text = "".join(file)

# Find where the format string is stored in the file
file = text.split("# FORMAT STRING HERE")

if update == "i":
    # Create a format string
    format_string = "".join([choice(possible_characters) for i in range(randint(15, 45))])
else:
    format_string = str(return_attributes[2].split("'")[1])

# Add the format string to the file
key_line = file[1]
key_line = key_line.split("'")
key_line[1] = format_string
key_line = "'".join(key_line)
file[1] = key_line

text = "".join(file)

print("Format strings set!")

# Get the current user's home directory
settings_file_path = path.join(dir_path, "settings.json")

# Define the settings data to save
# If they want to bring over their old settings or not
keep_settings = input("\nDo you want to load your settings from an old version?\nNOTE: If you don't have an older version, it will create new settings by default [(y)es/(n)o] ")
while keep_settings != "y" and keep_settings != "n":
    keep_settings = input("\nDo you want to load your settings from an old version?\nNOTE: If you don't have an older version, it will create new settings by default [(y)es/(n)o] ")

data = {
    "version": version,
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

# Change the values to be the old ones if the user allowed it
# Otherwise the values will already be the default ones
if keep_settings == "y":
    try:
        with open(settings_file_path, "r") as file:
            file = json.load(file)

        data = {
            "version": version,
            "recentFilePaths": file["recentFilePaths"],
            "maxRecentFiles": file["maxRecentFiles"],
            "otherSettings": {
                "theme": file["theme"],
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

makedirs(dir_path, exist_ok=True)

# Write JSON data
with open(settings_file_path, 'w') as file:
    json.dump(data, file)

print("Created data files!")

# Removes the program file from any previous installations to not cause issues
# This happens right before any files are going to be written to disk
try:
    remove(path.join(dir_path, f"encryptext_v{version}.pyw"))
except: pass

# Write the file back to the Encryptext.py file
with open(path.join(dir_path, f"encryptext_v{version}.pyw"), "w", encoding="utf8") as file:
    file.write(text)

print("Building custom program...\n\n")

# Removes the pyinstaller files from any previous installations to not cause issues
# This happens right before any files are going to be written to disk
try:
    rmdir(path.join(dir_path, "dist"))
    rmdir(path.join(dir_path, "build"))
except: pass

# Start thread to create app
app_thread.start()

# Show a progress bar while app is compiling
progress_bar(0)

# Wait for app compilation to finish
app_thread.join()

# Remove old version if it's the same version number before moving new one out
try:
    remove(path.join(dir_path, f"encryptext_v{version}.exe"))
except: pass

# Moves the exe out of the dist folder
rename(path.join(dir_path, "dist", "encryptext.exe"), path.join(dir_path, f"encryptext_v{version}.exe"))

# Create desktop shortcut
# https://stackoverflow.com/a/69597224
try:
    from win32com.client import Dispatch

    shortcut_path = path.join(home_dir, "Desktop", f"Encryptext_v{version}.lnk")
    target_path = path.join(dir_path, f"encryptext_v{version}.exe")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.save()
except:
    print(f"Couldn't create Desktop shortcut!")

# Create Start Menu shortcut
try:
    # Create Start Menu folder for Encryptext
    makedirs(path.join(home_dir, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Encryptext"), exist_ok=True)

    shortcut_path = path.join(home_dir, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Encryptext", f"Encryptext {version}.lnk")
    target_path = path.join(dir_path, f"encryptext_v{version}.exe")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.save()
except:
    print("Couldn't create Start Menu shortcut!")

print("\n\nCreated program!")

# Removes the files from pyinstaller
rmdir(path.join(dir_path, "dist"))
rmtree(path.join(dir_path, "build"))
remove(path.join(dir_path, f"encryptext_v{version}.pyw"))
remove(path.join(dir_path, "installer_output.log"))

input("\nCompleted! Press enter to finish setup...")
