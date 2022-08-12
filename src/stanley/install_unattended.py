from src.file_tools import FileTools
def epic_male():
    ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json", "hebrew", "m", "Epic",unattended=True)
    ft.write_files()
def epic_female():
    ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json", "hebrew", "f", "Epic",unattended=True)
    ft.write_files()
def epic_uninstall():
    ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json","hebrew", "Epic",unattended=True)
    ft.remove_mod()
def steam_male():
    ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json", "hebrew", "m", "Steam",unattended=True)
    ft.write_files()
def steam_female():
    ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json", "hebrew", "f", "Steam",unattended=True)
    ft.write_files()
def steam_uninstall():
    ft = FileTools("gamefiles/stanley/The Stanley Parable RTL.json","hebrew", "Steam",unattended=True)
    ft.remove_mod()