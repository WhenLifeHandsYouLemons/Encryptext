from os import system
import PyInstaller.__main__

# Creates an executable file
PyInstaller.__main__.run([
    'installer_windows.py',
    '--onefile',
    '--clean',
    '--log-level',
    'CRITICAL',
    '--icon',
    'installer_icon.ico',
    '--add-data',
    'app_icon.ico;.',
    '--add-data',
    'Encryptext.pyw;.'
])
# Moves the exe out of the dist folder
system("move dist\\installer_windows.exe encryptext_installer_v0.0.0_64bit.exe")

# Removes the "build" folder
system("rmdir /s /q build")
# Removes the "installer.spec" file
system("del installer_windows.spec")
# Removes the "dist" folder
system("rmdir /s /q dist")
