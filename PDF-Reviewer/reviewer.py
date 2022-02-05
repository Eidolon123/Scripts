import os

dir_string = "path_to_directory_of_PDFS"

directory = os.fsencode(dir_string)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    os.system(f"firefox {dir_string}{filename}")
    print(f"Currently viewing file: {filename}")
    keep = input("Would you like to keep this file? y/n\n")
    while True:
        if keep == "y":
            break
        elif keep == "n":
            os.remove(os.fsencode(f"{dir_string}{filename}"))
            print(f"File '{filename}' has been deleted.")
            break
        else:
            print("invalid option try y or n")
            continue
