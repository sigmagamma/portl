# poRTL
Portal 1 translation tool for right-to-left languages

This project was created for the Portal 1 Hebrew fan translation, details on which (in Hebrew) you can find here:

https://www.facebook.com/groups/200491360554968/posts/868793153724782

Or in English here:

https://steamcommunity.com/sharedfiles/filedetails/?id=2554472476

## What this does
* Portal 1 has translations for several languages for subtitles and close captions (the closecaption file)
as well as other texts (the portal file). However, it does not support right to left languages,
and when creating translations for those text appears out of order. 
* The program takes a translation file and the source english file and generates relevant content for the RTL language,
along the way solving the order issue so that the text is readable. It does not handle right-to-left alignment of the text (yet).
* For the "portal" file, which contains the song, an even simpler approach is taken which doesn't
consider multiple lines. Note that this means some lines need to be out of order in the translation file.
* Finally, the program installs the content into the Portal folder and configures Portal to use it, with some effort made to back up previous files.
There is also a removal program to allow restoring the state prior to running the program.

## Windows Hebrew installation
This repository does not include any file with actual source or translation material from the game.
In order to run this you'll need to put either:

1. closecaption_hebrew.dat and portal_english.txt that already contain the hebrew translation OR
2. Portal translation - additions.csv and Portal translation - closedcaption.csv
in the same folder.

You can then run install_po_rtl_heb_win.py for a windows installation.
remove_po_rtl_heb_win.py removes an existing windows installation.

You can use the spec files with pyinstaller to create executables:

`pyinstaller remove_po_rtl_heb_win.spec`

`pyinstaller install_po_rtl_heb_win.spec`

You will have to have closecaption_hebrew.dat and portal_english.txt created
by the script in the same folder when running pyinstaller.

## Development setup
1. Get Portal: 
https://store.steampowered.com/app/400/Portal/
2. Get an IDE for editing python such as [Pycharm](https://www.jetbrains.com/pycharm/)
3. git clone https://github.com/sigmagamma/portl.git
4. If you want to change the actual translation, put the relevant csvs in the project folder. Otherwise, if you want to work with an existing translation and patch the game, put the modified `closecaption_hebrew.dat` and `portal_english.txt` in the project folder.
5. `text_tools.py` contains the text transformation logic, while `file_tools.py` contains filesystem logistics. `install_po_rtl_heb_win.py` and `remove_po_rtl_heb_win.py` perform the patching for windows.
6. Once you've applied the patch, run the game. You should be able to see subtitles
in Hebrew - if not, try manually applying the `autoexec.cfg` settings in the Portal console
(runnable by using \`): `cc_lang hebrew` and `cc_subtitles 1` . Notice that reapplying the patch requires a restart of the game to work.
7. If you want to work on the right-aligned version, checkout branch `feat-right-align` first. 

