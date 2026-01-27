set token=%1
set tag=%2
echo %token% | gh auth login --with-token
gh release create %tag% --title "Portal 2 Arabic"
cd gamefiles\portal2\dist_arabic
for /r %%i in (portal-2-arabic-installer.exe ) do gh release upload --clobber %tag% %%i
cd ..\..\..