set align=%1
set edition=%2
echo press u
gamefiles\portal\dist\install_portal_%edition%_heb_win_%align%.exe
echo press y
gamefiles\portal\dist\install_portal_%edition%_heb_win_%align%.exe
echo "test that game is installed for %edition% %align%"
pause
echo press u
gamefiles\portal\dist\install_portal_%edition%_heb_win_%align%.exe
echo "test that game is uninstalled for %edition% %align%"
pause
start "" "C:\Program Files\7-Zip\7z.exe" x gamefiles\portal\dist\install_portal_%edition%_heb_win_%align%.zip -o"%modpath%\..\.." -y
echo "test that game is installed for %edition% %align%"
pause
rmdir /s /q "%modpath%"
echo "test that game is uninstalled for %edition% %align%"
pause