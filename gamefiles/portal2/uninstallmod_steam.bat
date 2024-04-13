::This should be run from the main project folder
set store=steam
FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\portal 2\portal2_dlc3\
    set binpath=%%A %%B\steamapps\common\portal 2\bin
    set updatepath=%%A %%B\steamapps\common\portal 2\update\
    )

del /s /q "%modpath%"
rd /s /q "%modpath%"
venv\Scripts\python.exe -c "from src.portal2.install_unattended import %store%_uninstall;%store%_uninstall()"
copy gamefiles\portal2\vguimatsurface_orig.dll "%binpath%\vguimatsurface.dll"
copy gamefiles\portal2\pak01_dir_orig.vpk "%updatepath%\pak01_dir.vpk"