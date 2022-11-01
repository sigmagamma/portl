from src.file_tools import FileTools
import sys
from src import legacy_backup_tools as lbt

def hebrew_ltr_install():
    ft = FileTools("gamefiles/portal/Portal.json", "hebrew", store="Steam",unattended=True)
    lbt.restore_backup(ft)
    ft.write_files()
def hebrew_rtl_install():
    ft = FileTools("gamefiles/portal/Portal RTL.json", "hebrew", store="Steam",unattended=True)
    lbt.restore_backup(ft)
    ft.write_files()

def uninstall():
    ft = FileTools("gamefiles/portal/Portal RTL.json","hebrew", store="Steam",unattended=True)
    ft.remove_mod()

if __name__ == '__main__':
    globals()[sys.argv[1]]()
