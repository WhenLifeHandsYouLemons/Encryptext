from os import system
import PyInstaller.__main__

# Creates an executable file
PyInstaller.__main__.run([
    'installer_linux.py',
    '--onefile',
    '--clean',
    '--log-level',
    'FATAL',
    '--icon',
    'installer_icon.ico',
    '--add-data=app_icon.ico:.',
    '--add-data=Encryptext.pyw:.'
])
# Moves the exe out of the dist folder
system("mv dist/installer_linux encryptext_installer_v0.0.0_linux")

# Removes the "build" folder
system("rm -rf build")
# Removes the "installer.spec" file
system("rm installer_linux.spec")
# Removes the "dist" folder
system("rm -rf dist")
