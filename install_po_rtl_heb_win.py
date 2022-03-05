from file_tools import FileTools,steam_path_windows
import legacy_backup_tools as lbt
answer = input("This is an alpha version. By proceeding you acknowledge you are responsible for running this. Press y to install, u to uninstall")
if answer == "y":
    ft = FileTools("Portal",steam_path_windows(),"hebrew")
    lbt.restore_backup(ft)
    ft.write_files()
elif answer == 'u':
    ft = FileTools("Portal", steam_path_windows(), "hebrew")
    ft.remove_mod()

