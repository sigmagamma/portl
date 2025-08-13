from install_portal2 import install_portal2
from sys import argv
sheet = argv[1] if len(argv) > 1 else None
install_portal2("gamefiles/portal2/Portal2 RTL Arabic testers.json", "uarabic", "Steam",sheet=sheet,patch=False)