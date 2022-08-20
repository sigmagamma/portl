set store=%1
set gender=%2
reg import gamefiles\stanley\utils\%store%.reg
echo press u
gamefiles\stanley\dist\install_stanley_heb_win_%store%_%gender%.exe
rmdir /s /q "%modpath%"
echo press y
gamefiles\stanley\dist\install_stanley_heb_win_%store%_%gender%.exe
IF %store%==epic (
if not exist "%modpath%\SAVE\0" mkdir "%modpath%\SAVE\0"
copy gamefiles\stanley\test\notstanley.sav "%modpath%\SAVE\0\notstanley.sav"
)
echo "test that game is installed for %store% %gender%"
pause
echo press u
gamefiles\stanley\dist\install_stanley_heb_win_%store%_%gender%.exe
echo "test that game is uninstalled for %store% %gender%"
pause
rmdir /s /q "%modpath%"
IF %store%==epic (
copy "%modpath%\..\thestanleyparable\gameinfo.txt" "%modpath%\..\thestanleyparable\gameinfo_backup.txt"
)
start "" "D:\Program Files\7-Zip\7z.exe" x gamefiles\stanley\dist\install_stanley_heb_win_%store%_%gender%.zip -o"%modpath%\.." -y
IF %store%==epic (
if not exist "%modpath%\SAVE\0" mkdir "%modpath%\SAVE\0"
copy gamefiles\stanley\test\notstanley.sav "%modpath%\SAVE\0\notstanley.sav"
)
echo "test that game is installed for %store% %gender%"
pause
rmdir /s /q "%modpath%"
IF %store%==epic (
copy "%modpath%\..\thestanleyparable\gameinfo_backup.txt" "%modpath%\..\thestanleyparable\gameinfo.txt"
del "%modpath%\..\thestanleyparable\gameinfo_backup.txt"
)
echo "test that game is uninstalled for %store% %gender%"
pause