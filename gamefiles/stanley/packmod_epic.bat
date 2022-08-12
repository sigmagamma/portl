::This should be run from the main project folder
set modpath=D:\Program Files\Epic Games\TheStanleyParable\thestanleyparable_dlc1\
ECHO %modpath%
del /Q gamefiles\stanley\dist\*.*
venv\Scripts\python.exe -c "from src.stanley.install_unattended import epic_uninstall;epic_uninstall()"
venv\Scripts\python.exe -c "from src.stanley.install_unattended import epic_female;epic_female()"
start "" "D:\Program Files\7-Zip\7z.exe" a gamefiles\stanley\dist\install_stanley_heb_win_epic_female.zip "%modpath%\cfg" "%modpath%\maps" "%modpath%\materials" "%modpath%\resource" "%modpath%\scripts" "%modpath%\portl.txt"
cd gamefiles\stanley
..\..\venv\Scripts\pyinstaller.exe  --clean .\install_stanley_heb_win_epic.spec
cd ..\..
move gamefiles\stanley\dist\install_stanley_heb_win_epic.exe gamefiles\stanley\dist\install_stanley_heb_win_epic_female.exe
venv\Scripts\python.exe -c "from src.stanley.install_unattended import epic_uninstall;epic_uninstall()"
venv\Scripts\python.exe -c "from src.stanley.install_unattended import epic_male;epic_male()"
start "" "D:\Program Files\7-Zip\7z.exe" a gamefiles\stanley\dist\install_stanley_heb_win_epic_male.zip "%modpath%\cfg" "%modpath%\maps" "%modpath%\materials" "%modpath%\resource" "%modpath%\scripts" "%modpath%\portl.txt"
cd gamefiles\stanley
..\..\venv\Scripts\pyinstaller.exe  --clean .\install_stanley_heb_win_epic.spec
cd ..\..
move gamefiles\stanley\dist\install_stanley_heb_win_epic.exe gamefiles\stanley\dist\install_stanley_heb_win_epic_male.exe
