from os import devnull, system
from os.path import abspath, join
from sys import _MEIPASS
from time import sleep
from subprocess import check_call
from cryptography.fernet import Fernet as F
from random import choice, randint
from string import ascii_letters, digits
import threading as t

print("\nStarting installer...")
print("Please wait...")

# Used for getting files when using one-file mode
def getTrueFilename(filename):
    try:
        base = _MEIPASS
    except Exception:
        base = abspath(".")
    return join(base, filename)

# Open the Encryptext.py file and read it into a variable
file = open(getTrueFilename("Encryptext.pyw"), "r", encoding="utf8")
file = file.read()

# Find where the encryption key is stored in the file
file = file.split("# ENCRYPTION KEY HERE")

# Create a key and remove the b'' from the string
key = str(F.generate_key()).split("'")[1]

# Add the key to the file
key_line = file[1]
key_line = key_line.split("'")
key_line[1] = key
key_line = "'".join(key_line)
file[1] = key_line

text = "".join(file)

print("Encryption key created!")

possible_characters = ascii_letters + digits

# Find where the format item separator string is stored in the file
file = text.split("# FORMAT ITEM SEPARATOR HERE")

# Create a format item separator string
format_item_separator = "".join([choice(possible_characters) for i in range(randint(15, 45))])
# Add the format item separator string to the file
key_line = file[1]
key_line = key_line.split("'")
key_line[1] = format_item_separator
key_line = "'".join(key_line)
file[1] = key_line

text = "".join(file)

# Find where the format separator string is stored in the file
file = text.split("# FORMAT SEPARATOR HERE")

# Create a format separator string
format_separator = "".join([choice(possible_characters) for i in range(randint(15, 45))])

# Add the format separator string to the file
key_line = file[1]
key_line = key_line.split("'")
key_line[1] = format_separator
key_line = "'".join(key_line)
file[1] = key_line

text = "".join(file)

# Find where the format string is stored in the file
file = text.split("# FORMAT STRING HERE")

# Create a format string
format_string = "".join([choice(possible_characters) for i in range(randint(15, 45))])

# Add the format string to the file
key_line = file[1]
key_line = key_line.split("'")
key_line[1] = format_string
key_line = "'".join(key_line)
file[1] = key_line

text = "".join(file)

# Write the file back to the Encryptext.py file
file = open(getTrueFilename("Encryptext-User.pyw"), "w", encoding="utf8")
file.write(text)
file.close()

print("Format strings created!")
print("Creating custom program...\n\n")

# Creates an executable file
def appCreation():
    file_path = getTrueFilename("Encryptext-User.pyw")
    icon_path = getTrueFilename("app_icon.ico")
    # https://stackoverflow.com/a/72523249
    # https://stackoverflow.com/a/13790741
    # https://stackoverflow.com/a/8529412
    check_call(["pyinstaller",
                "--onefile",
                "--clean",
                "--windowed",
                "--log-level",
                "FATAL",
                "--icon",
                icon_path,
                f"--add-data={icon_path}:.",
                "--name",
                "Encryptext",
                file_path
               ],
            #    shell=True,
               stdout=open(devnull, 'wb'),
               stderr=open(devnull, 'wb'))

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

# Start thread to create app
app_thread = t.Thread(target=appCreation)
app_thread.start()

# Show a progress bar while app is compiling
l = 100
i = 0
printProgressBar(i, l, prefix='Progress:', suffix='Complete', length=50)
while i < l-25:
    sleep(0.5)
    i += 1
    printProgressBar(i, l, prefix='Progress:', suffix='Complete', length=50, printEnd='')

app_thread.join()

while i < l:
    sleep(0.05)
    i += 1
    printProgressBar(i, l, prefix='Progress:', suffix='Complete', length=50, printEnd='')

# Moves the exe out of the dist folder
system("mv dist/Encryptext Encryptext")

print("\r\n\nCreated program!")
print("Cleaning up...")

# Removes the "dist" folder
system("rm -rf dist")
# Removes the "build" folder
system("rm -rf build")
# Removes the "Encryptext-User.spec" file
system("rm Encryptext.spec")

input("\nCompleted! Press enter to finish setup...")
