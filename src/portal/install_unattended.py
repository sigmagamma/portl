from src.file_tools import FileTools
import sys
from src import legacy_backup_tools as lbt

def hebrew_rtx_ltr_install():
    ft = FileTools("gamefiles/portal/Portal RTX.json", "hebrew", store="Steam",unattended=True)
    lbt.restore_backup(ft)
    ft.write_files()
def hebrew_rtx_rtl_install():
    ft = FileTools("gamefiles/portal/Portal RTX RTL.json", "hebrew", store="Steam",unattended=True)
    lbt.restore_backup(ft)
    ft.write_files()

def hebrew_2007_ltr_install():
    ft = FileTools("gamefiles/portal/Portal 2007.json", "hebrew", store="Steam",unattended=True)
    lbt.restore_backup(ft)
    ft.write_files()
def hebrew_2007_rtl_install():
    ft = FileTools("gamefiles/portal/Portal 2007 RTL.json", "hebrew", store="Steam",unattended=True)
    lbt.restore_backup(ft)
    ft.write_files()
def resizer_2007_install():
    ft = FileTools("gamefiles/portalresizer/Portal 2007 resizer.json", "hebrew", store="Steam",unattended=True)
    ft.write_files()

def resizer_rtx_install():
    ft = FileTools("gamefiles/portalresizer/Portal RTX resizer.json", "hebrew", store="Steam",unattended=True)
    ft.write_files()
def uninstall_2007():
    ft = FileTools("gamefiles/portal/Portal 2007 RTL.json","hebrew", store="Steam",unattended=True)
    ft.remove_mod()
def uninstall_rtx():
    ft = FileTools("gamefiles/portal/Portal RTX RTL.json","hebrew", store="Steam",unattended=True)
    ft.remove_mod()
if __name__ == '__main__':
    globals()[sys.argv[1]]()
