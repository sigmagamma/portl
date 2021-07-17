import os
import sys
import winreg
from shutil import copyfile
from shutil import move
from os import path
import text_tools as tt
import subprocess

##Steam logic
def steam_path_windows():

    try:
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
    except:
        hkey = None
        print(sys.exc_info())
    try:
        steam_path = winreg.QueryValueEx(hkey, "InstallPath")
    except:
        steam_path = None
        print(sys.exc_info())
    return steam_path[0]

def steam_path_linux():
    return "~/.steam/steam"

## path functions
def get_new_cfg_path(type):
    filename = "{}.cfg".format(type)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        filename = path.abspath(path.join(path.dirname(__file__), filename))
    return filename
def get_dest_cfg_path(steam_path,type):
    return steam_path+"\steamapps\common\Portal\portal\cfg\{}.cfg".format(type)

def get_temp_cfg_path(steam_path,type):
    return steam_path + "\steamapps\common\Portal\portal\cfg\{}2.cfg".format(type)

def get_backup_cfg_path(steam_path,type):
    return steam_path + "\steamapps\common\Portal\portal\cfg\{}-portl-backup.cfg".format(type)

def get_backup_additions_path(steam_path):
    return steam_path + "\steamapps\common\Portal\portal\\resource\portal_english-portl-backup.txt"

def get_dest_additions_path(steam_path):
    return steam_path + "\steamapps\common\Portal\portal\\resource\portal_english.txt"

def get_temp_additions_path(steam_path):
    return steam_path + "\steamapps\common\Portal\portal\\resource\portal_temp.txt".format(type)

def get_new_additions_path():
    filename = "portal_english.txt"
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        filename = path.abspath(path.join(path.dirname(__file__), filename))
    return filename

def get_dest_captions_path(steam_path,language):
    return steam_path + "\steamapps\common\Portal\portal\\resource\closecaption_{}.dat".format(language)

def get_dest_captions_text_path(steam_path,language):
    return steam_path + "\steamapps\common\Portal\portal\\resource\closecaption_{}.txt".format(language)

def get_new_captions_path(language):
    filename = "closecaption_{}.dat".format(language)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        filename = path.abspath(path.join(path.dirname(__file__), filename))
    return filename

def get_compiler_path(steam_path):
    return steam_path + "\steamapps\common\portal\\bin\captioncompiler.exe"

def get_english_captions_text_path(steam_path):
    return steam_path + "\steamapps\common\Portal\portal\\resource\closecaption_english.txt"

def get_backup_captions_text_path(steam_path,language):
    return steam_path + "\steamapps\common\Portal\portal\\resource\closecaption_{}-portl-backup.txt".format(language)

def get_backup_captions_path(steam_path,language):
    return steam_path + "\steamapps\common\Portal\portal\\resource\closecaption_{}-portl-backup.dat".format(language)



def get_english_additions_text_path(steam_path):
    return steam_path + "\steamapps\common\Portal\portal\\resource\portal_english.txt"

def get_captions_csv_path():
    return "Portal translation - closedcaption.csv"
def get_additions_csv_path():
    return "Portal translation - additions.csv"
## cfg files logic
def write_temp_cfg(dest_cfg_path,temp_cfg_path,lang_replacement,subtitles_replacement):
    with open(dest_cfg_path, 'r') as f_in, open(temp_cfg_path, 'w') as f_out:
        lang_flag = False
        subtitles_flag = False
        for line in f_in:
            if line.startswith("cc_lang"):
                lang_flag = True
                if lang_replacement != '':
                    f_out.write(lang_replacement)
            elif line.startswith("cc_subtitles"):
                subtitles_flag = True
                if subtitles_replacement != '':
                    f_out.write(subtitles_replacement)
            else:
                f_out.write(line)
        if not lang_flag and lang_replacement != '':
            f_out.write(lang_replacement)
        if not subtitles_flag and subtitles_replacement != '':
            f_out.write(subtitles_replacement)

def backup_cfg(steam_path,type):
    dest_cfg_path = get_dest_cfg_path(steam_path,type)
    backup_cfg_path = get_backup_cfg_path(steam_path, type)
    copyfile(dest_cfg_path, backup_cfg_path)

def write_cfg(steam_path,language,type):
    dest_cfg_path = get_dest_cfg_path(steam_path,type)
    if type != 'config' and not (os.path.isfile(dest_cfg_path)):
        new_cfg_path = get_new_cfg_path(type)
        copyfile(new_cfg_path, dest_cfg_path)
    else:
        temp_cfg_path = get_temp_cfg_path(steam_path,type)
        backup_cfg_path = get_backup_cfg_path(steam_path,type)
        lang_replacement = 'cc_lang "' + language + '"\n'
        subtitles_replacement = 'cc_subtitles "1"'
        write_temp_cfg(dest_cfg_path,temp_cfg_path,lang_replacement,subtitles_replacement)
        if not (os.path.isfile(backup_cfg_path)):
            copyfile(dest_cfg_path, backup_cfg_path)
        move(temp_cfg_path, dest_cfg_path)

