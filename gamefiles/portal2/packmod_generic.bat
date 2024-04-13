set gender=%1
set store=steam

del /s /q gamefiles\portal2\%gender%
mkdir gamefiles\portal2\%gender%
mkdir gamefiles\portal2\%gender%\portal2_dlc3
mkdir gamefiles\portal2\%gender%\portal2_dlc3\resource
mkdir -p tempzip\portal2_dlc3
venv\Scripts\python.exe -c "from src.portal2.install_unattended import %store%_%gender%;%store%_%gender%()"
for %%I in (cfg scripts resource media maps) do robocopy "%modpath%\%%I" tempzip\portal2_dlc3\%%I /e
copy "%modpath%\portl.txt" tempzip\portal2_dlc3\portl.txt
copy gamefiles\portal2\%store%zip\readme.txt tempzip
copy gamefiles\portal2\pak_01.dir tempzip\update
cd tempzip
start "" "c:\Program Files\7-Zip\7z.exe" a ..\gamefiles\portal2\dist\portal2-hebrew-%gender%.zip *
:: wait 5 seconds. Seriously.
ping 192.0.2.2 -n 1 -w 5000 > nul
cd ..
del /s /q tempzip
rmdir /s /q tempzip
move "%modpath%resource\subtitles_english.dat" gamefiles\portal2\%gender%\portal2_dlc3\resource
move "%modpath%resource\subtitles_english.txt" gamefiles\portal2\%gender%\portal2_dlc3\resource


