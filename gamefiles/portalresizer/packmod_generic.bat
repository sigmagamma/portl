set edition=%1
del /Q gamefiles\portalresizer\dist\*%edition%_resizer.*
venv\Scripts\python.exe -c "from src.portal.install_unattended import uninstall_%edition%;uninstall_%edition%()"
venv\Scripts\python.exe -c "from src.portal.install_unattended import resizer_%edition%_install;resizer_%edition%_install()"
mkdir -p tempzip\custom\portl
for %%I in (resource) do robocopy "%modpath%\%%I" tempzip\custom\portl\%%I /e
copy "%modpath%\portl.txt" tempzip\custom\portl\portl.txt
copy gamefiles\portalresizer\%edition%zip\portl_readme.txt tempzip
cd tempzip
start "" "C:\Program Files\7-Zip\7z.exe" a ..\gamefiles\portalresizer\dist\install_portal_%edition%_resizer.zip *
:: wait 5 seconds. Seriously.
ping 192.0.2.2 -n 1 -w 5000 > nul
cd ..
del /s /q tempzip
rmdir /s /q tempzip
cd gamefiles\portalresizer
..\..\venv\Scripts\pyinstaller.exe  --clean .\install_portal_%edition%_resizer.spec
cd ..\..
