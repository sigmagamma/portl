from src.file_tools import FileTools
import sys


def arabic_ltr_install():
    ft = FileTools("gamefiles/blackmesa/Black Mesa Arabic.json", "uarabic", store="Steam",unattended=True)
    ft.write_files()
def arabic_rtl_install():
    ft = FileTools("gamefiles/blackmesa/Black Mesa Arabic RTL.json", "uarabic", store="Steam",unattended=True)
    ft.write_files()
def hindi_ltr_install():
    ft = FileTools("gamefiles/blackmesa/Black Mesa Hindi.json", "hindi", store="Steam",unattended=True)
    ft.write_files()
def hebrew_ltr_install():
    ft = FileTools("gamefiles/blackmesa/Black Mesa Hebrew.json", "hebrew", store="Steam",unattended=True)
    ft.write_files()
def hebrew_rtl_install():
    ft = FileTools("gamefiles/blackmesa/Black Mesa Hebrew RTL.json", "hebrew", store="Steam",unattended=True)
    ft.write_files()

def uninstall():
    ft = FileTools("gamefiles/blackmesa/Black Mesa Hebrew RTL.json","hebrew", store="Steam",unattended=True)
    ft.remove_mod()

if __name__ == '__main__':
    globals()[sys.argv[1]]()
