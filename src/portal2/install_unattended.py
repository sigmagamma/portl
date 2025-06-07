from src.file_tools import FileTools
import sys
from src import legacy_backup_tools as lbt

# def hebrew_ltr_install():
#     ft = FileTools("gamefiles/portal2/Portal2.json", "hebrew", "m",store="Steam",unattended=True)
#     ft.write_files()
def steam_glados_WIN():
    ft = FileTools("gamefiles/portal2/Portal2 RTL.json", "hebrew", "m",store="Steam",unattended=True)
    ft.write_files()
def arabic_steam_glados_WIN():
    ft = FileTools("gamefiles/portal2/Portal2 RTL Arabic.json", "uarabic", "m",store="Steam",unattended=True)
    ft.write_files()

def steam_mabsuta_WIN():
    ft = FileTools("gamefiles/portal2/Portal2 RTL.json", "hebrew", "f",store="Steam",unattended=True)
    ft.write_files()

def steam_glados_linux():
    ft = FileTools("gamefiles/portal2/Portal2 RTL.json", "hebrew", "m",store="Steam",unattended=True,gameos="linux")
    ft.write_files()

def steam_mabsuta_linux():
    ft = FileTools("gamefiles/portal2/Portal2 RTL.json", "hebrew", "f",store="Steam",unattended=True,gameos="linux")
    ft.write_files()

def steam_uninstall():
    ft = FileTools("gamefiles/portal2/Portal2.json","hebrew", store="Steam",unattended=True)
    ft.remove_mod()

if __name__ == '__main__':
    globals()[sys.argv[1]]()
