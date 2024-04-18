#!/usr/bin/python'

from os import rename, path
from shutil import rmtree, copy
import hashlib
import PyInstaller.__main__

version = "1.9.3"
testing = False

def update_build_number() -> str:
    with open("builds/build_number.txt", "r") as file:
        build_number = int(file.read().strip())
    build_number += 1
    with open("builds/build_number.txt", "w") as file:
        file.write(str(build_number))
    return build_number

build_number = update_build_number()
version = f"{version}.{build_number}"

# Compute hash of the input string
def computeHash(input_string: str) -> str:
    hash_object = hashlib.sha256()
    hash_object.update(input_string.encode('utf-8'))

    return hash_object.hexdigest()

def modifyInstallerFile(add: bool) -> None:
    with open("encryptext_installer.py", "r+") as file:
        installer_file = file.read()

        if add:
            # Add the computed hash and version number
            installer_parts = installer_file.split("INSERT COMPUTED HASH HERE")
            installer_file = hash_str.join(installer_parts)
            installer_parts = installer_file.split("INSERT VERSION NUMBER HERE")
            installer_file = version.join(installer_parts)
        else:
            # Remove the computed hash and version number
            installer_parts = installer_file.split(hash_str)
            installer_file = "INSERT COMPUTED HASH HERE".join(installer_parts)
            installer_parts = installer_file.split(version)
            installer_file = "INSERT VERSION NUMBER HERE".join(installer_parts)

        file.seek(0)
        file.write(installer_file)
        file.truncate()

def changeDebug(file_name: str, debug: bool) -> None:
    with open(f".venv/Lib/site-packages/ttkbootstrap/{file_name}", "r+") as file:
        lines = file.read()
        lines = f"debug = {debug}".join(lines.split(f"debug = {not debug}"))
        file.seek(0)
        file.write(lines)
        file.truncate()

# Open the key.txt file and read in the key
with open("Original Files/key.txt", "r") as file:
    key = file.read().strip()
# Compute the hash of the key
hash_str = computeHash(key)

# Add hash and version
modifyInstallerFile(True)

# Open the ttkbootstrap's files and change debug to False
changeDebug("style.py", False)

try:
    # Creates an executable file
    PyInstaller.__main__.run([
        'encryptext_installer.py',
        '--onefile',
        '--clean',
        '--log-level',
        'INFO',
        '--icon',
        'app_icon.ico',
        '--add-data',
        'app_icon.ico;.',
        '--add-data',
        'Encryptext.pyw;.',
        '--add-data',
        '.venv/Lib/site-packages/ttkbootstrap;ttkbootstrap',
        '--add-data',
        '.venv/Lib/site-packages/tkinter;tkinter',
        "--collect-all",
        "tkinterweb",
        "--collect-all",
        "alive_progress",
        "--collect-all",
        "grapheme"
    ])
except Exception as e:
    print("Stopped for:", e)

    # Remove hash and version
    modifyInstallerFile(False)

    # Open the ttkbootstrap's files and change debug to True
    changeDebug("style.py", True)

    # Remove pyinstaller folders and files
    rmtree("dist")
    rmtree("build")

    exit()

# Remove hash and version
modifyInstallerFile(False)

# Move the exe out of the dist folder
if testing:
    rename(path.join("dist", "encryptext_installer.exe"), f"builds/testing/encryptext_installer_v{version}_64bit.exe")
else:
    copy(path.join("dist", "encryptext_installer.exe"), f"builds/testing/encryptext_installer_v{version}_64bit_release.exe")
    version = '.'.join(version.split('.')[0:-1])
    rename(path.join("dist", "encryptext_installer.exe"), f"builds/release/encryptext_installer_v{version}_64bit.exe")

# Open the ttkbootstrap's files and change debug to True
changeDebug("style.py", True)

# Remove pyinstaller folders and files
rmtree("dist")
rmtree("build")
