#!/usr/bin/python'

from os import rename, path, remove
from shutil import rmtree
import hashlib

import PyInstaller.__main__

version = "1.9.0"

# Compute hash of the input string
def computeHash(input_string):
    hash_object = hashlib.sha256()
    hash_object.update(input_string.encode('utf-8'))

    return hash_object.hexdigest()

# Open the key.txt file and read in the key
with open("Original Files/key.txt", "r") as file:
    key = file.read().strip()
# Compute the hash of the key
hash_str = computeHash(key)

# Add the computed hash
with open("encryptext_installer.py", "r+") as file:
    installer_file = file.read()
    installer_parts = installer_file.split("INSERT COMPUTED HASH HERE")
    installer_file = hash_str.join(installer_parts)
    file.seek(0)
    file.write(installer_file)
    file.truncate()

# Creates an executable file
PyInstaller.__main__.run([
    'encryptext_installer.py',
    '--onefile',
    '--clean',
    '--log-level',
    'ERROR',
    '--icon',
    'app_icon.ico',
    '--add-data',
    'app_icon.ico;.',
    '--add-data',
    'Encryptext.pyw;.',
    "--collect-all",
    "tkinterweb",
    "--collect-all",
    "alive_progress",
    "--collect-all",
    "grapheme"
])

# Remove the computed hash
with open("encryptext_installer.py", "r+") as file:
    installer_file = file.read()
    installer_parts = installer_file.split(hash_str)
    installer_file = "INSERT COMPUTED HASH HERE".join(installer_parts)
    file.seek(0)
    file.write(installer_file)
    file.truncate()

# Move the exe out of the dist folder
remove(f"encryptext_installer_v{version}_64bit.exe")
rename(path.join("dist", "encryptext_installer.exe"), f"encryptext_installer_v{version}_64bit.exe")

# Remove pyinstaller folders and files
rmtree("dist")
rmtree("build")
remove("encryptext_installer.spec")
