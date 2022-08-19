set store=%1
set gender=%2
reg import gamefiles\stanley\utils\%store%.reg
echo u | gamefiles\stanley\dist\install_stanley_heb_win_%store%_%gender%.exe
del /s /q %modpath%
echo y | gamefiles\stanley\dist\install_stanley_heb_win_%store%_%gender%.exe
echo "test that game is installed for %store% %gender%"
pause
echo u | gamefiles\stanley\dist\install_stanley_heb_win_%store%_%gender%.exe
echo "test that game is uninstalled for %store% %gender%"
pause
del /s /q %modpath%
start "" "D:\Program Files\7-Zip\7z.exe" x gamefiles\stanley\dist\install_stanley_heb_win_%store%_%gender%.zip -o"%modpath%"
echo "test that game is installed for %store% %gender%"
pause
del /s /q %modpath%
echo "test that game is uninstalled for %store% %gender%"
pause