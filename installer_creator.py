from os import rename, path, remove
from shutil import rmtree
import PyInstaller.__main__

version = "1.8.0"

# Creates an executable file
PyInstaller.__main__.run([
    'encryptext_installer.py',
    '--onefile',
    '--clean',
    '--log-level',
    'ERROR',
    '--icon',
    'installer_icon.ico',
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

# Move the exe out of the dist folder
remove(f"encryptext_installer_v{version}_64bit.exe")
rename(path.join("dist", "encryptext_installer.exe"), f"encryptext_installer_v{version}_64bit.exe")

# Remove pyinstaller folders
rmtree("dist")
rmtree("build")
