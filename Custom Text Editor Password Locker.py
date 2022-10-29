import shutil
import os

tries = 5

settings = []
with open("/home/sooraj/Desktop/Python/Tkinter/Custom-Text-Editor/Settings.txt", "r") as f:
    content = f.read()
    lines = content.splitlines()
    for line in lines:
        settings.append(line)

if settings[0] == "firstTimeOpeningApp=False":
    while tries != 0:
        password = input("\nWhat is the password? ")
        # if password == "bJLJB-dmfRBti4Z1eLoFLLIFZaqvoxKUf09Aq51c-FY=":
        if password == "password":
            os.system("python3 'Custom Text Editor Interface Edition.py'")
            # execfile("Custom Text Editor Interface Edition.py")
        else:
            print("\nWrong password!")
            print(f"You have {tries - 1} tries left.")
            tries = tries - 1
else:
    while True:
        chosen_password = input("\nWhat would you like the password for this application to be? Any characters are allowed. ")
        repeated_password = input("\nPlease retype your password to confirm it. ")
        if chosen_password == repeated_password:
            False
        else:
            print("Sorry, the passwords don't match. Please try again.")


print("You have run out of tries! Please wait for __ minutes before continuing.")
