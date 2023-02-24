FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\portalrtx\portal_rtx\custom\portl\
    )
ECHO %modpath%

for %%I in (ltr rtl) do call gamefiles\portal\packmod_generic.bat  %%I rtx
copy registry\apply_fonts_portal_hebrew.reg gamefiles\portal\dist
copy registry\remove_fonts_portal.reg gamefiles\portal\dist
:: copy gamefiles\portal\rtxrtlexe\portl_readme.txt gamefiles\portal\dist
cd gamefiles\portal\dist
:: start "" "C:\Program Files\7-Zip\7z.exe" a install_portal_rtx_heb_win_rtl_ex.zip install_portal_rtx_heb_win_rtl.exe apply_fonts_portal_hebrew.reg remove_fonts_portal.reg portl_readme.txt
start "" "C:\Program Files\7-Zip\7z.exe" a install_portal_rtx_heb_win_rtl.zip apply_fonts_portal_hebrew.reg remove_fonts_portal.reg
:: wait 10 seconds.
ping 192.0.2.2 -n 1 -w 10000 > nul
DEL *.reg
:: DEL  install_portal_rtx_heb_win_rtl.exe
:: DEL portl_readme.txt
cd ..\..\..
