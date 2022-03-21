
import os
from shutil import move,copyfile
## uninstall logic for old version


def get_temp_cfg_path(file_tools,type):
    return file_tools.game_parent_path + file_tools.basegame_path + "\cfg\{}2.cfg".format(type)

def get_backup_cfg_path(file_tools,type):
    return file_tools.game_parent_path + file_tools.basegame_path + "\cfg\{}-portl-backup.cfg".format(type)

def get_backup_other_path(file_tools):
    return file_tools.game_parent_path + file_tools.basegame_path + "\\resource\portal_english-portl-backup.txt"

def get_backup_captions_text_path(file_tools):
    return file_tools.game_parent_path + file_tools.basegame_path +  \
           "\\resource\closecaption_{}-portl-backup.txt".format(file_tools.language)

def get_backup_captions_path(file_tools):
    return file_tools.game_parent_path + file_tools.basegame_path +  \
           "\\resource\closecaption_{}-portl-backup.dat".format(file_tools.language)

def find_lines(backup_cfg_path,lang_line,subtitles_line):
    if (os.path.isfile(backup_cfg_path)):
        with open(backup_cfg_path, 'r') as f_in:
            for line in f_in:
                if lang_line == '' and line.startswith("cc_lang"):
                   lang_line = line
                if subtitles_line == '' and line.startswith("cc_subtitles"):
                   subtitles_line = line
    return lang_line,subtitles_line


def restore_cfg(file_tools):
    main_autoexec_path = file_tools.get_basegame_cfg_path('autoexec')
    backup_autoexec_path = get_backup_cfg_path(file_tools,'autoexec')
    temp_autoexec_path = get_temp_cfg_path(file_tools,'autoexec')
    backup_config_path = get_backup_cfg_path(file_tools, 'config')
    if not ( (os.path.isfile(backup_autoexec_path)) or (os.path.isfile(backup_config_path))):
        return
    backup_lang_line = ''
    backup_subtitles_line = ''
    backup_lang_line,backup_subtitles_line = find_lines(backup_autoexec_path,backup_lang_line,backup_subtitles_line)
    if backup_lang_line == '' or backup_subtitles_line == '':

        backup_lang_line, backup_subtitles_line = find_lines(backup_config_path, backup_lang_line,
                                                             backup_subtitles_line)
    file_tools.write_replacement_cfg(main_autoexec_path, temp_autoexec_path, backup_lang_line, backup_subtitles_line)
    move(temp_autoexec_path, main_autoexec_path)
    if (os.path.isfile(backup_autoexec_path)):
        os.remove(backup_autoexec_path)
    if (os.path.isfile(backup_config_path)):
        os.remove(backup_config_path)

def restore_captions(file_tools):
    main_caption_path = file_tools.get_compiled_captions_path()
    if (os.path.isfile(main_caption_path)):
        os.remove(main_caption_path)
    backup_captions_text_path = get_backup_captions_text_path(file_tools)
    if (os.path.isfile(backup_captions_text_path)):

        answer = input("We previously took the backup "
                       +backup_captions_text_path+" in case you've modified "+
                       file_tools.language+" subtitles. \nOtherwise press y to delete.")
        if answer == "y":
            os.remove(backup_captions_text_path)

def restore_other(file_tools):
    backup_other_path = get_backup_other_path(file_tools)
    file_data = {"name": "portal","folder":"resource","localized": True}
    if (os.path.isfile(backup_other_path)):
        copyfile(backup_other_path, file_tools.get_basegame_english_other_path(file_data))
        os.remove(backup_other_path)
def restore_backup(file_tools):
    restore_cfg(file_tools)
    restore_other(file_tools)
    restore_captions(file_tools)


