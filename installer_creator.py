#!/usr/bin/python'

from os import rename, path
from shutil import rmtree, copy
import hashlib
import platform
import PyInstaller.__main__

version = "1.9.4"
testing = True

os_type = platform.system()

def update_build_number() -> str:
    file_path = "builds/build_number.txt"

    with open(file_path, "r") as file:
        build_number = int(file.read().strip())

    build_number += 1

    with open(file_path, "w") as file:
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

def changeDebug(debug: bool) -> None:
    with open(f"to-package/ttkbootstrap/style.py", "r+") as file:
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
changeDebug(False)

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
        'packages/ttkbootstrap;ttkbootstrap',
        '--add-data',
        'packages/tkinter;tkinter',
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
    changeDebug(True)

    # Remove pyinstaller folders and files
    rmtree("dist")
    rmtree("build")

    exit()

# Remove hash and version
modifyInstallerFile(False)

# Move the exe out of the dist folder
if os_type == "Windows":
    end_file_type = "exe"
elif os_type == "Darwin":
    end_file_type = ""
elif os_type == "Linux":
    end_file_type = "bin"
else:
    end_file_type = ""

if testing:
    rename(path.join("dist", f"encryptext_installer.{end_file_type}"), f"builds/testing/{os_type.lower()}/encryptext_installer_v{version}_64bit.{end_file_type}")
else:
    copy(path.join("dist", f"encryptext_installer.{end_file_type}"), f"builds/testing/{os_type.lower()}/encryptext_installer_v{version}_64bit_release.{end_file_type}")
    version = '.'.join(version.split('.')[0:-1])
    rename(path.join("dist", f"encryptext_installer.{end_file_type}"), f"builds/release/{os_type.lower()}/encryptext_installer_v{version}_64bit.{end_file_type}")

# Open the ttkbootstrap's files and change debug to True
changeDebug(True)

# Remove pyinstaller folders and files
rmtree("dist")
rmtree("build")
