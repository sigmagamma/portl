set align=%1
del /Q gamefiles\portal\dist\*%align%*.*
venv\Scripts\python.exe -c "from src.portal.install_unattended import uninstall;uninstall()"
venv\Scripts\python.exe -c "from src.portal.install_unattended import hebrew_%align%_install;hebrew_%align%_install()"
mkdir -p tempzip\custom\portl
for %%I in (cfg maps materials resource scripts) do robocopy "%modpath%\%%I" tempzip\custom\portl\%%I /e
copy "%modpath%\portl.txt" tempzip\custom\portl\portl.txt
copy gamefiles\portal\%align%zip\portl_readme.txt tempzip
cd tempzip
start "" "C:\Program Files\7-Zip\7z.exe" a ..\gamefiles\portal\dist\install_portal_heb_win_%align%.zip *
:: wait 5 seconds. Seriously.
ping 192.0.2.2 -n 1 -w 5000 > nul
cd ..
del /s /q tempzip
rmdir /s /q tempzip
cd gamefiles\portal
..\..\venv\Scripts\pyinstaller.exe  --clean .\install_portal_heb_win_%align%.spec
cd ..\..
