import os

# Creates an executable file
os.system('pyinstaller --onefile --log-level CRITICAL --icon="installer_icon.ico" installer.py')
# Moves the exe out of the dist folder
os.system("move dist\\installer.exe installer.exe")

# Removes the "build" folder
os.system("rmdir /s /q build")
# Removes the "installer.spec" file
os.system("del installer.spec")
# Removes the "dist" folder
os.system("rmdir /s /q dist")
