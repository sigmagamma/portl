# poRTL
Source engine translation framework with support for right-to-left languages.

Currently Portal 1 is supported. Current working branch is [feat-stanley](https://github.com/sigmagamma/portl/tree/feat-stanley). If you want to start working on a new game, checkout that branch and then create a new one out of it. 
Snapshot branch for latest Portal release is [portal-0.9.1](https://github.com/sigmagamma/portl/tree/portal-0.9.1)
see https://github.com/sigmagamma/portl/issues/6 for details on other games.


This project was originally created for the Portal 1 Hebrew fan translation, details on which (in Hebrew) you can find here:

https://www.facebook.com/groups/200491360554968/posts/868793153724782

Or in English here:

https://steamcommunity.com/sharedfiles/filedetails/?id=2554472476

## What this does
* The program takes translation files and text files for Source games and generates content for the relevant language,
 reversing RTL text if necessary so that the text is readable. Support for right-to-left alignment of the text is limited.
* The program installs the content into the mod folder. In some cases where the mod cannot override the base game folder the file in the base game folder is moved to a backup.
* The installer also allows removing the mod and restoring the backup
* The installer doubles as a tool to generate the required content for easier installation later.
* The installer now copies the folders "materials" and "sound" to the mod folder

## Windows Hebrew installation for Portal
This repository does not include any file with actual source or translation material from the game.
In order to run this you'll need to put either:

1. closecaption_english.dat credits.txt and portal_english.txt that already contain the hebrew translation OR
2. Portal translation - additions.csv, Portal translation - closecaption.csv, Portal translation - credits.csv
in the gamefiles\portal folder.

You can then run install_po_rtl_heb_win.py for a Windows installation.

You can use the spec files with pyinstaller to create the executable.

Pyinstaller is a very fragile solution that's currently working on a crutch.
Use this guide:
https://python.plainenglish.io/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184

Some additional points to follow:
Within the Visual Studio Installer, make sure you add "Desktop development with C++".
In step 5, if you're working with Pycharm, you should probably copy the release into the project folder in order to have it install pyinstaller into your Virtual Environment.
Also you may have to run Pycharm as administrator.
I've used the pyinstaller develop branch:
https://github.com/pyinstaller/pyinstaller/archive/develop.zip

Once Pyinstaller is installed into your environment,modify the path for the portalhebrew folder within the file. Then run 

`pyinstaller --clean install_po_rtl_heb_win.spec`

Spec file was generated with:
`.\venv\Scripts\pyi-makespec.exe --onefile .\install_po_rtl_heb_win.py`


## Development setup - Portal
1. Get Portal: 
https://store.steampowered.com/app/400/Portal/
2. Get an IDE for editing python such as [Pycharm](https://www.jetbrains.com/pycharm/)
3. git clone https://github.com/sigmagamma/portl.git
4. If you want to change the actual translation, put the relevant csvs in the gamefiles\portal folder
These have to be named "Portal translation - closecaption.csv", "Portal translation - credits.csv" and "Portal translation - portal.csv."
Otherwise, if you want to work with an existing translation and patch the game, put the modified `closecaption_english.dat` `credits.txt` and `portal_english.txt` in the project folder.
5. `text_tools.py` contains the text transformation logic, while `file_tools.py` contains filesystem logistics. `install_po_rtl_heb_win.py` performs the patching for windows.
6. Once you've applied the patch, run the game. You should be able to see subtitles
in Hebrew - if not, try manually applying the following settings in the Portal console
(runnable by using \`): `cc_lang english` and `cc_subtitles 1` . Notice that reapplying the patch requires a restart of the game to work.
7. If you want to work on the right-aligned version, follow similar instructions with install_po_rtl_heb_win_rtl.py, and see additional procedure below.

## Right alignment instructions
This branch contains code that supports right alignment for the captions (not for the song). For this to work correctly:
The installer that does this is 'install_po_rtl_heb_win_rtl.py'.

It is assumed you're running Windows 10 with Hebrew support, meaning you have the Tahoma font.
Run apply_fonts_portal_hebrew.reg to map Tahoma to Miriam Fixed. Restart your PC.
When you start the game, set the game resolution to 1366 * 768. (The plan is to support other sizes)
Once you're done playing, to restore Tahoma run the remove_fonts_portal.reg file and restart Windows.

This process is required as the game does not support native right to left alignment, and also does not allow setting the font for Hebrew characters.


## Development setup - Stanley Parable

1. Get Stanley Parable:
https://store.steampowered.com/app/221910/The_Stanley_Parable/
(Epic not supported yet)
2. Get an IDE for editing python such as [Pycharm](https://www.jetbrains.com/pycharm/)
3. git clone https://github.com/sigmagamma/portl.git and switch to feat-stanley
4. If you want to change the actual translation, put the relevant csv in the gamefiles\stanley folder. 
It has to be named "The Stanley Parable translation - subtitles.csv". You also need to have subtitles_english.txt in that folder.
For this mode you have to get an additional game that has captioncompiler, like Portal or Portal 2 (sourcesdk will be supported later). Configure the compiler_game settings in 'The Stanley Parable.json'.
Otherwise, if you want to work with an existing translation and patch the game, put the modified `subtitles_english.dat` in that folder.
5. `text_tools.py` contains the text transformation logic, while `file_tools.py` contains filesystem logistics. `install_stanley_steam_heb_win.py` performs the patching for windows.
6. Once you've applied the patch, run the game. You should be able to see subtitles
in Hebrew - if not, try manually applying the following settings in the console
(runnable by using \`): `cc_lang english` and `cc_subtitles 1` . Notice that reapplying the patch requires a restart of the game to work.


## Configuration reference
the game-specific json is an attempt to centralize all localization-related configuration into a single file.
Rather than use conditional logic based on game within the code, we keep all related properties for each game
within that file.

* game -  name of the game main folder . example "Portal"
* shortname - name of the game for versioning
* version - version of distribution
* basegame - the name of inner central game folder. example "portal"
* caption_file_name - the prefix for the subtitle file. For example if the file is closecaption_english.txt then this will be "closecaption".
* other_file_names - other files in the resource folder that need translation.
* max_chars_before_break - This determines the length of each line before portl puts a <cr> to create a new one.
* mod_type - for old games like Portal use "custom". For later games use "dlc".
* os - future use for other OS support
* vpk_file_name - should be the dir file in the basegame folder.
* language_name_other_override - unfortunately Portal didn't allow portal_hebrew.txt, so this logic specifically overrides it to be called portal_english.txt, while renaming the original.
* compiler_game_service_path - If the game has no caption compiler, then this is the steam path under which the main game folder is found
* compiler_game - name of the main folder for the compiler
* compiler_game_path - additional path after the steam folder and into the basegame folder, such as \\Black Mesa\\bms
* english_captions_text_path - name of local file with english text for captions


Deprecated, Portal only:
* scheme_on_vpk - true/false. Some games have the scheme file outside the VPK.
* scheme_file_name - just the file name, not the path
* format_replacements: - defines which keys to change in the scheme files and to which values.
* os - deprecated use to determine how to change configuration in the res file such as text size. 