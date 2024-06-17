set gender=%1
set store=steam

del /s /q gamefiles\portal2\%gender%
mkdir gamefiles\portal2\%gender%
mkdir gamefiles\portal2\%gender%\portal2_dlc3
mkdir gamefiles\portal2\%gender%\portal2_dlc3\resource
mkdir -p tempzip\portal2_dlc3
mkdir -p tempzip\update
venv\Scripts\python.exe -c "from src.portal2.install_unattended import %store%_%gender%;%store%_%gender%()"
for %%I in (cfg scripts resource media maps) do robocopy "%modpath%\%%I" tempzip\portal2_dlc3\%%I /e
copy "%modpath%\portl.txt" tempzip\portal2_dlc3\portl.txt
copy "%modpath%\pak01_dir.vpk" tempzip\portal2_dlc3\pak01_dir.vpk
copy gamefiles\portal2\%store%zip\readme.txt tempzip
copy "%modpath%..\update\pak01_dir.vpk" tempzip\update\pak01_dir.vpk
cd tempzip
start "" "c:\Program Files\7-Zip\7z.exe" a ..\gamefiles\portal2\dist\portal2-hebrew-%gender%.zip *
:: wait 5 seconds. Seriously.
ping 192.0.2.2 -n 1 -w 10000 > nul
cd ..
del /s /q tempzip
rmdir /s /q tempzip
move "%modpath%resource\subtitles_english.dat" gamefiles\portal2\%gender%\portal2_dlc3\resource
move "%modpath%resource\subtitles_english.txt" gamefiles\portal2\%gender%\portal2_dlc3\resource


