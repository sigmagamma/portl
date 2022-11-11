set align=%1
set language=%2
del /Q gamefiles\blackmesa\dist\*%language%*%align%*.*
venv\Scripts\python.exe -c "from src.blackmesa.install_unattended import uninstall;uninstall()"
venv\Scripts\python.exe -c "from src.blackmesa.install_unattended import %language%_%align%_install;%language%_%align%_install()"
mkdir -p tempzip\bms\custom\portl
for %%I in (cfg maps materials resource scripts) do robocopy "%modpath%\%%I" tempzip\bms\custom\portl\%%I /e
copy "%modpath%\portl.txt" tempzip\bms\custom\portl\portl.txt
copy gamefiles\blackmesa\%language%%align%zip\portl_readme.txt tempzip
cd tempzip
start "" "C:\Program Files\7-Zip\7z.exe" a ..\gamefiles\blackmesa\dist\install_black_mesa_%language%_win_%align%.zip *
:: wait 5 seconds. Seriously.
ping 192.0.2.2 -n 1 -w 10000 > nul
cd ..
del /s /q tempzip
rmdir /s /q tempzip
cd gamefiles\blackmesa
..\..\venv\Scripts\pyinstaller.exe  --clean .\install_black_mesa_%language%_win_%align%.spec
cd ..\..
