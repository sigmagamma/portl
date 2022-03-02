import os
import sys
import winreg
from shutil import copyfile,copy,move,rmtree
from os import path
import text_tools as tt
import subprocess
import json
import shlex
import re

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
                    self.basegame = data['basegame']
                    self.basegame_path = "\\" + self.game + "\\" + self.basegame
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
                        self.compiler_basegame_path = data.get('compiler_game_path')
                        self.compiler_game = data.get('compiler_game')
                    else:
                        self.compiler_game_parent_path = self.game_parent_path
                        self.compiler_basegame_path = self.basegame_path
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
                    self.os = data.get('os')
                    self.scheme_file_name = data.get("scheme_file_name")
                    self.format_replacements = data.get("format_replacements")
                else:
                    return None
        else:
            return None

    ## general folder logic
    # patch are the local files of the patch.
    # basegame is the content folder for the original game (usually something like portal/portal)
    # mod is where the mod gets placed (for instance portal/custom/portl)
    # compiler is where caption compilation happens
    def get_full_game_path(self):
        return self.game_parent_path + "\\"+self.game

    def get_basegame_cfg_folder(self):
        return self.get_full_basegame_path() + "\cfg"

    def get_full_basegame_path(self):
        return self.game_parent_path + self.basegame_path

    def get_basegame_cache_folder(self):
        return self.get_full_basegame_path() + "\\maps\\soundcache"

    def get_basegame_cache_path(self):
        return self.get_basegame_cache_folder()+"\_master.cache"

    def get_basegame_resource_folder(self):
        return self.get_full_basegame_path() + "\\resource"

    def search_dlc_folders(self):
        dlcs = [a for a in os.listdir(self.get_full_game_path()) if a.startswith(self.basegame+'_dlc')]
        dlc_seq = 0
        for dlc in dlcs:
            number = dlc.replace(self.basegame+'_dlc','')
            if number.isnumeric():
                num = int(number)
                if num > dlc_seq:
                    dlc_seq = num
            folder = self.get_full_game_path()+"\\"+dlc
            if os.path.exists(folder + "\\" + "portl.txt"):
                return folder,dlc_seq
        return None,dlc_seq
    def get_dlc_folder(self):
        folder,number = self.search_dlc_folders()
        if folder is not None:
            return folder
        number = number + 1
        return self.get_full_basegame_path() + "_dlc" + str(number)

    def get_custom_parent_folder(self):
        return self.get_full_basegame_path() + "\custom"

    def get_custom_folder(self):
        return self.get_custom_parent_folder()+"\portl"

    def get_mod_cfg_folder(self):
        return self.mod_folder+"\cfg"

    def get_mod_resource_folder(self):
        return self.mod_folder+"\\resource"

    def get_mod_cache_folder(self):
        return self.mod_folder+"\\maps\\soundcache"

    def get_patch_version_file(self):
        return "portl.txt"

    def create_mod_folders(self):
        mod_cfg_folder = self.get_mod_cfg_folder()
        if not os.path.exists(mod_cfg_folder):
            os.makedirs(mod_cfg_folder)
        mod_resource_folder = self.get_mod_resource_folder()
        if not os.path.exists(mod_resource_folder):
            os.makedirs(mod_resource_folder)
        copy(self.get_patch_version_file(), self.mod_folder)
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

    def get_compiler_resource_folder(self):
        return self.compiler_game_parent_path + self.compiler_basegame_path + "\\resource"

    def get_compiler_path(self):
        return self.compiler_game_parent_path + \
               "\{}\\bin\captioncompiler.exe".format(self.compiler_game)


    ## cfg files logic

    def get_patch_cfg_path(self,type):
        filename = "{}.cfg".format(type)
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            filename = path.abspath(path.join(path.dirname(__file__), filename))
        return filename

    def get_basegame_cfg_path(self, type):
        return self.get_basegame_cfg_folder()+"\{}.cfg".format(type)

    def get_mod_cfg_path(self, type):
        return self.get_mod_cfg_folder() + "\{}.cfg".format(type)

    # for either lang or subtitle line provided, if they exist in file, replace them
    # otherwise add the line
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
        return self.get_compiler_resource_folder()+"\{}_{}.dat".format(self.caption_file_name,self.language)

    def get_to_compile_text_path(self):
        return self.get_compiler_resource_folder()+"\{}_{}.txt".format(self.caption_file_name,self.language)


    def get_mod_captions_text_path(self):
        return self.get_mod_resource_folder() + "\{}_{}.txt".format(self.caption_file_name,self.language)

    def get_patch_captions_path(self):
        filename = "{}_{}.dat".format(self.caption_file_name,self.language)
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            filename = path.abspath(path.join(path.dirname(__file__), filename))
        return filename


    def get_english_captions_text_path(self):
        return self.get_basegame_resource_folder()+"\{}_english.txt".format(self.caption_file_name)

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
        return self.get_basegame_resource_folder()+"\{}_english.txt".format(other_file_name)

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

    ## scheme files logic
    def check_compatibility(self,platform_string):
        lexer = shlex.shlex(platform_string)
        state = True
        negate = False
        parantheses = False
        in_paran = ""
        for token in lexer:
            if token == ")":
                state = self.check_compatibility(in_paran) != negate
                negate = False
                in_paran = ""
            elif parantheses:
                in_paran += token
            elif token == "!":
                negate = True
            elif token == "||" and state:
                break
            elif token == "&&" and not state:
                break
            elif token == "$":
                continue
            elif token == "(":
                parantheses = True
            else:
                compatability = (token == self.os) or (token == "GAMECONSOLE" and self.os in ["X360","PS3"])
                state = compatability != negate
                negate = False
        return state


    def write_scheme_file(self,source_scheme_path, dest_scheme_path,format_replacements):
        with open(source_scheme_path, 'r') as f_in, open(dest_scheme_path, 'w') as f_out:
            while True:
                line = f_in.readline()
                if not line:
                    break
                for key in format_replacements.keys():
                    compare_key = "\""+key+"\""
                    potential_key = line.strip()
                    if potential_key.startswith(compare_key):
                        f_out.write(line)
                        f_out.write(f_in.readline())
                        replacement = format_replacements.get(key)
                        next = f_in.readline()
                        while True:
                            next_stripped =  next.strip("\"\t\n")
                            if not next_stripped.isnumeric():
                                f_out.write(next)
                                break
                            f_out.write(next)
                            format = replacement.get(next_stripped)
                            if format is not None:
                                f_out.write(f_in.readline())
                                while True:
                                    field_value = f_in.readline()
                                    if field_value.strip("\"\t\n") == "}":
                                        f_out.write(field_value)
                                        next = f_in.readline()
                                        break
                                    # TODO that's very specific. rethink this
                                    fv_array = [ a for a in re.split('\"\s{1,}\"|\s{1,}\"|]\s{1,}|\"\s{1,}\[',field_value) if a != '']
                                    if len(fv_array) > 2 and not self.check_compatibility(fv_array[2]):
                                        f_out.write(field_value)
                                        continue
                                    fv_key = fv_array[0]
                                    value = format.get(fv_key)
                                    if value is not None:
                                        field_value = field_value.replace(fv_array[1],value)
                                    f_out.write(field_value)
                    else:
                        f_out.write(line)

    def get_basegame_scheme_path(self):
        return self.get_basegame_resource_folder()+"\\"+self.scheme_file_name

    def get_mod_scheme_path(self):
        return self.get_mod_resource_folder() + "\\" + self.scheme_file_name

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
        if self.scheme_file_name is not None:
            self.write_scheme_file(self.get_basegame_scheme_path(),self.get_mod_scheme_path(),self.format_replacements)