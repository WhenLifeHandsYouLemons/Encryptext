import os

password = input("\nWhat is the password? ")
if password == "password":
    loop = True
    if not os.path.exists("C:/Users/2005s/Documents/Visual Studio Code/Python/Tkinter/Custom-Text-Editor/"):
        os.makedirs("C:/Users/2005s/Documents/Visual Studio Code/Python/Tkinter/Custom-Text-Editor/")
else:
    loop = False

while loop == True:
    task = input("\nWhat would like to do?    New    View    Write/Edit    Exit    : ")
    if task == "New":
        new_file_name = input("\nWhat's the name of the file to be created? ")
        open(f"C:/Users/2005s/Documents/Visual Studio Code/Python/Tkinter/Custom-Text-Editor/{new_file_name}.ctetv", "w+")
        print("\nCreated new note.")
    elif task == "View":
        open_file_name = input("\nWhat's the name of the file to be opened? ")
        try:
            with open(f"C:/Users/2005s/Documents/Visual Studio Code/Python/Tkinter/Custom-Text-Editor/{open_file_name}.ctetv", "r") as f:
                content = f.read()
                lines = content.split(" /n ")
                showing = "\n".join(lines)

            print(f"\nViewing 'C:/Users/2005s/Documents/Visual Studio Code/Python/Tkinter/Custom-Text-Editor/{open_file_name}.ctetv'.")
            print("--------------------------------------------------")
            print(showing)
            print("--------------------------------------------------\n")
            opened = True
        except:
            print("\nSorry, there's no such file with that name.")
    elif task == "Write" or task == "Edit":
        edit_file_name = input("\nWhat's the name of the file to be edited? ")
        written = input("Write what you want to save. Use '/n' to add a line break in between. \n\n")
        print("/n")
        with open(f"C:/Users/2005s/Documents/Visual Studio Code/Python/Tkinter/Custom-Text-Editor/{edit_file_name}.ctetv", "w") as f:
            f.write(written)
        print("\nSaved succesfully!")
    elif task == "Exit":
        loop = False
    else:
        print("\nThat's not a valid command please try again.")
