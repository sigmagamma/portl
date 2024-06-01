::This should be run from the main project folder
del /s /q  gamefiles\portal2\dist

mkdir gamefiles\portal2\dist
del /s /q  gamefiles\portal2\generic
mkdir gamefiles\portal2\generic
del /s /q gamefiles\portal2\bin
mkdir gamefiles\portal2\bin

FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\portal 2\portal2_dlc3\
    )
set nsisbinpath="C:\Program Files (x86)\NSIS\Bin"

%nsisbinpath%\GenPat.exe  "C:\projects\portalhebrew\gamefiles\portal2\vguimatsurface_orig.dll" "C:\projects\portalhebrew\gamefiles\portal2\vguimatsurface.dll"  C:\projects\portalhebrew\gamefiles\portal2\bin\vguimatsurface.dll.patch
call gamefiles\portal2\uninstallmod_steam.bat
for %%I in (glados mabsuta) do call gamefiles\portal2\packmod_generic.bat %%I
for %%I in (cfg scripts resource media maps) do robocopy "%modpath%\%%I" gamefiles\portal2\generic\portal2_dlc3\%%I /e
%nsisbinpath%\GenPat.exe  "C:\projects\portalhebrew\gamefiles\portal2\pak01_dir_orig.vpk" "C:\Program Files (x86)\Steam\steamapps\common\Portal 2\update\pak01_dir.vpk"  C:\projects\portalhebrew\gamefiles\portal2\update\pak01_dir.vpk.patch
copy "%modpath%\portl.txt" gamefiles\portal2\generic\portal2_dlc3\portl.txt

cd gamefiles\portal2
%nsisbinpath%\makensis.exe portal2.nsi
move portal-2-hebrew-installer.exe dist
cd ..\..
