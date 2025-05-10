::This should be run from the main project folder
FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\Half-Life 2\hl2\custom\portl
    set completepath=%%A %%B\steamapps\common\Half-Life 2\hl2_complete\
    )
del /s /q "%modpath%"
rd /s /q "%modpath%"

venv\Scripts\python.exe -c "from src.hl2.install_unattended import steam_uninstall;steam_uninstall()"
copy gamefiles\hl2\hl2_complete_source\resource\clientscheme.res "%completepath%\resource\clientscheme.res"
