# portl
Portal 1 translation tool for right-to-left languages

This repository does not include any file with actual source or translation material from the game.
In order to run this you'll need to put either:

1. closecaption_hebrew.dat and portal_english.txt that already contain the hebrew translation OR
2. Portal translation - additions.csv and Portal translation - closedcaption.csv
in the same folder.

You can use the spec files with pyinstaller to create executables:
pyinstaller remove_po_rtl_heb_win.spec
pyinstaller install_po_rtl_heb_win.spec