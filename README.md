# poRTL
Source engine translation framework with support for right-to-left languages.

Currently, Portal, The Stanley Parable (2013) and Black Mesa Arabic are supported.
Current working branch is [feat-black-mesa](https://github.com/sigmagamma/portpyinsl/tree/feat-black-mesa). If you want 
to start working on a new game, checkout that branch and then create a new one out of it. 
Portal is currently working in feat-portal-folder-picker (and the portal release branches),
Stanley is working in its release branch, untested in feat-black-mesa.
Snapshot branch for latest Portal release is [portal-0.9.1](https://github.com/sigmagamma/portl/tree/portal-0.9.1)
Snapshot branch for latest Stanley release is [stanley-0.9.2](https://github.com/sigmagamma/portl/tree/stanley-0.9.2)
see https://github.com/sigmagamma/portl/issues/6 for details on other games.


This project was originally created for the Portal 1 Hebrew fan translation, details on which (in Hebrew) you can find 
here:

https://docs.google.com/document/d/1CYy4ddqIiKt0RwiUZftUVhPl0Pv8gTgZl8HHrvQCkF8/edit?usp=sharing

Or in English here:

https://steamcommunity.com/sharedfiles/filedetails/?id=2554472476

Stanley Parable details (in Hebrew):
https://docs.google.com/document/d/1lsCQosS-TDPFxHi6mnZCE653AfrbqW5MhDCbnV-U_Ds/edit?usp=sharing

details in English:
https://steamcommunity.com/sharedfiles/filedetails/?id=2850801993

Release notes for Black Mesa in Arabic:
https://docs.google.com/document/d/1Yyc_eQwug51asbru8EZ4m6JrIgBErdMdJhBaW--I6kQ/edit?usp=sharing

## What this does
* The program takes translation files and text files for Source games and generates content for the relevant language,
 reversing RTL text if necessary so that the text is readable. Support for right-to-left alignment of the text is limited.
* The program installs the content into the mod folder. In some cases where the mod cannot override the base game folder 
the file in the base game folder is moved to a backup.
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
In step 5, if you're working with Pycharm, you should probably copy the release into the project folder in order to have 
it install pyinstaller into your Virtual Environment.
Remember to run setup.py with your python venv executable. You may have to run Pycharm as administrator.

I've used pyinstaller 5.6.2:
https://github.com/pyinstaller/pyinstaller/releases/tag/v5.6.2

Once Pyinstaller is installed into your environment,modify the path for the portalhebrew folder within the file. Then run 

`pyinstaller --clean install_po_rtl_heb_win.spec`

Spec file was generated with:
`.\venv\Scripts\pyi-makespec.exe --onefile .\install_po_rtl_heb_win.py`

For antivirus software, make sure you tell it to exclude the dist folder of the relevant folder in gamefiles.

## Development setup - Portal
1. Get Portal: 
https://store.steampowered.com/app/400/Portal/
2. Install Python 3.11 
3. Get an IDE for editing python such as [Pycharm](https://www.jetbrains.com/pycharm/)
4. git clone https://github.com/sigmagamma/portl.git
5. Open a project in the created folder, create a virtual environment, and install the requirements from requirements.txt. 
6. You will need a file named The `Portal private.json` under gamefiles/portal  including the link to the 
translation sheet. 
7. `text_tools.py` contains the text transformation logic, while `file_tools.py` contains filesystem logistics. 
`install_po_rtl_heb_win_ltr.py` performs the patching for windows. 
8. Once you've applied the patch, run the game. You should be able to see subtitles
in Hebrew - if not, try manually applying the following settings in the Portal console
(runnable by using \`): `cc_lang english` and `cc_subtitles 1` . Notice that reapplying the patch requires a restart of the game to work. 
9. If you want to work on the right-aligned version, follow similar instructions with install_po_rtl_heb_win_rtl.py, and see additional procedure below.

## Right alignment instructions
This branch contains code that supports right alignment for the captions (not for the song). For this to work correctly:
The installer that does this is 'install_po_rtl_heb_win_rtl.py'.

It is assumed you're running Windows 10 with Hebrew support, meaning you have the Tahoma font.
Run apply_fonts_portal_hebrew.reg to map Tahoma to Miriam Fixed. Restart your PC.
When you start the game, set the game resolution to 1366 * 768. (The plan is to support other sizes)
Once you're done playing, to restore Tahoma run the remove_fonts_portal.reg file and restart Windows.

This process is required as the game does not support native right to left alignment, and also does not allow setting the font for Hebrew characters.


## Development setup - The Stanley Parable

1. Get The Stanley Parable:
https://store.steampowered.com/app/221910/The_Stanley_Parable/
or in Epic:
https://store.epicgames.com/en-US/p/the-stanley-parable
2. Install Python 3.11
3. Get an IDE for editing python such as [Pycharm](https://www.jetbrains.com/pycharm/)
4. git clone https://github.com/sigmagamma/portl.git and switch to stanley-0.9.2 
5. Open a project in the created folder, create a virtual environment, and install the requirements from requirements.txt. 
6. You will need a file named The `Stanley Parable RTL private.json` under gamefiles/stanley  including the link to the 
translation sheet. 
You have to get an additional game that has captioncompiler, like Portal or Portal 2 (sourcesdk will be supported later). 
Configure the compiler_game settings in 'The Stanley Parable.json'.
Otherwise, if you want to work with an existing translation and patch the game, put the modified `subtitles_english.dat` 
in that folder.
7. `text_tools.py` contains the text transformation logic, while `file_tools.py` contains filesystem logistics.
`portal/install_unattended.py` contains quick installers and assumes your registry contains the correct folder placement. 
Otherwise use one of the other installers. 
8. Once you've applied the patch, run the game. You should be able to see subtitles
in Hebrew - if not, try manually applying the following settings in the console
(runnable by using \`): `cc_lang english` and `cc_subtitles 1` . Notice that reapplying the patch requires a restart of 
the game to work.


## Development setup - Black Mesa

1. Get Black Mesa
https://store.steampowered.com/app/362890/Black_Mesa/
2. Install Python 3.11
3. Get an IDE for editing python such as [Pycharm](https://www.jetbrains.com/pycharm/)
4. git clone https://github.com/sigmagamma/portl.git and switch to feat-black-mesa
5. Open a project in the created folder, create a virtual environment, and install the requirements from requirements.txt. 
6. You will need a file named The `Black Mesa Arabic RTL private.json` (with or without RTL, and with the relevant 
language) under gamefiles/blackmesa  including the link to the translation sheet. 
7. `text_tools.py` contains the text transformation logic, while `file_tools.py` contains filesystem logistics. 
`portal/install_unattended.py` contains quick installers and assumes your registry contains the correct folder placement. 
Otherwise use one of the other installers.
8. Once you've applied the patch, run the game. You should be able to see subtitles
in the chosen language - if not, try manually applying the following settings in the console
(runnable by using \`): `cc_lang uarabic` and `cc_subtitles 1` . Notice that reapplying the patch requires a restart of 
9. the game to work.


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


Deprecated:
* os - deprecated use to determine how to change configuration in the res file such as text size. 