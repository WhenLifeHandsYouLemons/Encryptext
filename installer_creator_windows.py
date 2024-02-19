from os import system
import PyInstaller.__main__

version = "1.6.0"

# Creates an executable file
PyInstaller.__main__.run([
    'installer_windows.py',
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
    "tkinterweb"
])

# Moves the exe out of the dist folder
system(f"move dist\\installer_windows.exe encryptext_installer_v{version}_64bit.exe")

# Removes the "build" folder
system("rmdir /s /q build")
# Removes the "dist" folder
system("rmdir /s /q dist")
