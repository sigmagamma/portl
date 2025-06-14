import datetime
import math
import os
import sys
import time
import winreg
from shutil import copyfile,copy,rmtree,copytree
from os import path
from distutils.dir_util import copy_tree
import vpk
import src.sound_tools as sound_tools
import src.text_tools as tt
import subprocess
import json
from urllib.request import urlopen
import tkinter as tk
from tkinter import filedialog

from src.text_tools import TextTools

REPO = "https://github.com/sigmagamma/portl/"
# this is required due to AV software flagging shutil.move for some reason
def move(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    copyfile(src,dst)
    os.remove(src)


def move_tree(src, dst):
    copy_tree(src, dst)
    rmtree(src)
class FileTools:
    def __init__(self, game_filename,language,gender=None,store='Steam',unattended=False,gameos='WIN'):

        if (game_filename is not None):
            with open(self.get_patch_gamedata(game_filename),'r') as game_data_file:
                data = json.load(game_data_file)
                if data is not None:
                    self.game = data['game']

                    # OS details
                    self.gameos = gameos

                    # game path
                    self.game_parent_path = None
                    self.basegame = data['basegame']
                    self.gameguid = data.get('gameguid')
                    path_guess = None
                    if self.gameguid:
                        path_guess = self.reg_path_windows()
                    elif store == 'Steam':
                        steam_main_folder = data.get('steam_main_folder')
                        if steam_main_folder is not None:
                            steam_path = self.steam_path_windows(steam_main_folder)
                            if steam_path is not None:
                                path_guess = steam_path + "\\" + steam_main_folder
                    if unattended:
                        file_path = path_guess

                    else:
                        if path_guess is None:
                            action_text = "choose"
                        else:
                            action_text = "confirm"
                        root = tk.Tk()
                        root.withdraw()
                        file_path = filedialog.askdirectory(title="Please {} game folder".format(action_text),initialdir=path_guess)
                        root.destroy()
                    self.unattended = unattended

                    if os.path.exists(file_path) and os.path.exists(file_path+"\\"+self.basegame):
                        self.main_folder = os.path.basename(file_path)
                        self.main_path = file_path
                        self.game_parent_path = os.path.dirname(file_path)
                    else:
                        raise Exception("installation cancelled or not a valid game folder")

                    # other details
                    self.basegame_path = "\\" + self.main_folder + "\\" + self.basegame
                    self.store = store
                    self.shortname = data['shortname']
                    self.version = data['version']
                    self.gender = gender
                    self.gender_textures = data.get('gender_textures')
                    if self.gender_textures is None:
                        self.gender_textures = []
                    self.additional_folders = data.get('additional_folders')
                    self.vpk_folders = data.get('vpk_folders')
                    if self.vpk_folders is None:
                        self.vpk_folders = []
                    self.additional_configuration = data.get('additional_configuration')
                    if self.additional_folders is None:
                        self.additional_folders = []
                    #language details
                    change_language = data.get('change_language')
                    if change_language:
                        self.target_language = language
                    else:
                        self.target_language = self.get_original_localization_lang()
                    self.language = language

                    # translation file details
                    # self.caption_file_name = data['caption_file_name']
                    self.other_files = data.get('other_files')
                    if self.other_files is None:
                        self.other_files = []
                    self.max_chars_before_break = data['max_chars_before_break']
                    self.total_chars_in_line = data.get('total_chars_in_line')
                    compiler_game_service_path = data.get('compiler_game_service_path')
                    if compiler_game_service_path is not None:
                        self.compiler_game_parent_path = compiler_game_service_path
                        self.compiler_basegame_path = data.get('compiler_game_path')
                        self.compiler_main_folder = data.get('compiler_game')
                    else:
                        self.compiler_game_parent_path = self.game_parent_path
                        self.compiler_basegame_path = self.basegame_path
                        self.compiler_main_folder = self.main_folder
                    self.compiler_path = self.get_compiler_path()
                    # self.english_captions_text_path = data.get('english_captions_text_path')
                    # if self.english_captions_text_path is None:
                    #     self.english_captions_text_path = self.get_english_captions_text_path()
                    # else:
                    #     self.english_captions_text_path = self.get_patch_file_path(self.english_captions_text_path)

                    # mod folder logic
                    mod_type = data.get('mod_type')
                    self.mod_type = mod_type
                    if mod_type == 'custom':
                        self.mod_folder = self.get_custom_folder()
                    elif mod_type == 'dlc':
                        self.mod_folder = self.get_dlc_folder()
                    self.dlc_compiler = data.get('dlc_compiler')
                    self.not_deletable = data.get('not_deletable')
                    if not self.not_deletable:
                        self.not_deletable = []
                    # scheme file logic - to be removed
                    self.scheme_file_name = data.get("scheme_file_name")
                    self.format_replacements = data.get("format_replacements")
                    self.vpk_file_name = data.get("vpk_file_name")
                    private_file = self.get_patch_gamedata_private(game_filename)

                    # External translation sheet details
                    # self.captions_translation_url = None
                    self.translation_url = None
                    if os.path.exists(private_file):
                        with  open(private_file,'r') as game_data_file_private:
                            data_private = json.load(game_data_file_private)
                            self.translation_url = data_private.get('translation_url')
                            # translation_sheet = data.get('captions_translation_sheet')
                            # if self.translation_url is not None and translation_sheet is not None:
                            #     self.captions_translation_url = self.translation_url + translation_sheet

                    # text transformation details
                    self.captions_prefix = data.get('captions_prefix')
                    if self.captions_prefix is None:
                        self.captions_prefix = ""
                    self.captions_filters = data.get('captions_filters')

                    # CFG disable
                    self.disable_cfg = data.get('disable_cfg')
                    self.text_spacings = data.get('text_spacings')
                    if self.text_spacings is None:
                        self.text_spacings = []
                    self.speech_folder = data.get('speech_folder')
                    self.scene_folder = data.get('scene_folder')
                    self.filter_files = data.get('filter_files')
                    self.filter_out_files = data.get('filter_out_files')

    ##Steam/Epic logic

    def reg_path_windows(self):
        try:
            game_config_path = "System\\GameConfigStore\\Children"
            installpath = None
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, game_config_path, 0, winreg.KEY_READ) as hkey:
                i = -1
                while True:
                    i = i + 1
                    key = winreg.EnumKey(hkey, i)
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, game_config_path + "\\" + key, 0,
                                        winreg.KEY_READ) as gkey:
                        gameguid = None
                        try:
                            gameguid = winreg.QueryValueEx(gkey, "GameDVR_GameGUID")[0]
                            if (gameguid is not None) and (gameguid == self.gameguid):
                                installpath = winreg.QueryValueEx(gkey, "MatchedExeFullPath")[0]
                                break
                        except Exception as e:
                            continue
            if installpath:
                regpath_folder = os.path.dirname(installpath)
                if os.path.exists(regpath_folder):
                    return regpath_folder
            else:
                return None
        except Exception:
            return None


    def steam_path_windows(self,main_folder):
        try:
            hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Valve\\Steam",0, winreg.KEY_READ)
            steam_path = winreg.QueryValueEx(hkey, "InstallPath")
            winreg.CloseKey(hkey)
            steam_path_guess = steam_path[0] + "\\steamapps\\common"
            if os.path.exists(steam_path_guess +"\\" + main_folder):
                return steam_path_guess
            raise Exception()
        except Exception as e:
            # fine, let's hope it's at one of the standard folders
            steam_path_guess = "{}:\\Program Files (x86)\\Steam\\steamapps\\common"
            for i in range(ord('C'), ord('Z')):
                current_guess = steam_path_guess.format(chr(i))
                if os.path.exists(current_guess +"\\" + main_folder):
                    return current_guess
        return None

    # This is unused, but is left for some general reference of how to achieve this
    def epic_path_windows(self):
        epic_manifests_path = None
        try:
            hkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Epic Games\\EOS",0, winreg.KEY_READ)
            epic_manifests_path = winreg.QueryValueEx(hkey, "ModSdkMetadataDir")[0]
            winreg.CloseKey(hkey)
            if not os.path.exists(epic_manifests_path):
                epic_manifests_path = None
                raise Exception
        except Exception as e:
            # fine, let's hope it's at one of the standard folders
            epic_manifests_path_guess = "{}:/ProgramData/Epic/EpicGamesLauncher/Data/Manifests"
            for i in range(ord('C'), ord('Z')):
                current_guess = epic_manifests_path_guess.format(chr(i))
                if os.path.exists(current_guess):
                    epic_manifests_path = current_guess
                    break
        try:
            if epic_manifests_path is not None:
                for filename in os.listdir(epic_manifests_path):
                    manifest = json.load(open(os.path.join(epic_manifests_path,filename),'r'))
                    if manifest.get("DisplayName") == "The Stanley Parable":
                        game_path =  manifest.get('InstallLocation')
                        if os.path.exists(game_path):
                            return os.path.abspath(os.path.join(game_path, os.pardir))
        except:
            return None
        return None
    def steam_path_linux(self):
        return "~/.steam/steam/steamapps/common"

    def steam_path_macos(self):
        return "~/Library/Application Support/Steam/SteamApps/common"
    ## general folder logic
    # patch are the local files of the patch.
    # basegame is the content folder for the original game (usually something like portal/portal)
    # mod is where the mod gets placed (for instance portal/custom/portl)
    # compiler is where caption compilation happens

    def get_patch_gamedata(self,game_filename):
        filename = game_filename
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            filename = path.abspath(path.join(path.dirname(__file__), filename))
        return filename
    def get_patch_gamedata_private(self,game_filename):
        filename = game_filename.replace(".json"," private.json")
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            filename = path.abspath(path.join(path.dirname(__file__), filename))
        return filename
    def get_full_game_path(self):
        return self.game_parent_path + "\\"+self.main_folder

    def get_full_basegame_path(self):
        return self.game_parent_path + self.basegame_path

    def get_basegame_cache_folder(self):
        return self.get_full_basegame_path() + "\\maps\\soundcache"

    def get_basegame_cache_path(self):
        return self.get_basegame_cache_folder()+"\_master.cache"

    def get_basegame_subfolder(self,subfolder):
        return self.get_full_basegame_path() + "\\"+subfolder

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

    def get_sizepatch_custom_folder(self):
        return self.get_custom_parent_folder()+"\sizepatch"

    def get_mod_resource_folder(self):
        return self.mod_folder+"\\resource"

    def get_mod_subfolder(self,subfolder):
        return self.mod_folder + "\\"+subfolder

    def get_mod_scripts_folder(self):
        return self.mod_folder+"\\scripts"


    def get_mod_cache_folder(self):
        return self.mod_folder+"\\maps\\soundcache"

    def get_patch_version_file(self):
        filename = self.get_gamefiles_folder() + "\\portl.txt"
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            filename = path.abspath(path.join(path.dirname(__file__), filename))
        return filename
    def get_mod_version_path(self):
        return self.mod_folder + "\\portl.txt"
    def get_temp_version_path(self,temp_path):
        return temp_path+ "\\portl.txt"
    def write_patch_version_file(self):
        rtl_text=""
        if self.total_chars_in_line is not None:
            rtl_text = "RTL version"
        gender_text = ""
        if self.gender is not None:
            gender_text = " " + self.gender
        with open(self.get_mod_version_path(),'w') as file:
            file.write(self.shortname+"-"+self.version+" "+rtl_text+ " " + self.store + gender_text + " " + self.gameos + "\n"+ REPO)
    def create_mod_folders(self):
        cfg_folder = self.get_mod_cfg_folder()
        if not os.path.exists(cfg_folder):
            os.makedirs(cfg_folder)
        # see here: https://github.com/sigmagamma/portal-text-size-changer
        sizepatch_folder = self.get_sizepatch_custom_folder()
        if os.path.exists(sizepatch_folder):
            rmtree(sizepatch_folder)
        self.write_patch_version_file()
        if self.mod_type == 'dlc':
            basegame_cache_path = self.get_basegame_cache_path()
            if (not self.unattended) and not os.path.exists(basegame_cache_path):
                input("Note: You'll have to start the game, get to the loading screen, wait for a while, and then restart it. Press any key.")
            else:
                if os.path.exists(basegame_cache_path):
                    mod_cache_folder = self.get_mod_cache_folder()
                    if not os.path.exists(mod_cache_folder):
                        os.makedirs(mod_cache_folder)
                    copy(basegame_cache_path,mod_cache_folder)
    def remove_mod_folder(self):
        if not os.path.exists(self.mod_folder):
            return
        temp_path = self.mod_folder+"_"+str(math.floor(time.time()))
        os.makedirs(temp_path)
        moved = False
        for file in self.not_deletable:
            file_path = self.mod_folder+"\\"+file
            new_file_path = temp_path + "\\"+file
            if os.path.exists(file_path):
                if (not moved):
                    move(self.get_mod_version_path(), self.get_temp_version_path(temp_path))
                moved = True
                if os.path.isdir(file_path):
                    move_tree(file_path,new_file_path)
                else:
                    move(file_path,new_file_path)
        rmtree(self.mod_folder)
        if moved:
            os.rename(temp_path,self.mod_folder)
        else:
            rmtree(temp_path)
    def remove_mod(self):
        self.remove_mod_folder()
        for file_data in self.other_files:
            file_store = file_data.get('store')
            if file_store and file_store == self.store and file_data.get('override'):
                self.restore_basegame_english_other_path(file_data)

    def get_compiler_resource_folder(self):
        return self.compiler_game_parent_path + self.compiler_basegame_path + "\\resource"

    def get_compiler_path(self):
        return self.compiler_game_parent_path + \
               "\{}\\bin\captioncompiler.exe".format(self.compiler_main_folder)

    ## Close Captions logic

    def get_mod_captions_path(self,file_data):
        return self.get_mod_resource_folder() + "\{}_{}.dat".format(file_data.get('name'), self.target_language)

    def get_compiled_captions_path(self,file_data):
        if self.dlc_compiler:
            return self.get_mod_resource_folder() + "\{}_{}.dat".format(file_data.get('name'), self.language)
        return self.get_compiler_resource_folder()+"\{}_{}.dat".format(file_data.get('name'),self.language)

    def get_to_compile_text_path(self,file_data):
        return self.get_compiler_resource_folder()+"\{}_{}.txt".format(file_data.get('name'),self.language)
    def get_from_compile_text_path(self,file_data):
        if self.dlc_compiler:
            return "{}_{}.txt".format(file_data.get('name'),self.language)
        return self.get_compiler_resource_folder()+"\{}_{}.txt".format(file_data.get('name'),self.language)

    def get_mod_captions_text_path(self,file_data):
        return self.get_mod_resource_folder() + "\{}_{}.txt".format(file_data.get('name'), self.target_language)


    def get_gamefiles_folder(self):
        return "gamefiles\\"+self.shortname

    ## Other files logic - text files not for compilation
    def get_mod_other_path(self, file_data,use_dest):
        override = file_data.get('override')
        if override:
            language = self.get_localized_suffix(file_data,"english")
        else:
            language = self.get_localized_suffix(file_data, self.target_language)
        name = file_data.get('name')
        extension = self.get_dest_extension_else_extension(file_data,use_dest)
        folder = file_data.get('folder')
        local_temporary_parent_target_folder = file_data.get('local_temporary_parent_target_folder')
        alternative_parent_target_folder = file_data.get('alternative_parent_target_folder')

        if local_temporary_parent_target_folder is None and alternative_parent_target_folder is None:
            target_folder = self.get_mod_subfolder(folder)
        elif alternative_parent_target_folder is not None:
            target_folder = self.get_full_game_path() + "\\" + alternative_parent_target_folder + "\\" + folder
        else:
            target_folder = self.get_local_temporary_target_folder(file_data)
        return target_folder+"\{}{}.{}".format(name,language,extension)
    def get_localized_suffix(self,file_data,language):
        localized = file_data.get('localized')
        if localized:
            return "_"+language
        return ""
    def get_basegame_english_path(self,file_data,backup_flag):
        folder = self.get_basegame_subfolder(file_data.get('folder'))
        return self.get_english_path(folder,file_data,backup_flag)
    def get_local_source_path(self,local_parent_folder,file_data,backup_flag):
        folder = self.get_gamefiles_folder() + "\\" + local_parent_folder  + "\\" + file_data.get('folder')
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            folder = path.abspath(path.join(path.dirname(__file__), folder))
        return self.get_english_path(folder, file_data, backup_flag)

    def get_local_temporary_target_folder(self, file_data):
        local_parent_target_folder = file_data.get('local_temporary_parent_target_folder')
        folder = self.get_gamefiles_folder() + "\\" + local_parent_target_folder  + "\\" + file_data.get('folder')
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            folder = path.abspath(path.join(path.dirname(__file__), folder))
        return folder


    def get_alternative_source_path(self,alternative_parent_folder,file_data,backup_flag):
        folder = self.get_full_game_path() + "\\" + alternative_parent_folder  + "\\" + file_data.get('folder')
        return self.get_english_path(folder, file_data, backup_flag)


    def get_english_path(self,folder,file_data,backup_flag):
        language = self.get_localized_suffix(file_data,"english")
        backup = ""
        if backup_flag:
            backup = "_backup"
        path = folder +"\\"+file_data.get('name')+language+backup+"."+file_data.get('extension')
        return path

    def get_basegame_english_other_path(self,file_data):
        return self.get_basegame_english_path(file_data,backup_flag=False)
    def get_basegame_english_backup_other_path(self,file_data):
        return self.get_basegame_english_path(file_data,backup_flag=True)

    def backup_basegame_english_other_path(self,file_data):
        orig_path = self.get_basegame_english_other_path(file_data)
        backup_path = self.get_basegame_english_backup_other_path(file_data)
        if os.path.exists(orig_path) and not(os.path.exists(backup_path)):
            move(orig_path,backup_path)
    def restore_basegame_english_other_path(self, file_data):
        backup_path = self.get_basegame_english_backup_other_path(file_data)
        if os.path.exists(backup_path):
            move(backup_path,self.get_basegame_english_other_path(file_data))

    def get_dest_extension_else_extension(self,file_data,use_dest):
        extension = file_data.get('extension')
        if use_dest:
            dest_extension = file_data.get('dest_extension')
            if (dest_extension):
                extension = dest_extension
        return extension
    def get_local_other_path(self,file_data,get_from_dest):
        override = file_data.get('override')
        if override:
            language = self.get_localized_suffix(file_data,"english")
        else:
            language = self.get_localized_suffix(file_data, self.target_language)
        return self.get_gamefiles_folder() + "\\"+file_data.get('name')+language+"."+\
               self.get_dest_extension_else_extension(file_data,get_from_dest)

    def get_patch_other_path(self,file_data,get_from_dest):
        filename = self.get_local_other_path(file_data,get_from_dest)
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            filename = path.abspath(path.join(path.dirname(__file__), filename))
        return filename

    def get_patch_other_csv_path(self,file_data):
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            return self.game + " translation - " + file_data.get('name') + ".csv"
        else:
            return self.get_gamefiles_folder() + "\\" + self.game + " translation - " + file_data.get('name') + ".csv"

    def write_other_from_patch(self,file_data):
        if file_data.get('base_override'):
            dest_other_path = self.get_basegame_english_other_path(file_data)
        else:
            #TODO make this more generic
            is_captions = file_data.get('is_captions')
            if is_captions:
                dest_other_path = self.get_mod_captions_path(file_data)
            else:
                dest_other_path = self.get_mod_other_path(file_data,True)
        copyfile(self.get_patch_other_path(file_data,True), dest_other_path)

    def write_other_from_csv(self,file_data,csv_path):
        dest_other_path = self.get_mod_other_path(file_data,False)
        is_on_vpk = file_data.get('is_on_vpk')
        folder = file_data.get('folder')
        name = file_data.get('name')
        extension = file_data.get('extension')
        is_captions = file_data.get('is_captions')
        dest_extension = file_data.get('dest_extension')
        insert_newlines = file_data.get('insert_newlines')
        vpk_relative_path = file_data.get('vpk_relative_path')
        local_parent_source_folder = file_data.get('local_parent_source_folder')
        alternative_parent_source_folder = file_data.get('alternative_parent_source_folder')
        local_temporary_parent_target_folder = file_data.get('local_temporary_parent_target_folder')
        if insert_newlines is None:
            insert_newlines = True
        language = self.get_localized_suffix(file_data,'english')
        basic_formatting = file_data.get('basic_formatting')
        if is_on_vpk:
            source_other_path = self.get_patch_other_path(file_data,False)
            if vpk_relative_path is None:
                vpk_path = self.get_basegame_vpk_path()
            else:
                vpk_path = self.main_path + "\\" + vpk_relative_path
            self.save_file_from_vpk(folder+"/"+name+language+'.'+extension,source_other_path,vpk_path)
        else:
            if local_parent_source_folder is not None:
                source_other_path = self.get_local_source_path(local_parent_source_folder,file_data,False)
            elif alternative_parent_source_folder is not None:
                source_other_path = self.get_alternative_source_path(alternative_parent_source_folder, file_data, False)
            else:
                basegame_other_path = self.get_basegame_english_other_path(file_data)
                backup_basegame_other_path = self.get_basegame_english_backup_other_path(file_data)
                if os.path.exists(basegame_other_path):
                    source_other_path = basegame_other_path
                elif os.path.exists(backup_basegame_other_path):
                    source_other_path = backup_basegame_other_path
                else:
                    raise Exception(
                        "file " + basegame_other_path + " or " + backup_basegame_other_path + " don't exist. Verify game files integrity")
        translated_lines,scene_map = tt.read_translation_from_csv(csv_path, self.gender, self.store, self.gameos)
        encoding = file_data.get('encoding')
        song_mode = file_data.get('song_mode')
        override = file_data.get('override')
        if not override:
            if local_temporary_parent_target_folder is None:
                target_folder = self.get_mod_subfolder(folder)
            else:
                target_folder = self.get_local_temporary_target_folder(file_data)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
        TextTools(source_other_path,dest_other_path,translated_lines,is_captions,
                                         self.max_chars_before_break,self.total_chars_in_line,self.language,
                                        insert_newlines=insert_newlines,source_encoding= encoding,
                                         prefix=self.captions_prefix,filters=self.captions_filters,
                                        basic_formatting=basic_formatting,text_spacings=self.text_spacings,
                                         song_mode=song_mode).translate()
        if dest_extension:
            to_compile_text_path = self.get_to_compile_text_path(file_data)
            from_compile_text_path = self.get_from_compile_text_path(file_data)
            move(dest_other_path, to_compile_text_path)

            # this works because "translated path" is also the file name of to_compile_text_path
            if self.dlc_compiler:
                dlc_folder, dlc_number = self.search_dlc_folders()
                subprocess.check_output([self.compiler_path, from_compile_text_path,"-d",str(dlc_number)], cwd=self.get_compiler_resource_folder())
            else:
                subprocess.run([self.compiler_path, from_compile_text_path],
                               cwd=self.get_compiler_resource_folder())
            # TODO generalize this
            compiled_captions_path = self.get_compiled_captions_path(file_data)
            #TODO make this work for local_temporary_parent_target_folder
            dest_captions_path = self.get_mod_captions_path(file_data)
            move(compiled_captions_path, dest_captions_path)
            # Let's be nice and also move the uncompiled file to the mod folder
            dest_captions_text_path = self.get_mod_captions_text_path(file_data)
            move(to_compile_text_path, dest_captions_text_path)
        if is_on_vpk:
            os.remove(source_other_path)
        if scene_map:
            for scene_filename,scene in scene_map.items():
                speech_folder = self.get_mod_subfolder(self.speech_folder)
                source_scene_filename = os.path.join(self.get_basegame_subfolder(self.scene_folder),scene_filename)
                target_scene_filename = os.path.join(self.get_mod_subfolder(self.scene_folder),scene_filename)
                sound_tools.rewrite_scene(speech_folder,source_scene_filename,target_scene_filename,scene)

    def get_basegame_vpk_path(self):
        return self.get_full_basegame_path() + "\\" + self.vpk_file_name

    def save_file_from_vpk(self,path_in_vpk,path_on_disk,vpk_path):
        if os.path.exists(vpk_path):
            pak = vpk.open(vpk_path)
            pakfile = pak.get_file(path_in_vpk)
            pakfile.save(path_on_disk)
            pakfile.close()

        else:
            raise Exception("file " +vpk_path + " doesn't exist. Verify game files integrity")

    # assets logic - copy entire folders from patch
    def get_mod_asset_path(self,filename):
        return self.mod_folder+"/"+filename

    def get_patch_file_path(self, filename):
        filename = self.get_gamefiles_folder()+"\\"+filename
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            filename = path.abspath(path.join(path.dirname(__file__), filename))
        return filename

    def copy_assets(self,patch=False):
        for filename in self.additional_folders:
            src_path = self.get_patch_file_path(filename)
            if os.path.exists(src_path):
                copy_tree(src_path,self.get_mod_asset_path(filename),preserve_mode=0)
        if (not patch) and self.gender is not None and 'materials' in self.additional_folders:
            for texture in self.gender_textures:
                gender_texture_path = self.get_mod_asset_path("materials")+"\\"+texture+"_"+self.gender+".vtf"
                if os.path.exists(gender_texture_path):
                    dest_texture_path = self.get_mod_asset_path("materials")+"\\"+texture+".vtf"
                    move(gender_texture_path,dest_texture_path)
        for vpk_details in self.vpk_folders:
            source_folder = vpk_details.get('source_folder')
            target_name = vpk_details.get('target_name')
            temp_src_path =  self.get_patch_file_path("temp_vpk")
            rmtree(temp_src_path,ignore_errors=True)
            copytree(self.get_patch_file_path(source_folder),temp_src_path)
            if self.gender is not None:
                gender_path = self.get_patch_file_path(self.gender + "_" + source_folder)
                if os.path.exists(gender_path):
                    copytree(gender_path,temp_src_path,dirs_exist_ok=True)

            vpk_created = vpk.NewVPK(temp_src_path)
            target_folder = vpk_details.get('target_folder')
            if target_folder == None:
                target_folder = self.mod_folder
            else:
                target_folder = self.main_path + "/" + target_folder
            vpk_created.version = 1
            vpk_created.save(target_folder+"/"+target_name+".vpk")
            rmtree(temp_src_path)
        #TODO handle gender textures for vpk
    def get_mod_cfg_folder(self):
        return self.mod_folder + "\cfg"

    def get_mod_cfg_path(self, filename):
        return self.get_mod_cfg_folder() + "\{}".format(filename)

    def get_basegame_cfg_folder(self):
        return self.get_full_basegame_path() + "\cfg"
    def get_basegame_cfg_path(self, filename):
        return self.get_basegame_cfg_folder()+"\{}".format(filename)

    def get_lang_from_cfg(self,cfg_path):
        lang = ''
        if (os.path.isfile(cfg_path)):
            with open(cfg_path, 'r') as f_in:
                for line in f_in:
                    if lang == '' and line.startswith("cc_lang"):
                        lang_line = line
                        lang = (lang_line.split('"'))[1]
                        break
        return lang

    # best effort to find user's localization lang and override it so that after
    # uninstallation configuration won't be affected
    def get_original_localization_lang(self):
        src_config_path = self.get_basegame_cfg_path('config.cfg')
        lang = self.get_lang_from_cfg(src_config_path)
        # using a non-official localization as the language to override in old versions was a mistake
        # might not be able to correct it, but can avenge it
        # dfd_english is some sort of bizzare override from mods
        if lang == '' or lang == 'hebrew' or lang == 'dfd_English':
            lang = 'english'
        return lang

    def write_autoexec_cfg(self):
        #TODO move this to spreadsheet
        with open(self.get_mod_cfg_path('autoexec.cfg'), 'w') as file:
            file.write('cc_subtitles "1"\n')
            file.write('cc_lang "' + self.target_language + '"\n')
            file.write('closecaption "1"' + '"\n')
            if self.additional_configuration:
                file.write(self.additional_configuration)

    def get_csv_from_url(self,filename,url):
        response = urlopen(url)
        if response.status == 200:
            with open(filename, 'w', encoding='utf-8') as file:
                for line in response:
                    file.write(line.decode('utf-8'))

    ## main write function
    def write_files(self):
        self.create_mod_folders()
        if (not self.disable_cfg):
            self.write_autoexec_cfg()
        # need to copy assets first since scenes are based on sounds
        self.copy_assets()

        for file_data in self.other_files:
            if self.filter_files and file_data.get('name') not in self.filter_files:
                continue
            if self.filter_out_files and file_data.get('name') in self.filter_out_files:
                continue
            file_store = file_data.get('store')
            if file_store and file_store != self.store:
                continue
            if file_data.get('override'):
                self.backup_basegame_english_other_path(file_data)
            other_csv_path = self.get_patch_other_csv_path(file_data)
            sheet = file_data.get("translation_sheet")
            file_url = None
            if sheet is not None and self.translation_url is not None:
                file_url = self.translation_url + sheet
                self.get_csv_from_url(other_csv_path, file_url)
            if os.path.isfile(other_csv_path):
                self.write_other_from_csv(file_data,other_csv_path)
                if file_url is not None:
                    os.remove(other_csv_path)
            else:
                self.write_other_from_patch(file_data)
            if file_data.get('override'):
                self.backup_basegame_english_other_path(file_data)

        # let's copy the assets again to make sure we got everything
        self.copy_assets()
        print(datetime.datetime.now())
    ## patch write function
    def write_patch_files(self):
        self.create_mod_folders()
        if (not self.disable_cfg):
            self.write_autoexec_cfg()
        # self.write_captions_from_patch()
        for file_data in self.other_files:
            file_store = file_data.get('store')
            if file_store and file_store != self.store:
                continue
            if file_data.get('override'):
                self.backup_basegame_english_other_path(file_data)
            self.write_other_from_patch(file_data)
        self.copy_assets(patch=True)