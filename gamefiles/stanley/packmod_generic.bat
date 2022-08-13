set store=%1
del /Q gamefiles\stanley\dist\*%store%*.*
reg import gamefiles\stanley\utils\%store%.reg
venv\Scripts\python.exe -c "from src.stanley.install_unattended import %store%_uninstall;%store%_uninstall()"
venv\Scripts\python.exe -c "from src.stanley.install_unattended import %store%_female;%store%_female()"
mkdir -p tempzip\thestanleyparable_dlc1
for %%I in (cfg maps materials resource portl.txt) do robocopy "%modpath%\%%I" tempzip\thestanleyparable_dlc1\%%I /e
IF %store%==epic (
mkdir tempzip\thestanleyparable
copy "%modpath%\..\thestanleyparable\gameinfo.txt" tempzip\thestanleyparable
)
copy gamefiles\stanley\%store%zip\readme.txt tempzip
cd tempzip
start "" "D:\Program Files\7-Zip\7z.exe" a ..\gamefiles\stanley\dist\install_stanley_heb_win_%store%_female.zip *
:: wait 5 seconds. Seriously.
ping 192.0.2.2 -n 1 -w 5000 > nul
cd ..
del /s /q tempzip
rmdir /s /q tempzip
cd gamefiles\stanley
..\..\venv\Scripts\pyinstaller.exe  --clean .\install_stanley_heb_win_%store%.spec
cd ..\..
move gamefiles\stanley\dist\install_stanley_heb_win_%store%.exe gamefiles\stanley\dist\install_stanley_heb_win_%store%_female.exe
venv\Scripts\python.exe -c "from src.stanley.install_unattended import %store%_uninstall;%store%_uninstall()"
venv\Scripts\python.exe -c "from src.stanley.install_unattended import %store%_male;%store%_male()"
mkdir -p tempzip\thestanleyparable_dlc1
for %%I in (cfg maps materials resource portl.txt) do robocopy "%modpath%\%%I" tempzip\thestanleyparable_dlc1\%%I /e
IF %store%==epic (
mkdir tempzip\thestanleyparable
copy "%modpath%\..\thestanleyparable\gameinfo.txt" tempzip\thestanleyparable
)
copy gamefiles\stanley\%store%zip\readme.txt tempzip
cd tempzip
start "" "D:\Program Files\7-Zip\7z.exe" a ..\gamefiles\stanley\dist\install_stanley_heb_win_%store%_male.zip *
ping 192.0.2.2 -n 1 -w 5000 > nul
cd ..
del /s /q tempzip
rmdir /s /q tempzip
cd gamefiles\stanley
..\..\venv\Scripts\pyinstaller.exe  --clean .\install_stanley_heb_win_%store%.spec
cd ..\..
move gamefiles\stanley\dist\install_stanley_heb_win_%store%.exe gamefiles\stanley\dist\install_stanley_heb_win_%store%_male.exe