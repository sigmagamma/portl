::This should be run from the main project folder
del /s /q  gamefiles\portal2\dist_arabic

mkdir gamefiles\portal2\dist_arabic
del /s /q  gamefiles\portal2\generic
mkdir gamefiles\portal2\generic
mkdir gamefiles\portal2\generic\update
mkdir gamefiles\portal2\generic\update\resource

FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\portal 2\portal2_dlc3\
    )
set nsisbinpath="C:\Program Files (x86)\NSIS\Bin"

call gamefiles\portal2\uninstallmod_steam.bat
venv\Scripts\python.exe -c "from src.portal2.install_unattended import arabic_steam_glados_WIN;arabic_steam_glados_WIN()"

for %%I in (cfg scripts resource media maps) do robocopy "%modpath%\%%I" gamefiles\portal2\generic\portal2_dlc3\%%I /e
copy "%modpath%..\update\pak01_dir.vpk" gamefiles\portal2\generic\update\pak01_dir.vpk
copy "%modpath%\..\update\resource\basemodui_tu_english.txt" gamefiles\portal2\generic\update\resource\basemodui_tu_english.txt
copy "%modpath%\portl.txt" gamefiles\portal2\generic\portal2_dlc3\portl.txt
copy "%modpath%\pak01_dir.vpk" gamefiles\portal2\generic\portal2_dlc3\pak01_dir.vpk
robocopy gamefiles\portal2\game_assets_arabic\media gamefiles\portal2\generic\portal2_dlc3\media
cd gamefiles\portal2
%nsisbinpath%\makensis.exe portal2_arabic.nsi
move portal-2-arabic-installer.exe dist_arabic
cd ..\..
