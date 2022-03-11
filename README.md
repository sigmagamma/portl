# poRTL
Source engine translation tool for right-to-left languages
Currently Portal 1 is supported. Current working branch is [feat-stanley](https://github.com/sigmagamma/portl/tree/feat-stanley). If you want to start working on a new game, checkout that branch and then create a new one out of it. 
Snapshot branches for Portal release are [portal-0.9.0-left-align](https://github.com/sigmagamma/portl/tree/portal-0.9.0-left-align) and [portal-0.9.0-right-align](https://github.com/sigmagamma/portl/tree/portal-0.9.0-right-align) .

see https://github.com/sigmagamma/portl/issues/6 for details on other games.


This project was originally created for the Portal 1 Hebrew fan translation, details on which (in Hebrew) you can find here:

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

## Windows Hebrew installation for Portal
This repository does not include any file with actual source or translation material from the game.
In order to run this you'll need to put either:

1. closecaption_hebrew.dat and portal_hebrew.txt that already contain the hebrew translation OR
2. Portal translation - additions.csv and Portal translation - closecaption.csv
in the same folder.

You can then run install_po_rtl_heb_win.py for a windows installation.

You can use the spec files with pyinstaller to create the executable.
However, in windows you may have to compile pyinstaller on your machine to do so to avoid the executable being flagged by AV software.
See this guide:
https://python.plainenglish.io/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184
Some additional points to follow: 
Within the Visual Studio Installer, make sure you add "Desktop development with C++".
In step 5, if you're working with Pycharm, you should probably copy the release into the project folder in order to have it install pyinstaller into your Virtual Environment.
Also you may have to to run Pycharm as administrator.

Once Pyinstaller is installed into your environment,modify the path for the portalhebrew folder within the file. Then run 

`pyinstaller --clean install_po_rtl_heb_win.spec`

You will have to have closecaption_hebrew.dat and portal_hebrew.txt created
by the script in the same folder when running pyinstaller.

## Development setup - Portal
1. Get Portal: 
https://store.steampowered.com/app/400/Portal/
2. Get an IDE for editing python such as [Pycharm](https://www.jetbrains.com/pycharm/)
3. git clone https://github.com/sigmagamma/portl.git
4. If you want to change the actual translation, put the relevant csvs in the project folder. 
These have to be named "Portal translation - closecaption.csv" and "Portal translation - portal.csv."
Otherwise, if you want to work with an existing translation and patch the game, put the modified `closecaption_hebrew.dat` and `portal_hebrew.txt` in the project folder.
5. `text_tools.py` contains the text transformation logic, while `file_tools.py` contains filesystem logistics. `install_po_rtl_heb_win.py` performs the patching for windows.
6. Once you've applied the patch, run the game. You should be able to see subtitles
in Hebrew - if not, try manually applying the `autoexec.cfg` settings in the Portal console
(runnable by using \`): `cc_lang hebrew` and `cc_subtitles 1` . Notice that reapplying the patch requires a restart of the game to work.
7. If you want to work on the right-aligned version, checkout branch https://github.com/sigmagamma/portl/tree/feat-right-align first. 

## Development setup - Stanley Parable

1. Get Stanley Parable:
https://store.steampowered.com/app/221910/The_Stanley_Parable/
(Epic not supported yet)
2. Get an IDE for editing python such as [Pycharm](https://www.jetbrains.com/pycharm/)
3. git clone https://github.com/sigmagamma/portl.git
4. If you want to change the actual translation, put the relevant csv in the project folder. 
It has to be named "The Stanley Parable translation - subtitles.csv".
For this mode you have to get an additional game that has captioncompiler, like Portal or Portal 2
(sourcesdk will be supported later)
Otherwise, if you want to work with an existing translation and patch the game, put the modified `subtitles_hebrew.dat` in the project folder.
5. `text_tools.py` contains the text transformation logic, while `file_tools.py` contains filesystem logistics. `install_stanley_steam_heb_win.py` performs the patching for windows.
6. Once you've applied the patch, run the game. You should be able to see subtitles
in Hebrew - if not, try manually applying the `autoexec.cfg` settings in the Portal console
(runnable by using \`): `cc_lang hebrew` and `cc_subtitles 1` . Notice that reapplying the patch requires a restart of the game to work.


## Configuration reference
game_data.json is an attempt to centralize all localization-related configuration into a single file.
Rather than use conditional logic based on game within the code, we keep all related properties for each game
within that file.

The top key for each game is also the name of the game main folder (will probably change soon). example "Portal"
* basegame - the name of inner central game folder. example "portal"
* caption_file_name - the prefix for the subtitle file. For example if the file is closecaption_english.txt then this will be "closecaption".
* other_file_names - other files in the resource folder that need translation.
* max_chars_before_break - This determines the length of each line before portl puts a <cr> to create a new one.
* mod_type - for old games like Portal use "custom". For later games use "dlc".
* os - this is used to determine how to change configuration in the res file such as text size. 
* scheme_on_vpk - true/false. Some games have the scheme file outside the VPK.
* vpk_file_name - should be the dir file in the basegame folder.
* scheme_file_name - just the file name, not the path
* format_replacements: - defines which keys to change in the scheme files and to which values.
* language_name_other_override - unfortunately Portal didn't allow portal_hebrew.txt, so this logic specifically overrides it to be called portal_english.txt, while renaming the original.
* compiler_game_service_path - If the game has no caption compiler, then this is the steam path under which the main game folder is found
* compiler_game - name of the main folder for the compiler
* compiler_game_path - additional path after the steam folder and into the basegame folder, such as \\Black Mesa\\bms
* english_captions_text_path - name of local file with english text for captions