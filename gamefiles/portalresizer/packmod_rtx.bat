FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\portalrtx\portal_rtx\custom\portl\
    )
ECHO %modpath%
call gamefiles\portalresizer\packmod_generic.bat rtx
