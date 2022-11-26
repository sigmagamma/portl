FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\portal\portal\custom\portl\
    )
ECHO %modpath%

gamefiles\portal\testmod_generic.bat ltr