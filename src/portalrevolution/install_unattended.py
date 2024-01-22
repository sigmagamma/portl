from src.file_tools import FileTools
import sys
from src import legacy_backup_tools as lbt

def hebrew_ltr_install():
    ft = FileTools("gamefiles/portalrevolution/Portal Revolution.json", "hebrew", store="Steam",unattended=True)
    ft.write_files()
def hebrew_rtl_install():
    ft = FileTools("gamefiles/portalrevolution/Portal Revolution RTL.json", "hebrew", store="Steam",unattended=True)
    ft.write_files()

def uninstall():
    ft = FileTools("gamefiles/portalrevolution/Portal Revolution.json","hebrew", store="Steam",unattended=True)
    ft.remove_mod()

if __name__ == '__main__':
    globals()[sys.argv[1]]()