## patch files logic
def write_captions_from_patch(steam_path,language):
    backup_captions_path = get_backup_captions_path(steam_path,language)
    dest_captions_path = get_dest_captions_path(steam_path, language)
    if os.path.isfile(dest_captions_path) and not (os.path.isfile(backup_captions_path)):
        copyfile(dest_captions_path,backup_captions_path)
    copyfile(get_new_captions_path(language),dest_captions_path)
def write_additions_from_patch(steam_path):
    backup_additions_path = get_backup_additions_path(steam_path)
    dest_additions_path = get_dest_additions_path(steam_path)
    if os.path.isfile(dest_additions_path) and not (os.path.isfile(backup_additions_path)):
        copyfile(dest_additions_path, backup_additions_path)
    copyfile(get_new_additions_path(),get_dest_additions_path(steam_path))

## csv files logic
def write_captions_from_csv(steam_path,compiler_path,language,csv_path):
    orig_captions_text_path = get_english_captions_text_path(steam_path)
    dest_captions_text_path = get_dest_captions_text_path(steam_path,language)
    backup_captions_text_path = get_backup_captions_text_path(steam_path,language)
    if os.path.isfile(dest_captions_text_path) and not (os.path.isfile(backup_captions_text_path)):
        copyfile(dest_captions_text_path,backup_captions_text_path)
    translated_path = "closecaption_{}.txt".format(language)
    translated_lines = tt.read_translation_from_csv(csv_path)
    tt.translate(orig_captions_text_path,translated_path,translated_lines,True)
    move(translated_path,dest_captions_text_path)
    # Compiler actually takes the local path as under the resources folder, so that's ok
    subprocess.run([compiler_path,translated_path])

def write_additions_from_csv(steam_path,csv_path):
    backup_additions_path = get_backup_additions_path(steam_path)
    dest_additions_path = get_dest_additions_path(steam_path)
    temp_additions_path = get_temp_additions_path(steam_path)
    if os.path.isfile(dest_additions_path) and not (os.path.isfile(backup_additions_path)):
        copyfile(dest_additions_path, backup_additions_path)
    translated_lines = tt.read_translation_from_csv(csv_path)
    tt.translate(backup_additions_path,temp_additions_path,translated_lines,False)
    move(temp_additions_path,dest_additions_path)

## main write function
def write_files(steam_path,language):
    write_cfg(steam_path,language,'autoexec')
    backup_cfg(steam_path,'config')
    captions_csv_path = get_captions_csv_path()
    additions_csv_path = get_additions_csv_path()
    if (os.path.isfile(captions_csv_path)):
        write_captions_from_csv(steam_path,get_compiler_path(steam_path),language,captions_csv_path)
    else:
        write_captions_from_patch(steam_path,language)
    if os.path.isfile(additions_csv_path):
        write_additions_from_csv(steam_path,additions_csv_path)
    else:
        write_additions_from_patch(steam_path)

## uninstall logic
def find_lines(backup_cfg_path,lang_line,subtitles_line):
    if (os.path.isfile(backup_cfg_path)):
        with open(backup_cfg_path, 'r') as f_in:
            for line in f_in:
                if lang_line == '' and line.startswith("cc_lang"):
                   lang_line = line
                if subtitles_line == '' and line.startswith("cc_subtitles"):
                   subtitles_line = line
    return lang_line,subtitles_line


def restore_cfg(steam_path):
    dest_autoexec_path = get_dest_cfg_path(steam_path,'autoexec')
    backup_autoexec_path = get_backup_cfg_path(steam_path,'autoexec')
    temp_autoexec_path = get_temp_cfg_path(steam_path,'autoexec')
    backup_config_path = get_backup_cfg_path(steam_path, 'config')
    backup_lang_line = ''
    backup_subtitles_line = ''
    backup_lang_line,backup_subtitles_line = find_lines(backup_autoexec_path,backup_lang_line,backup_subtitles_line)
    if backup_lang_line == '' or backup_subtitles_line == '':

        backup_lang_line, backup_subtitles_line = find_lines(backup_config_path, backup_lang_line,
                                                             backup_subtitles_line)
    write_temp_cfg(dest_autoexec_path,temp_autoexec_path,backup_lang_line,backup_subtitles_line)
    move(temp_autoexec_path, dest_autoexec_path)
    if (os.path.isfile(backup_autoexec_path)):
        os.remove(backup_autoexec_path)

    if (os.path.isfile(backup_config_path)):
        os.remove(backup_config_path)
def restore_captions(steam_path,language):
    dest_caption_path = get_dest_captions_path(steam_path, language)
    if (os.path.isfile(dest_caption_path)):
        os.remove(dest_caption_path)
    dest_captions_text_path = get_dest_captions_text_path(steam_path,language)
    backup_captions_text_path = get_backup_captions_text_path(steam_path,language)
    if (os.path.isfile(backup_captions_text_path)):
        copyfile(backup_captions_text_path, dest_captions_text_path)
        os.remove(backup_captions_text_path)

def restore_additions(steam_path):
    backup_additions_path = get_backup_additions_path(steam_path)
    if (os.path.isfile(backup_additions_path)):
        copyfile(backup_additions_path, get_dest_additions_path(steam_path))
        os.remove(backup_additions_path)
def restore_backup(steam_path,language):
    restore_cfg(steam_path)
    restore_additions(steam_path)
    restore_captions(steam_path,language)


