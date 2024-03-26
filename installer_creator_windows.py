from os import system
import PyInstaller.__main__

version = "1.7.3"

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
    "tkinterweb"
])

# Move the exe out of the dist folder
system(f"move dist\\encryptext_installer.exe encryptext_installer_v{version}_64bit.exe")

# Remove pyinstaller folders
system("rmdir /s /q build")
system("rmdir /s /q dist")
