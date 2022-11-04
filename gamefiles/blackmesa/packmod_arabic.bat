FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\Black Mesa\bms\custom\portl\
    )
ECHO %modpath%
DEL /Q gamefiles\blackmesa\dist\install_black_mesa_a_win_ltr.*
call ./gamefiles/blackmesa/packmod_generic.bat ltr arabic
move gamefiles\blackmesa\dist\install_black_mesa_arabic_win_ltr.zip gamefiles\blackmesa\dist\install_black_mesa_a_win_ltr.zip