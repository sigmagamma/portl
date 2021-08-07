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
along the way solving the order issue so that the text is readable. It also handles right-to-left alignment for the captions (not for the song).
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

##Right alignment instructions
This branch contains code that supports right alignment for the captions (not for the song). For this to work correctly:
1. It is assumed you're running Windows 10 with Hebrew support, meaning your default system
Hebrew font is Tahoma. 
2. Run applyfonts.reg to change the default font to Miriam Fixed. Restart your PC.
3. When you start the game, set the game resolution to 1920 * 1080

Once you're done playing, to restore the system font to Tahoma run the removefonts.reg file and restart Windows.

This process is required as the game does not support native right to left alignment, and also does not allow setting the font for Hebrew characters. 
 

