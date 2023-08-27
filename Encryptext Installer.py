import os
from cryptography.fernet import Fernet

# Open the Encryptext.py file and read it into a variable
file = open("Encryptext.py", "r", encoding="utf8")
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
file = open("Encryptext-User.py", "w", encoding="utf8")
file.write(text)
file.close()

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
