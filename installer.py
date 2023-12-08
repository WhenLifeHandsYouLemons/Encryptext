import os
from cryptography.fernet import Fernet

print("Starting installer...")
print("Please wait...")

# Open the Encryptext.py file and read it into a variable
file = open("Encryptext.pyw", "r", encoding="utf8")
file = file.read()

# Find where the encryption key is stored in the file
file = file.split("# ENCRYPTION KEY HERE")

# Create a key and remove the b'' from the string
key = str(Fernet.generate_key()).split("'")[1]

# Add the key to the file
key_line = file[1]
key_line = key_line.split("'")
key_line[1] = key
key_line = "'".join(key_line)
file[1] = key_line

text = "# ENCRYPTION KEY HERE".join(file)

# Write the file back to the Encryptext.py file
file = open("Encryptext-User.pyw", "w", encoding="utf8")
file.write(text)
file.close()

print("Encryption key created!")
print("Creating custom program...\n\n")

# Creates an executable file
# https://stackoverflow.com/a/72523249
# https://stackoverflow.com/a/13790741
os.system('pyinstaller --onefile --clean --windowed --log-level ERROR --icon="app_icon.ico" --add-data "app_icon.ico;." --name Encryptext Encryptext-User.pyw')
# Moves the exe out of the dist folder
os.system("move dist\\Encryptext.exe Encryptext.exe")

print("\n\nCreated program!")
print("Cleaning up...")

# Removes the "dist" folder
os.system("rmdir /s /q dist")
# Removes the "build" folder
os.system("rmdir /s /q build")
# Removes the "Encryptext-User.spec" file
os.system("del Encryptext.spec")
# Remove the "Encryptext-User.pyw" file
os.system("del Encryptext-User.pyw")
# Remove the "Encryptext.pyw" file
os.system("del Encryptext.pyw")
# Remove the app_icon.ico file
os.system("del app_icon.ico")

input("\nCompleted! Press enter to finish setup...")
