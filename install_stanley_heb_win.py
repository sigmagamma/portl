from file_tools import FileTools,steam_path_windows
answer = input("This is an alpha version. By proceeding you acknowledge you are responsible for running this. Press y to install, u to uninstall")
if answer == "y":
    ft = FileTools("The Stanley Parable",steam_path_windows(),"hebrew")
    ft.write_files()
elif answer == 'u':
    ft = FileTools("The Stanley Parable", steam_path_windows(), "hebrew")
    ft.remove_mod_folder()
