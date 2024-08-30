set token=%1
set tag=%2
echo %token% | gh auth login --with-token
gh release create %tag% --title "Portal 2 Hebrew"
cd gamefiles\portal2\dist
for /r %%i in (portal-2-hebrew-installer.exe portal2-hebrew-glados-linux.zip portal2-hebrew-mabsuta-linux.zip) do gh release upload --clobber %tag% %%i
cd ..\..\..