from file_tools import FileTools,steam_path_windows
import legacy_backup_tools as lbt
import os
ft = FileTools("Portal",steam_path_windows(),"hebrew")
base_text = "This is an alpha version. By proceeding you acknowledge you are responsible for running this."+ \
            "\r\nNotice that this will remove previous hebrew patch installations as well as the unofficial size patch. "
if os.path.exists(ft.mod_folder):
    answer = input(base_text + " Press y to reinstall, u to uninstall")
    if answer == "y":
        lbt.restore_backup(ft)
        ft.write_files()
    elif answer == 'u':
        ft.remove_mod()
else:
    answer = input(base_text + " Press y to install")
    if answer == "y":
        lbt.restore_backup(ft)
        ft.write_files()


