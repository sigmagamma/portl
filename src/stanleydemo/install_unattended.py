from src.file_tools import FileTools
import sys

def steam_male():
    ft = FileTools("gamefiles/stanleydemo/The Stanley Parable Demo RTL.json", "hebrew", "m", "Steam",unattended=True)
    ft.write_files()
def steam_female():
    ft = FileTools("gamefiles/stanleydemo/The Stanley Parable Demo RTL.json", "hebrew", "f", "Steam",unattended=True)
    ft.write_files()
def steam_uninstall():
    ft = FileTools("gamefiles/stanleydemo/The Stanley Parable Demo RTL.json","hebrew", store="Steam",unattended=True)
    ft.remove_mod()

if __name__ == '__main__':
    globals()[sys.argv[1]]()
