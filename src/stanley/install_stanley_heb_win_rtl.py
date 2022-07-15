from src.file_tools import FileTools
answer = input("This is an alpha version. By proceeding you acknowledge you are responsible for running this. Press y to install, u to uninstall, any other key to quit")
try:
    if answer == "y":
        ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json", "hebrew")
        ft.write_files()
    elif answer == 'u':
        ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json", "hebrew")
        ft.remove_mod()
except Exception as e:
    input("installer crashed with an error:\n"+e)
    exit()
if answer == 'y' or 'u':
    input("Done, press any key to quit.")

