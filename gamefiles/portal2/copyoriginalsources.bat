::This should be run from the main project folder, and on a clean portal 2 installation without the mod
set store=steam
FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\portal 2\portal2_dlc3\
    set binpath=%%A %%B\steamapps\common\portal 2\bin
    set updatepath=%%A %%B\steamapps\common\portal 2\update\
    )

copy "%binpath%\vguimatsurface.dll"  gamefiles\portal2\vguimatsurface_orig.dll
copy "%updatepath%\pak01_dir.vpk" gamefiles\portal2\pak01_dir_orig.vpk
copy "%updatepath%\resource\basemodui_tu_english.txt" gamefiles\portal2\update_source\resource\basemodui_tu_english.txt
copy "%updatepath%\resource\basemodui_tu_english.txt" gamefiles\portal2\update_source\resource\basemodui_tu_english.txt