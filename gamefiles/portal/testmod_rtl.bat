FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\portal\portal\custom\portl\
    )
ECHO %modpath%

start "" "c:\Program Files\7-Zip\7z.exe" x gamefiles\portal\dist\install_portal_2007_heb_win_rtl_ex.zip -o"gamefiles\portal\dist" -y
:: wait 5 seconds. Seriously.
ping 192.0.2.2 -n 1 -w 5000 > nul
call gamefiles\portal\testmod_generic.bat rtl 2007
del gamefiles\portal\dist\install_portal_2007_heb_win_rtl.exe
del gamefiles\portal\dist\*.reg
del gamefiles\portal\dist\portl_readme.txt

FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\portalRTX\portal_rtx\custom\portl\
    )
ECHO %modpath%

start "" "c:\Program Files\7-Zip\7z.exe" x gamefiles\portal\dist\install_portal_rtx_heb_win_rtl_ex.zip -o"gamefiles\portal\dist" -y
:: wait 5 seconds. Seriously.
ping 192.0.2.2 -n 1 -w 5000 > nul
call gamefiles\portal\testmod_generic.bat rtl rtx
del gamefiles\portal\dist\install_portal_rtx_heb_win_rtl.exe
del gamefiles\portal\dist\*.reg
del gamefiles\portal\dist\portl_readme.txt