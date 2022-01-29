import legacy_backup_tools as lbt
from file_tools import FileTools,steam_path_windows
answer = input("This is an alpha version. Press y to acknowledge you are responsible for running this.")
if answer == "y":
    ft = FileTools("Portal",steam_path_windows(),"hebrew")
    lbt.restore_backup(ft)
    ft.remove_custom_folder()