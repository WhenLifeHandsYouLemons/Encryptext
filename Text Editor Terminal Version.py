import os

password = input("\nWhat is the password? ")
if password == "":
    loop = True
    if not os.path.exists("C:/Editor/Notes/"):
        os.makedirs("C:/Editor/Notes/")
else:
    loop = False

while loop == True:
    task = input("\nWhat would like to do?    New    View    Write/Edit    Exit    : ")
    if task == "New":
        new_file_name = input("\nWhat is the name of the file to be created? ")
        open(f"C:/Editor/Notes/{new_file_name}.ctetv", "w+")
        print("\nCreated new note.")
    elif task == "View":
        open_file_name = input("\nWhat is the name of the file to be opened? ")
        try:
            with open(f"C:/Editor/Notes/{open_file_name}.ctetv", "r") as f:
                content = f.read()
                lines = content.split(" /n ")
                showing = "\n".join(lines)

            print(f"\nViewing 'C:/Editor/Notes/{open_file_name}.ctetv'.")
            print("--------------------------------------------------")
            print(showing)
            print("--------------------------------------------------\n")
            opened = True
        except:
            print("\nSorry, there is no such file with that name.")
    elif task == "Write" or task == "Edit":
        edit_file_name = input("\nWhat is the name of the file to be edited? ")
        written = input("Write what you want to save. Use '/n' to add a line break in between. \n\n")
        print("/n")
        with open(f"C:/Editor/Notes/{edit_file_name}.ctetv", "w") as f:
            f.write(written)
        print("\nSaved succesfully!")
    elif task == "Exit":
        loop = False
    else:
        print("\nThat is not a valid command please try again.")
