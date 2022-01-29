import os
import sys
import winreg
from shutil import copyfile
from shutil import move
from shutil import rmtree
from os import path
import text_tools as tt
import subprocess

game_data = \
    {
        "Portal": {
            "path":"\Portal\portal",
            "caption_file_name":"closecaption",
            "other_file_names": ["portal"]
        }
    }


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
    def __init__(self, game,game_service_path,language,compiler_path=None):

        if (game is not None):
            data = game_data.get(game)
            if data is not None:
                self.game = game
                self.game_path = data['path']
                self.caption_file_name = data['caption_file_name']
                self.other_file_names = data['other_file_names']
                self.game_parent_path = game_service_path
                self.language = language
                if compiler_path is not None:
                    self.compiler_path = compiler_path
                else:
                    self.compiler_path = self.get_compiler_path()
            else:
                return None
        return None

    def get_basegame_resource_folder(self):
        return self.game_parent_path + self.game_path + "\\resource"

    def get_custom_folder(self):
        return self.game_parent_path + self.game_path + "\custom\portl"

    def get_custom_cfg_folder(self):
        return self.game_parent_path + self.game_path + "\custom\portl\cfg"

    def get_custom_resource_folder(self):
        return self.game_parent_path + self.game_path + "\custom\portl\\resource"

    def create_custom_folders(self):
        custom_folder = self.get_custom_folder()
        custom_cfg_folder = self.get_custom_cfg_folder()
        custom_resource_folder = self.get_custom_resource_folder()
        if not os.path.exists(custom_folder):
            os.mkdir(custom_folder)
        if not os.path.exists(custom_cfg_folder):
            os.mkdir(custom_cfg_folder)
        if not os.path.exists(custom_resource_folder):
            os.mkdir(custom_resource_folder)

    def remove_custom_folder(self):
        rmtree(self.get_custom_folder())

    def get_compiler_path(self):
        return self.game_parent_path + \
               "\{}\\bin\captioncompiler.exe".format(self.game)

    # patch are the local files of the patch. basegame is the content folder
    # for the original game (usually something like portal/portal)
    # while custom is where the mod gets placed (so portal/custom/portl)

    ## cfg files logic

    def get_patch_cfg_path(self,type):
        filename = "{}.cfg".format(type)
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            filename = path.abspath(path.join(path.dirname(__file__), filename))
        return filename

    def get_basegame_cfg_path(self, type):
        return self.game_parent_path + self.game_path + "\cfg\{}.cfg".format(type)

    def get_custom_cfg_path(self,type):
        return self.game_parent_path + self.game_path + "\custom\portl\cfg\{}.cfg".format(type)

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
        dest_cfg_path = self.get_custom_cfg_path(type)
        if type != 'config':
            new_cfg_path = self.get_patch_cfg_path(type)
            copyfile(new_cfg_path, dest_cfg_path)
        else:
            src_cfg_path = self.get_basegame_cfg_path(type)
            lang_replacement = 'cc_lang "' + self.language + '"\n'
            subtitles_replacement = 'cc_subtitles "1"'
            self.write_replacement_cfg(src_cfg_path, dest_cfg_path, lang_replacement, subtitles_replacement)



    ## Close Captions logic


    def get_custom_captions_path(self):
        return self.game_parent_path + self.game_path +\
               "\custom\portl\\resource\{}_{}.dat".format(self.caption_file_name,self.language)

    def get_basegame_captions_path(self):
        return self.game_parent_path + self.game_path +\
               "\\resource\{}_{}.dat".format(self.caption_file_name,self.language)

    def get_basegame_captions_text_path(self):
        return self.game_parent_path + self.game_path +\
               "\\resource\{}_{}.txt".format(self.caption_file_name,self.language)


    def get_custom_captions_text_path(self):
        return self.game_parent_path + self.game_path +\
               "\custom\portl\\resource\{}_{}.txt".format(self.caption_file_name,self.language)

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
        dest_captions_path = self.get_custom_captions_path()
        copyfile(self.get_patch_captions_path(), dest_captions_path)

    def write_captions_from_csv(self,compiler_path,csv_path):
        orig_captions_text_path = self.get_english_captions_text_path()
        # captions are compiled in the basegame folder
        basegame_captions_text_path = self.get_basegame_captions_text_path()
        translated_path = "{}_{}.txt".format(self.caption_file_name,self.language)
        translated_lines = tt.read_translation_from_csv(csv_path)
        tt.translate(orig_captions_text_path,translated_path,translated_lines,True)
        move(translated_path,basegame_captions_text_path)
        subprocess.run([compiler_path,translated_path], cwd=self.get_basegame_resource_folder())
        basegame_captions_path = self.get_basegame_captions_path()
        dest_captions_path = self.get_custom_captions_path()
        move(basegame_captions_path,dest_captions_path)
        # Let's be nice and also move the uncompiled file to the custom folder
        dest_captions_text_path = self.get_custom_captions_text_path()
        move(basegame_captions_text_path,dest_captions_text_path)

    ## Other files logic - text files not for compilation
    def get_custom_other_path(self,other_file_name):
        return self.game_parent_path + self.game_path +\
               "\custom\portl\\resource\{}_{}.txt".format(other_file_name,self.language)

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
        dest_other_path = self.get_custom_other_path(other_file_name)
        copyfile(self.get_patch_other_path(other_file_name), dest_other_path)

    def write_other_from_csv(self,other_file_name,csv_path):
        dest_other_path = self.get_custom_other_path(other_file_name)
        basegame_other_path = self.get_basegame_english_other_path(other_file_name)
        translated_lines = tt.read_translation_from_csv(csv_path)
        tt.translate(basegame_other_path,dest_other_path,translated_lines,False)

    # ## Credits logic
    # def get_basegame_credits_path(self):
    #     return self.game_service_path + self.game_path+"\\scripts\\credits.txt"

    ## main write function
    def write_files(self):
        self.create_custom_folders()
        self.write_cfg('autoexec')
        captions_csv_path = self.get_patch_captions_csv_path()
        if (os.path.isfile(captions_csv_path)):
            self.write_captions_from_csv(self.compiler_path,captions_csv_path)
        else:
           self.write_captions_from_patch()
        for other_file_name in self.other_file_names:
            other_csv_path = self.get_patch_other_csv_path(other_file_name)
            if os.path.isfile(other_csv_path):
                self.write_other_from_csv(other_file_name,other_csv_path)
            else:
                self.write_other_from_patch(other_file_name)
