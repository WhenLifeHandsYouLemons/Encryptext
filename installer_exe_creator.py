import os
# TODO: Need to adjust this

# Creates an executable file
os.system("pyinstaller --onefile --windowed Encryptext-User.py")
# Removes the "build" folder
os.system("rmdir /s /q build")
# Removes the "Encryptext-User.spec" file
os.system("del Encryptext-User.spec")
# Moves the exe out of the dist folder
os.system("move dist\\Encryptext-User.exe Encryptext-User.exe")
# Removes the "dist" folder
os.system("rmdir /s /q dist")
