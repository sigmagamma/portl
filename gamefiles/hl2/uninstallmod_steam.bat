::This should be run from the main project folder
FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\Half-Life 2\hl2\custom\portl
    set completepath=%%A %%B\steamapps\common\Half-Life 2\hl2_complete
    set episodicpath=%%A %%B\steamapps\common\Half-Life 2\episodic
    set ep2path=%%A %%B\steamapps\common\Half-Life 2\ep2
    set lostcoastpath=%%A %%B\steamapps\common\Half-Life 2\lostcoast
    set platformpath=%%A %%B\steamapps\common\Half-Life 2\platform
    set hl2path=%%A %%B\steamapps\common\Half-Life 2\hl2
    )
del /s /q "%modpath%"
rd /s /q "%modpath%"

venv\Scripts\python.exe -c "from src.hl2.install_unattended import steam_uninstall;steam_uninstall()"
copy gamefiles\hl2\hl2_complete_source\resource\clientscheme.res "%completepath%\resource\clientscheme.res"
copy gamefiles\hl2\lostcoast_source\resource\lostcoast_english.txt "%lostcoastpath%\resource\lostcoast_english.txt"
copy gamefiles\hl2\ep2_source\resource\ep2_english.txt "%ep2path%\resource\ep2_english.txt"
copy gamefiles\hl2\episodic_source\resource\episodic_english.txt "%episodicpath%\resource\episodic_english.txt"
copy gamefiles\hl2\platform_source\resource\vgui_english.txt "%platformpath%\resource\vgui_english.txt"
copy gamefiles\hl2\hl2_source\resource\valve_english.txt "%hl2path%\resource\valve_english.txt"
del /s /q "%ep2path%\scripts
rmdir "%ep2path%\scripts
del /s /q "%episodicpath%\scripts"
rmdir "%episodicpath%\scripts"