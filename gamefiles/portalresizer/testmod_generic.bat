set edition=%1
echo press u
gamefiles\portalresizer\dist\install_portal_%edition%_resizer.exe
echo press y
gamefiles\portalresizer\dist\install_portal_%edition%_resizer.exe
echo "test that game is installed for %edition%"
pause
echo press u
gamefiles\portalresizer\dist\install_portal_%edition%_resizer.exe
echo "test that game is uninstalled for %edition% "
pause
start "" "C:\Program Files\7-Zip\7z.exe" x gamefiles\portalresizer\dist\install_portal_%edition%_resizer.zip -o"%modpath%\..\.." -y
echo "test that game is installed for %edition%"
pause
rmdir /s /q "%modpath%"
echo "test that game is uninstalled for %edition%"
pause