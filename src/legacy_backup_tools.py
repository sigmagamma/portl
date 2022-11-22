
import os
from shutil import move,copyfile
## uninstall logic for old version


def get_temp_cfg_path(file_tools,type):
    return file_tools.get_full_basegame_path() + "\cfg\{}2.cfg".format(type)

def get_backup_cfg_path(file_tools,type):
    return file_tools.get_full_basegame_path() + "\cfg\{}-portl-backup.cfg".format(type)

def get_backup_other_path(file_tools):
    return file_tools.get_full_basegame_path() + "\\resource\portal_english-portl-backup.txt"

def get_backup_other_path_2(file_tools):
    return file_tools.get_full_basegame_path() + "\\resource\portal_english_backup.txt"

def get_backup_captions_text_path(file_tools):
    return file_tools.get_full_basegame_path() +  \
           "\\resource\closecaption_{}-portl-backup.txt".format(file_tools.language)

def get_backup_captions_path(file_tools):
    return file_tools.get_full_basegame_path() +  \
           "\\resource\closecaption_{}-portl-backup.dat".format(file_tools.language)

def get_basegame_cfg_folder(file_tools):
    return file_tools.get_full_basegame_path() + "\cfg"
def get_basegame_cfg_path(file_tools, filename):
    return get_basegame_cfg_folder(file_tools)+"\{}".format(filename)


def find_lines(backup_cfg_path,lang_line,subtitles_line):
    if (os.path.isfile(backup_cfg_path)):
        with open(backup_cfg_path, 'r') as f_in:
            for line in f_in:
                if lang_line == '' and line.startswith("cc_lang"):
                   lang_line = line
                if subtitles_line == '' and line.startswith("cc_subtitles"):
                   subtitles_line = line
    return lang_line,subtitles_line

#remove "bad language"
def remove_hebrew_from_cfg(dest_cfg_path, temp_cfg_path):
    with open(dest_cfg_path, 'r') as f_in, open(temp_cfg_path, 'w') as f_out:
        for line in f_in:
            if not 'cc_lang "hebrew"' in line:
                f_out.write(line)

def restore_cfg(file_tools):
    backup_autoexec_path = get_backup_cfg_path(file_tools, 'autoexec')
    backup_config_path = get_backup_cfg_path(file_tools, 'config')
    main_autoexec_path = get_basegame_cfg_path(file_tools, '../autoexec.cfg')
    temp_autoexec_path = get_temp_cfg_path(file_tools,'autoexec')
    if os.path.isfile(main_autoexec_path):
        if os.path.isfile(backup_autoexec_path):
            move(backup_autoexec_path, main_autoexec_path)
        remove_hebrew_from_cfg(main_autoexec_path,temp_autoexec_path)
        move(temp_autoexec_path, main_autoexec_path)
    if (os.path.isfile(backup_config_path)):
        os.remove(backup_config_path)

def restore_captions(file_tools):
    file_data = {"name": "closecaption", "folder": "resource", "localized": True}
    main_caption_path = file_tools.get_compiled_captions_path(file_data)
    if (os.path.isfile(main_caption_path)):
        os.remove(main_caption_path)
    backup_captions_text_path = get_backup_captions_text_path(file_tools)
    if (os.path.isfile(backup_captions_text_path)):

        answer = input("We previously took the backup "
                       +backup_captions_text_path+" in case you've modified "+
                       file_tools.language+" subtitles. \nOtherwise press y to delete.")
        if answer == "y":
            os.remove(backup_captions_text_path)

def restore_portal(file_tools):
    file_data = {"name": "portal","folder":"resource","localized": True,"extension":"txt"}
    actual_file = file_tools.get_basegame_english_other_path(file_data)
    if not (os.path.isfile(actual_file)):
        backup_other_path = get_backup_other_path(file_tools)
        if (not os.path.isfile(backup_other_path)):
            backup_other_path = get_backup_other_path_2(file_tools)
        if (os.path.isfile(backup_other_path)):
            copyfile(backup_other_path, file_tools.get_basegame_english_other_path(file_data))
            os.remove(backup_other_path)
def restore_backup(file_tools):
    restore_cfg(file_tools)
    restore_portal(file_tools)
    restore_captions(file_tools)


