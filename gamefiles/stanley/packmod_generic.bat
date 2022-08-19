set store=%1
set gender=%2
del /Q gamefiles\stanley\dist\*%store%_%gender%*.*
reg import gamefiles\stanley\utils\%store%.reg
venv\Scripts\python.exe -c "from src.stanley.install_unattended import %store%_uninstall;%store%_uninstall()"
venv\Scripts\python.exe -c "from src.stanley.install_unattended import %store%_%gender%;%store%_%gender%()"
mkdir -p tempzip\thestanleyparable_dlc1
for %%I in (cfg maps materials resource) do robocopy "%modpath%\%%I" tempzip\thestanleyparable_dlc1\%%I /e
copy "%modpath%\portl.txt" tempzip\thestanleyparable_dlc1\portl.txt
IF %store%==epic (
mkdir tempzip\thestanleyparable
copy "%modpath%\..\thestanleyparable\gameinfo.txt" tempzip\thestanleyparable
)
copy gamefiles\stanley\%store%zip\readme.txt tempzip
cd tempzip
start "" "D:\Program Files\7-Zip\7z.exe" a ..\gamefiles\stanley\dist\install_stanley_heb_win_%store%_%gender%.zip *
:: wait 5 seconds. Seriously.
ping 192.0.2.2 -n 1 -w 5000 > nul
cd ..
del /s /q tempzip
rmdir /s /q tempzip
cd gamefiles\stanley
..\..\venv\Scripts\pyinstaller.exe  --clean .\install_stanley_heb_win_%store%.spec
cd ..\..
move gamefiles\stanley\dist\install_stanley_heb_win_%store%.exe gamefiles\stanley\dist\install_stanley_heb_win_%store%_%gender%.exe
