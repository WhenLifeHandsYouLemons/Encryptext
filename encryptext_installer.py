from os import rename, remove, rmdir, makedirs, path, environ
from shutil import rmtree
import sys
from subprocess import run
from time import sleep
import json
from cryptography.fernet import Fernet as F
from random import choice, randint
from string import ascii_letters, digits
import threading as t
# https://github.com/rsalmei/alive-progress
from alive_progress import alive_bar, styles

version = "1.8.0"

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
    file_path = path.join(dir_path, "Encryptext-User.pyw")
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
                "Encryptext",
                "--collect-all",
                "tkinterweb",
                file_path
    ]
    # Redirect both stdout and stderr to /dev/null or NUL depending on the platform
    with open(path.join(dir_path, "installer_output_log.txt"), 'w') as output_file:
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
    with open(path.join(dir_path, "installer_output_log.txt"), 'r') as output_file:
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

need_update = input("\nDo you want to be able to update Encryptext in the future?\nNOTE: This lowers the security but allows you to update Encryptext to get new features and not lose your encrypted files. [(y)es/(n)o] ")
while need_update != "y" and need_update != "n":
    need_update = input("\nDo you want to be able to update Encryptext in the future?\nNOTE: This lowers the security but allows you to update Encryptext to get new features and not lose your encrypted files. [(y)es/(n)o] ")

# Open the Encryptext.py file and read it into a variable
file = open(getTrueFilename("Encryptext.pyw"), "r", encoding="utf8")
file = file.read()

# Find where the update mode is stored in the file
file = file.split("# UPDATE MODE HERE")

if need_update == "y":
    # Set the update option to true
    option = "update = True"
else:
    option = "update = False"

# Add the option to the file
file[1] = option

text = "".join(file)

print("\nUpdate option set!")

if update == "u":
    print("\n\nPlease open the current version of Encryptext you have.")
    print("In the menu bar at the top, click on 'Help'. Then click on 'Update Encryptext'.\n")
    sleep(5)

# Find where the encryption key is stored in the file
file = text.split("# ENCRYPTION KEY HERE")

if update == "i":
    # Create a key and remove the b'' from the string
    key = F.generate_key().decode()
else:
    key = str(input("\nPlease enter the Encryption Key (be careful to not add the spaces, just the text):"))
    while len(key) != 44 and key[-1] != "=":
        key = str(input("\nYou haven't entered the key correctly. Please enter the 'Encryption Key' (be careful to not add the spaces, just the text):"))
    print()

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
    format_item_separator = str(input("\nPlease enter the Format Item Separator (be careful to not add the spaces, just the text):"))
    while len(format_item_separator) < 15:
        format_item_separator = str(input("\nYou haven't entered the string correctly. Please enter the 'Format Item Separator' (be careful to not add the spaces, just the text):"))

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
    format_separator = str(input("\nPlease enter the Format Separator String (be careful to not add the spaces, just the text):"))
    while len(format_separator) < 15:
        format_separator = str(input("\nYou haven't entered the string correctly. Please enter the 'Format Separator String' (be careful to not add the spaces, just the text):"))

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
    format_string = str(input("\nPlease enter the Format String (be careful to not add the spaces, just the text):"))
    while len(format_string) < 15:
        format_string = str(input("\nYou haven't entered the string correctly. Please enter the 'Format String' (be careful to not add the spaces, just the text):"))
    print()

# Add the format string to the file
key_line = file[1]
key_line = key_line.split("'")
key_line[1] = format_string
key_line = "'".join(key_line)
file[1] = key_line

text = "".join(file)

print("Format strings set!")

# Removes the install files from any previous installations to not cause issues
try:
    remove(path.join(dir_path, "Encryptext.spec"))
    remove(path.join(dir_path, "Encryptext-User.pyw"))
    rmdir(path.join(dir_path, "dist"))
    rmdir(path.join(dir_path, "build"))
except: pass

# Write the file back to the Encryptext.py file
makedirs(dir_path, exist_ok=True)
with open(path.join(dir_path, "Encryptext-User.pyw"), "w", encoding="utf8") as file:
    file.write(text)

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

# Write JSON data
with open(settings_file_path, 'w') as file:
    json.dump(data, file)

print("Created data files!")

print("Building custom program...\n\n")

# Start thread to create app
app_thread.start()

# Show a progress bar while app is compiling
progress_bar(0)

# Wait for app compilation to finish
app_thread.join()

# Moves the exe out of the dist folder
rename(path.join(dir_path, "dist", "Encryptext.exe"), f"Encryptext_v{version}.exe")

print("\n\nCreated program!")

# Removes the files from pyinstaller
rmdir(path.join(dir_path, "dist"))
rmtree(path.join(dir_path, "build"))
remove(path.join(dir_path, "Encryptext.spec"))
remove(path.join(dir_path, "Encryptext-User.pyw"))
remove(path.join(dir_path, "installer_output_log.txt"))

input("\nCompleted! Press enter to finish setup...")
