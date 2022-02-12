import os
import sys
import winreg
from shutil import copyfile,copy,move,rmtree
from os import path
import text_tools as tt
import subprocess
import json

##Steam/Epic logic
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
    return steam_path[0] + "\steamapps\common"


def steam_path_linux():
    return "~/.steam/steam/steamapps/common"



class FileTools:
    def __init__(self, game,game_service_path,language):

        if (game is not None):
            with open('game_data.json','r') as game_data_file:
                data = json.load(game_data_file).get(game)
                if data is not None:
                    self.game = game
                    self.game_path = data['path']
                    self.caption_file_name = data['caption_file_name']
                    self.other_file_names = data.get('other_file_names')
                    if self.other_file_names is None:
                        self.other_file_names = []
                    self.max_chars_before_break = data['max_chars_before_break']
                    self.total_chars_in_line = data.get('total_chars_in_line')
                    self.game_parent_path = game_service_path
                    self.language = language
                    compiler_game_service_path = data.get('compiler_game_service_path')
                    if compiler_game_service_path is not None:
                        self.compiler_game_parent_path = compiler_game_service_path
                        self.compiler_game_path = data.get('compiler_game_path')
                        self.compiler_game = data.get('compiler_game')
                    else:
                        self.compiler_game_parent_path = self.game_parent_path
                        self.compiler_game_path = self.game_path
                        self.compiler_game = self.game
                    self.compiler_path = self.get_compiler_path()
                    self.english_captions_text_path = data.get('english_captions_text_path')
                    if self.english_captions_text_path is None:
                        self.english_captions_text_path = self.get_english_captions_text_path()
                    mod_type = data.get('mod_type')
                    self.mod_type = mod_type
                    if mod_type == 'custom':
                        self.mod_folder = self.get_custom_folder()
                    elif mod_type == 'dlc':
                        self.mod_folder = self.get_dlc_folder()
                else:
                    return None
        else:
            return None

    def get_compiler_resource_folder(self):
        return self.compiler_game_parent_path + self.compiler_game_path + "\\resource"

    def get_custom_parent_folder(self):
        return self.game_parent_path + self.game_path + "\custom"

    def get_dlc_folder(self):
        return self.game_parent_path + self.game_path + "_dlc1"

    def get_custom_folder(self):
        return self.get_custom_parent_folder()+"\portl"

    def get_mod_cfg_folder(self):
        return self.mod_folder+"\cfg"

    def get_mod_resource_folder(self):
        return self.mod_folder+"\\resource"

    def get_mod_cache_folder(self):
        return self.mod_folder+"\\maps\\soundcache"
    def get_basegame_cache_path(self):
        return self.game_parent_path+self.game_path+"\maps\soundcache\_master.cache"
    def create_mod_folders(self):
        mod_cfg_folder = self.get_mod_cfg_folder()
        if not os.path.exists(mod_cfg_folder):
            os.makedirs(mod_cfg_folder)
        mod_resource_folder = self.get_mod_resource_folder()
        if not os.path.exists(mod_resource_folder):
            os.makedirs(mod_resource_folder)

        if self.mod_type == 'dlc':
            basegame_cache_path = self.get_basegame_cache_path()
            if not os.path.exists(basegame_cache_path):
                input("Note: You'll have to start the game, get to the loading screen, wait for a while, and then restart it. Press any key.")
            else:
                mod_cache_folder = self.get_mod_cache_folder()
                if not os.path.exists(mod_cache_folder):
                    os.makedirs(mod_cache_folder)
                copy(basegame_cache_path,mod_cache_folder)
    def remove_mod_folder(self):
        rmtree(self.mod_folder)

    def get_compiler_path(self):
        return self.compiler_game_parent_path + \
               "\{}\\bin\captioncompiler.exe".format(self.compiler_game)

    # patch are the local files of the patch. basegame is the content folder
    # for the original game (usually something like portal/portal)
    # while mod is where the mod gets placed (for instancef portal/custom/portl)

    ## cfg files logic

    def get_patch_cfg_path(self,type):
        filename = "{}.cfg".format(type)
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            filename = path.abspath(path.join(path.dirname(__file__), filename))
        return filename

    def get_basegame_cfg_path(self, type):
        return self.game_parent_path + self.game_path + "\cfg\{}.cfg".format(type)

    def get_mod_cfg_path(self, type):
        return self.get_mod_cfg_folder() + "\{}.cfg".format(type)

    def write_replacement_cfg(self,dest_cfg_path, temp_cfg_path, lang_replacement, subtitles_replacement):
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


    def write_cfg(self,type):
        dest_cfg_path = self.get_mod_cfg_path(type)
        if type != 'config':
            new_cfg_path = self.get_patch_cfg_path(type)
            copyfile(new_cfg_path, dest_cfg_path)
        else:
            src_cfg_path = self.get_basegame_cfg_path(type)
            lang_replacement = 'cc_lang "' + self.language + '"\n'
            subtitles_replacement = 'cc_subtitles "1"'
            self.write_replacement_cfg(src_cfg_path, dest_cfg_path, lang_replacement, subtitles_replacement)



    ## Close Captions logic


    def get_mod_captions_path(self):
        return self.get_mod_resource_folder() + "\{}_{}.dat".format(self.caption_file_name,self.language)

    def get_compiled_captions_path(self):
        return self.compiler_game_parent_path + self.compiler_game_path +\
               "\\resource\{}_{}.dat".format(self.caption_file_name,self.language)

    def get_to_compile_text_path(self):
        return self.compiler_game_parent_path + self.compiler_game_path +\
               "\\resource\{}_{}.txt".format(self.caption_file_name,self.language)


    def get_mod_captions_text_path(self):
        return self.get_mod_resource_folder() + "\{}_{}.txt".format(self.caption_file_name,self.language)

    def get_patch_captions_path(self):
        filename = "{}_{}.dat".format(self.caption_file_name,self.language)
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            filename = path.abspath(path.join(path.dirname(__file__), filename))
        return filename


    def get_english_captions_text_path(self):
        return self.game_parent_path + self.game_path +\
               "\\resource\{}_english.txt".format(self.caption_file_name)

    def get_patch_captions_csv_path(self):
        return self.game + " translation - "+ self.caption_file_name +".csv"

    def write_captions_from_patch(self):
        dest_captions_path = self.get_mod_captions_path()
        copyfile(self.get_patch_captions_path(), dest_captions_path)

    def write_captions_from_csv(self,csv_path):
        orig_captions_text_path = self.english_captions_text_path
        to_compile_text_path = self.get_to_compile_text_path()
        translated_path = "{}_{}.txt".format(self.caption_file_name,self.language)
        translated_lines = tt.read_translation_from_csv(csv_path)
        tt.translate(orig_captions_text_path,translated_path,translated_lines,True,self.max_chars_before_break,self.total_chars_in_line)
        move(translated_path,to_compile_text_path)
        # this works because "translated path" is also the file name of to_compile_text_path
        subprocess.run([self.compiler_path,translated_path], cwd=self.get_compiler_resource_folder())
        compiled_captions_path = self.get_compiled_captions_path()
        dest_captions_path = self.get_mod_captions_path()
        move(compiled_captions_path,dest_captions_path)
        # Let's be nice and also move the uncompiled file to the mod folder
        dest_captions_text_path = self.get_mod_captions_text_path()
        move(to_compile_text_path,dest_captions_text_path)

    ## Other files logic - text files not for compilation
    def get_mod_other_path(self, other_file_name):
        return self.get_mod_resource_folder() + "\{}_{}.txt".format(other_file_name,self.language)

    def get_basegame_english_other_path(self,other_file_name):
        return self.game_parent_path + self.game_path +\
               "\\resource\{}_english.txt".format(other_file_name)

    def get_patch_other_path(self,other_file_name):
        filename = "{}_{}.txt".format(other_file_name,self.language)
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            filename = path.abspath(path.join(path.dirname(__file__), filename))
        return filename

    def get_patch_other_csv_path(self,other_file_name):
        return self.game + " translation - "+ other_file_name +".csv"

    def write_other_from_patch(self,other_file_name):
        dest_other_path = self.get_mod_other_path(other_file_name)
        copyfile(self.get_patch_other_path(other_file_name), dest_other_path)

    def write_other_from_csv(self,other_file_name,csv_path):
        dest_other_path = self.get_mod_other_path(other_file_name)
        basegame_other_path = self.get_basegame_english_other_path(other_file_name)
        translated_lines = tt.read_translation_from_csv(csv_path)
        tt.translate(basegame_other_path,dest_other_path,translated_lines,False,self.max_chars_before_break,self.total_chars_in_line)

    # ## Credits logic
    # def get_basegame_credits_path(self):
    #     return self.game_service_path + self.game_path+"\\scripts\\credits.txt"

    ## main write function
    def write_files(self):
        self.create_mod_folders()
        self.write_cfg('autoexec')
        captions_csv_path = self.get_patch_captions_csv_path()
        if (os.path.isfile(captions_csv_path)):
            self.write_captions_from_csv(captions_csv_path)
        else:
           self.write_captions_from_patch()
        for other_file_name in self.other_file_names:
            other_csv_path = self.get_patch_other_csv_path(other_file_name)
            if os.path.isfile(other_csv_path):
                self.write_other_from_csv(other_file_name,other_csv_path)
            else:
                self.write_other_from_patch(other_file_name)
        #TODO handle change font for stanley