# poRTL
Source engine translation framework with support for right-to-left languages.

Currently, Portal, The Stanley Parable (2013) and Black Mesa Arabic are supported.
No current working branch, let's give it some rest. If you want 
to start working on a new game, checkout master and then create a new one out of it. 
Portal 2 is working in master.
Portal is currently working in feat-portal-folder-picker (and the portal release branches),
Stanley is working in its release branch, untested in feat-black-mesa.
Snapshot branch for latest Portal release is [portal-0.9.1](https://github.com/sigmagamma/portl/tree/portal-0.9.1)
Snapshot branch for latest Stanley release is [stanley-0.9.2](https://github.com/sigmagamma/portl/tree/stanley-0.9.2)
see https://github.com/sigmagamma/portl/issues/6 for details on other games.


This project was originally created for the Portal 1 Hebrew fan translation, details on which (in Hebrew) you can find 
here, including installation:

https://docs.google.com/document/d/1CYy4ddqIiKt0RwiUZftUVhPl0Pv8gTgZl8HHrvQCkF8/edit?usp=sharing

Or in English here:

https://steamcommunity.com/sharedfiles/filedetails/?id=2554472476

Stanley Parable details, including installation (in Hebrew):
https://docs.google.com/document/d/1lsCQosS-TDPFxHi6mnZCE653AfrbqW5MhDCbnV-U_Ds/edit?usp=sharing

details in English:
https://steamcommunity.com/sharedfiles/filedetails/?id=2850801993

Release notes for Black Mesa in Arabic:
https://docs.google.com/document/d/1Yyc_eQwug51asbru8EZ4m6JrIgBErdMdJhBaW--I6kQ/edit?usp=sharing

## What this does
* The program takes translation files and text files for Source games and generates content for the relevant language,
 reversing RTL text if necessary so that the text is readable. Support for right-to-left alignment of the text works for
 some of the games.
* The program installs the content into the mod folder, and sometimes overwrites existing content.
* Installers and zips are generated using batch files that rely on the content created using the program.
* The NSIS installer also backs up the files that will be overwritten.

## Development setup - Portal 2
The following part is relevant to developers who want to work on the game translation.
1. Get Portal 2:
https://store.steampowered.com/app/620/Portal_2/
2. Download the Portal 2 Authoring tools (I'm pretty sure that's required)
3. Install Python 3.11 
4. Get an IDE for editing python such as [Pycharm](https://www.jetbrains.com/pycharm/)
5. git clone https://github.com/sigmagamma/portl.git
6. Open a project in the created folder, create a virtual environment, and install the requirements from 
requirements.txt. 
7. You will need a seprately distributed file named The `Portal2 RTL private.json` under gamefiles/portal2 including the 
link to the translation sheet.
8. Run copyoriginalsources.bat. Should be run from the folder above gamefiles. 
9. Get GCFScape. https://nemstools.github.io/pages/GCFScape-Download.html
10. Go over `Portal2 RTL.json`, and look for the files which have a "local_parent_source_folder" field. create those folders under gamefiles\portal2, and then copy the files from the vpks using gcfscape as instructed there.
11. Patch the game in Windows using the release and get bin\vguimatsurface.dll, put it in gamefiles\portal2. Then uninstall the patch.
12. Put the windows vids under media, and the linux media files under linux\media
13. Put all relevant textures under game_assets\materials. Put "Glados" variant textures under m_game_assets\materials, and Mabsuta variant textures under m_game_assets
14. Extract update\pak1_dir.vpk to gamefiles\portal2\update_target
15. `text_tools.py` contains the text transformation logic, while `file_tools.py` contains filesystem logistics. 
`portal2/install_unattended.py` has the various installation functions. Make sure the working directory is above gamefiles.
16. packmod_steam.bat (again, run from one dir above gamefiles) produces the installation files and zips. it uses portal2.nsi which is the NSIS installer configuration, and 7-zip which should be in "c:\Program Files\7-Zip\7z.exe"

When in doubt, verify game files from Steam and start over. 
## Development setup - Portal 1
The following part is relevant to developers who want to work on the game translation.
1. Get Portal: 
https://store.steampowered.com/app/400/Portal/
2. Install Python 3.11 
3. Get an IDE for editing python such as [Pycharm](https://www.jetbrains.com/pycharm/)
4. git clone https://github.com/sigmagamma/portl.git
5. Open a project in the created folder, create a virtual environment, and install the requirements from 
requirements.txt. 
6. You will need a seprately distributed file named The `Portal 2007 private.json` under gamefiles/portal including the 
link to the translation sheet. 
7. `text_tools.py` contains the text transformation logic, while `file_tools.py` contains filesystem logistics. 
`install_portal_2007_heb_win_ltr.py` performs the patching for windows for the ltr version (there are also quick 
installers in the install_unattended script). make sure the working directory is above gamefiles.
8. Once you've applied the patch, run the game. You should be able to see subtitles
in Hebrew - if not, try manually applying the following settings in the Portal console
(runnable by using \`): `cc_lang english` and `cc_subtitles 1` . Notice that reapplying the patch requires a restart of
the game to work. 
9. If you want to work on the right-aligned version, follow similar instructions with 
`install_portal_2007_heb_win_rtl.py`,  and see additional procedure below.

## Right alignment instructions - Portal 1
This branch contains code that supports right alignment for the captions (not for the song). For this to work correctly:
The installer that does this is `install_portal_2007_heb_win_rtl.py`.

It is assumed you're running Windows 10 with Hebrew support, meaning you have the Tahoma font.
Run registry/apply_fonts_portal_hebrew.reg to map Tahoma to Miriam Fixed. Restart your PC.
When you start the game, set the game resolution to 1366 * 768. (not tested on other sizes - your mileage may vary)
Once you're done playing, to restore Tahoma run the remove_fonts_portal.reg file and restart Windows.

This process is required as the game does not support native right to left alignment, and also does not allow setting 
the font for Hebrew characters.


# creating releases - Portal 1

packmod_2007.bat and packmod_rtx currently pack zip files, and also exes using pyinstaller.
The spec files define pyinstaller behavior

Pyinstaller is a very fragile solution that's currently working on a crutch. It is repla
If you still want to make pyinstaller work, Use this guide:
https://python.plainenglish.io/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184

Some additional points to those in the guide:
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
translation sheet.  You will also need subtitle_english.txt in the same folder, which is the source file for the english subtitles.
You have to get an additional game that has captioncompiler, like Portal or Portal 2 (sourcesdk will be supported later). 
Configure the compiler_game settings in '`Stanley Parable RTL.json'.
Otherwise, if you want to work with an existing translation and patch the game, put the modified `subtitles_english.dat` 
in that folder.
8. `text_tools.py` contains the text transformation logic, while `file_tools.py` contains filesystem logistics.
`stanley/install_unattended.py` contains quick installers and assumes your registry contains the correct folder 
placement. Otherwise use one of the other installers. 
9. Once you've applied the patch, run the game. You should be able to see subtitles
in Hebrew - if not, try manually applying the following settings in the console
(runnable by using \`): `cc_lang english` and `cc_subtitles 1` . Notice that reapplying the patch requires a restart of 
the game to work.


## Development setup - Black Mesa

1. Get Black Mesa
https://store.steampowered.com/app/362890/Black_Mesa/
2. Install Python 3.11
3. Get an IDE for editing python such as [Pycharm](https://www.jetbrains.com/pycharm/)
4. git clone https://github.com/sigmagamma/portl.git and switch to feat-black-mesa
5. Open a project in the created folder, create a virtual environment, and install the requirements from 
requirements.txt. 
6. You will need a file named The `Black Mesa Arabic RTL private.json` (with or without RTL, and with the relevant 
language) under gamefiles/blackmesa  including the link to the translation sheet. 
7. `text_tools.py` contains the text transformation logic, while `file_tools.py` contains filesystem logistics. 
`portal/install_unattended.py` contains quick installers and assumes your registry contains the correct folder 
placement. 
Otherwise use one of the other installers.
8. Once you've applied the patch, run the game. You should be able to see subtitles
in the chosen language - if not, try manually applying the following settings in the console
(runnable by using \`): `cc_lang uarabic` and `cc_subtitles 1` . Notice that reapplying the patch requires a restart of 
9. the game to work.


## Configuration reference
the game-specific json is an attempt to centralize all localization-related configuration into a single file.
Rather than use conditional logic based on game within the code, we keep all related properties for each game
within that file.
Configuration grew a lot in portal 2,

* game -  name of the game main folder . example "Portal"
* shortname - name of the game for versioning
* version - version of distribution
* basegame - the name of inner central game folder. example "portal"
* other_files - files that need translation or reconfiguration from sheets (see below)
* filter_files, filter_out_files - these are lists of file names to include/exclude files, used for debugging
* max_chars_before_break - This determines the length of each line before portl puts a <cr> to create a new one.
* total_chars_in_line - this is the total length of the line in order to allow right-alignment.
* text_spacings - this is a collection of templates with the two properties above for repeated use in the sheets
* mod_type - for old games like Portal use "custom". For later games use "dlc".
* os - sort of deprecated, but keep as WIN in any case
* vpk_file_name - should be the dir file in the basegame folder. Just the filename.
* vpk_folders - this tells the program where to build the target VPKs and from what. null target_folder means this will be created in the mod folder.
* compiler_game_service_path - If the game has no caption compiler, then this is the steam path under which the main game folder is found
* compiler_game - name of the main folder for the compiler
* compiler_game_path - additional path after the steam folder and into the basegame folder, such as \\Black Mesa\\bms
* captions_prefix - This gets prefixed to every subtitle, we use <B> to make Courier New look better


other_files reference:
* name - basic filename without directory, language or suffix
* folder - folder name for the file
* localized - whether the file has a localized suffix
* override - override the file in the source folder rather than in the mod folder
* is_on_vpk - whether the source file should be taken from the VPK
* translation_sheet - the sheet in the translation file with which the file needs to be translated
* extension - the extension for the file
* is_captions - whether the file should be compiled to captions
* extension - the source extension for the file
* dest_extension - the target extension, if different 
* encoding - the source encoding for the game file
* insert_newlines - are lines separated using a new line
* local_temporary_parent_target_folder - where to put the target file for VPK packing
* local_parent_source_folder - with files that are in VPK, we first manually extract them here in order to maintain the base file unchanged
Deprecated:
* os - deprecated use to determine how to change configuration in the res file such as text size. 
* caption_file_name - the prefix for the subtitle file. For example if the file is closecaption_english.txt then this will be "closecaption".
