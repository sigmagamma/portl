from src.file_tools import FileTools
import sys

def steam_install():
    ft = FileTools("gamefiles/hl2/Half Life 2.json", "uarabic", "m",store="Steam",unattended=True)
    ft.write_files()

def steam_uninstall():
    ft = FileTools("gamefiles/portal2/Half Life 2.json","uarabic", store="Steam",unattended=True)
    ft.remove_mod()

if __name__ == '__main__':
    globals()[sys.argv[1]]()
