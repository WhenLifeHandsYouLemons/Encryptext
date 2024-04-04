#!/usr/bin/python'

from os import rename, path, remove
from shutil import rmtree
import hashlib
import PyInstaller.__main__

def update_build_number():
    with open("Original Files/build_number.txt", "r") as file:
        build_number = int(file.read().strip())
    build_number += 1
    with open("Original Files/build_number.txt", "w") as file:
        file.write(str(build_number))
    return build_number

version = "1.9.1"
build_number = update_build_number()
version = f"{version}.{build_number}"

# Compute hash of the input string
def computeHash(input_string: str) -> str:
    hash_object = hashlib.sha256()
    hash_object.update(input_string.encode('utf-8'))

    return hash_object.hexdigest()

def modifyInstallerFile(add: bool) -> None:
    if add:
        # Add the computed hash and version number
        with open("encryptext_installer.py", "r+") as file:
            installer_file = file.read()
            installer_parts = installer_file.split("INSERT COMPUTED HASH HERE")
            installer_file = hash_str.join(installer_parts)
            installer_parts = installer_file.split("INSERT VERSION NUMBER HERE")
            installer_file = version.join(installer_parts)

            file.seek(0)
            file.write(installer_file)
            file.truncate()
    else:
        # Remove the computed hash and version number
        with open("encryptext_installer.py", "r+") as file:
            installer_file = file.read()
            installer_parts = installer_file.split(hash_str)
            installer_file = "INSERT COMPUTED HASH HERE".join(installer_parts)
            installer_parts = installer_file.split(version)
            installer_file = "INSERT VERSION NUMBER HERE".join(installer_parts)

            file.seek(0)
            file.write(installer_file)
            file.truncate()

# Open the key.txt file and read in the key
with open("Original Files/key.txt", "r") as file:
    key = file.read().strip()
# Compute the hash of the key
hash_str = computeHash(key)

# Add hash and version
modifyInstallerFile(True)

try:
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
except Exception as e:
    print("Stopped for:", e)

    # Remove hash and version
    modifyInstallerFile(False)

    # Remove pyinstaller folders and files
    rmtree("dist")
    rmtree("build")
    remove("encryptext_installer.spec")

    exit()

# Remove hash and version
modifyInstallerFile(False)

# Move the exe out of the dist folder
rename(path.join("dist", "encryptext_installer.exe"), f"encryptext_installer_v{version}_64bit.exe")

# Remove pyinstaller folders and files
rmtree("dist")
rmtree("build")
remove("encryptext_installer.spec")
