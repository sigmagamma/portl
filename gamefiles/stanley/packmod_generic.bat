set store=%1
del /Q gamefiles\stanley\dist\*%store%*.*
reg import gamefiles\stanley\utils\%store%.reg
venv\Scripts\python.exe -c "from src.stanley.install_unattended import %store%_uninstall;%store%_uninstall()"
venv\Scripts\python.exe -c "from src.stanley.install_unattended import %store%_female;%store%_female()"
start "" "D:\Program Files\7-Zip\7z.exe" a gamefiles\stanley\dist\install_stanley_heb_win_%store%_female.zip "%modpath%\cfg" "%modpath%\maps" "%modpath%\materials" "%modpath%\resource" "%modpath%\scripts" "%modpath%\portl.txt"
cd gamefiles\stanley
..\..\venv\Scripts\pyinstaller.exe  --clean .\install_stanley_heb_win_%store%.spec
cd ..\..
move gamefiles\stanley\dist\install_stanley_heb_win_%store%.exe gamefiles\stanley\dist\install_stanley_heb_win_%store%_female.exe
venv\Scripts\python.exe -c "from src.stanley.install_unattended import %store%_uninstall;%store%_uninstall()"
venv\Scripts\python.exe -c "from src.stanley.install_unattended import %store%_male;%store%_male()"
start "" "D:\Program Files\7-Zip\7z.exe" a gamefiles\stanley\dist\install_stanley_heb_win_%store%_male.zip "%modpath%\cfg" "%modpath%\maps" "%modpath%\materials" "%modpath%\resource" "%modpath%\scripts" "%modpath%\portl.txt"
cd gamefiles\stanley
..\..\venv\Scripts\pyinstaller.exe  --clean .\install_stanley_heb_win_%store%.spec
cd ..\..
move gamefiles\stanley\dist\install_stanley_heb_win_%store%.exe gamefiles\stanley\dist\install_stanley_heb_win_%store%_male.exe