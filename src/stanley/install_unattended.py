from src.file_tools import FileTools
import sys

def epic_male():
    ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json", "hebrew", "m", "Epic",unattended=True)
    ft.write_files()
def epic_female():
    ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json", "hebrew", "f", "Epic",unattended=True)
    ft.write_files()
def epic_uninstall():
    ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json","hebrew", store="Epic",unattended=True)
    ft.remove_mod()
def steam_male():
    ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json", "hebrew", "m", "Steam",unattended=True)
    ft.write_files()
def steam_female():
    ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json", "hebrew", "f", "Steam",unattended=True)
    ft.write_files()
def steam_uninstall():
    ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json","hebrew", store="Steam",unattended=True)
    ft.remove_mod()

if __name__ == '__main__':
    globals()[sys.argv[1]]()
