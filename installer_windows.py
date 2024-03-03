import os
import sys
from subprocess import run
from time import sleep
from cryptography.fernet import Fernet as F
from random import choice, randint
from string import ascii_letters, digits
import threading as t

version = "1.7.1"

print("\nStarting installer...")
print("Please wait...")

# Used for getting files when using one-file mode .exe format
def getTrueFilename(filename):
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath(".")
    return os.path.join(base, filename)

# Creates an executable file
def appCreation():
    file_path = getTrueFilename("Encryptext-User.pyw")
    icon_path = getTrueFilename("app_icon.ico")
    # Fix for tkinterweb not working
    # https://github.com/pyinstaller/pyinstaller/issues/6658#issuecomment-1062817361
    subproc_env = os.environ.copy()
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
                "CRITICAL",
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
    with open(os.devnull, 'w') as null_file:
        run(command, shell=True, env=subproc_env, stdout=null_file, stderr=null_file)

# https://stackoverflow.com/a/34325723
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

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

# Write the file back to the Encryptext.py file
file = open(getTrueFilename("Encryptext-User.pyw"), "w", encoding="utf8")
file.write(text)
file.close()

print("Building custom program...\n\n")

# Start thread to create app
app_thread = t.Thread(target=appCreation)
app_thread.start()

# Show a progress bar while app is compiling
l = 100
i = 0
speed = 1.75
printProgressBar(i, l, prefix='Progress:', suffix='Complete', length=50)
while i < l-1:
    sleep(speed)

    if not app_thread.is_alive():
        speed = 0.05

    i += 1
    printProgressBar(i, l, prefix='Progress:', suffix='Complete', length=50, printEnd='')

app_thread.join()

printProgressBar(i+1, l, prefix='Progress:', suffix='Complete', length=50, printEnd='')

# Moves the exe out of the dist folder
os.system(f"move dist\\Encryptext.exe Encryptext_v{version}.exe >nul")

print("\n\nCreated program!")
print("Cleaning up...")

# Removes the "dist" folder
os.system("rmdir /s /q dist")
# Removes the "build" folder
os.system("rmdir /s /q build")
# Removes the "Encryptext.spec" file
os.system("del Encryptext.spec")

input("\nCompleted! Press enter to finish setup...")
