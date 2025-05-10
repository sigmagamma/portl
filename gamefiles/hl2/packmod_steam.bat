::This should be run from the main project folder
del /s /q  gamefiles\hl2\dist

mkdir gamefiles\hl2\dist
del /s /q  gamefiles\hl2\hl2
mkdir gamefiles\hl2\hl2\custom\portl\resource
del /s /q  gamefiles\hl2\hl2_complete
mkdir gamefiles\hl2\hl2_complete\resource

FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\Half-Life 2\hl2\custom\portl\
    set completepath=%%A %%B\steamapps\common\Half-Life 2\hl2_complete\
    )
set nsisbinpath="C:\Program Files (x86)\NSIS\Bin"

call gamefiles\hl2\uninstallmod_steam.bat


venv\Scripts\python.exe -c "from src.hl2.install_unattended import steam_install;steam_install()"

robocopy "%modpath%\resource" gamefiles\hl2\custom\portl\resource /e
copy "%completepath%resource\clientscheme.res" gamefiles\hl2\hl2_complete\resource\clientscheme.res
copy "%modpath%\portl.txt" gamefiles\hl2\hl2\portl.txt

cd gamefiles\hl2
%nsisbinpath%\makensis.exe hl2.nsi
move hl2-arabic-installer.exe dist
cd ..\..
