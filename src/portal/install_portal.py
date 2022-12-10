from src.file_tools import FileTools
from src import legacy_backup_tools as lbt
import os
def install_po_rtl(filename,language,store,patch):
    ft = FileTools(filename,language,store=store)
    base_text = "This is a beta version. By proceeding you acknowledge you are responsible for running this."+ \
                "\r\nNotice that this will remove previous hebrew patch installations as well as the unofficial size patch. "
    backup_exists = False
    for file_data in ft.other_files:
        if file_data.get('override'):
            if os.path.exists(ft.get_basegame_english_backup_other_path(file_data)):
                backup_exists = True
    if os.path.exists(ft.mod_folder) or backup_exists:
        answer = input(base_text + " Press y to reinstall, u to uninstall")
        if answer == "y":
            lbt.restore_backup(ft)

            if patch:
                ft.write_patch_files()
            else:
                ft.write_files()
        elif answer == 'u':
            ft.remove_mod()
    else:
        answer = input(base_text + " Press y to install")
        if answer == "y":
            lbt.restore_backup(ft)
            if patch:
                ft.write_patch_files()
            else:
                ft.write_files()
    if answer in ['y', 'u']:
        input("Done, press any key to quit.")



