FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\Black Mesa\bms\custom\portl\
    )
ECHO %modpath%
DEL /Q gamefiles\blackmesa\dist\install_black_mesa_a_win_ltr.*
call ./gamefiles/blackmesa/packmod_generic.bat ltr arabic
move gamefiles\blackmesa\dist\install_black_mesa_arabic_win_ltr.zip gamefiles\blackmesa\dist\install_black_mesa_a_win_ltr.zip
DEL /Q gamefiles\blackmesa\dist\install_black_mesa_a_win_rtl*.*
call ./gamefiles/blackmesa/packmod_generic.bat rtl arabic
move gamefiles\blackmesa\dist\install_black_mesa_arabic_win_rtl.zip gamefiles\blackmesa\dist\install_black_mesa_a_win_rtl.zip
copy registry/apply_fonts_black_mesa_arabic.reg gamefiles\blackmesa\dist
copy registry/remove_fonts_black_mesa.reg gamefiles\blackmesa\dist
copy arabicrtlzip/portal_readme.txt gamefiles\blackmesa\dist
cd gamefiles\blackmesa\dist
start "" "C:\Program Files\7-Zip\7z.exe" a install_black_mesa_a_win_rtl_ex.zip install_black_mesa_a_win_rtl.exe apply_fonts_black_mesa_arabic.reg remove_fonts_black_mesa.reg portl_readme.txt
start "" "C:\Program Files\7-Zip\7z.exe" a install_black_mesa_a_win_rtl.zip apply_fonts_black_mesa_arabic.reg remove_fonts_black_mesa.reg
:: wait 10 seconds.
ping 192.0.2.2 -n 1 -w 10000 > nul
DEL *.reg
DEL  install_black_mesa_a_win_rtl.exe
DEL portal_readme.txt
cd ..\..\..
