set token=%1
set tag=%2
echo %token% | gh auth login --with-token
gh release create %tag% --title "Portal and Portal RTX Resizer" --notes "See [Installation guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2924041906)."
cd gamefiles\portalresizer\dist
for /r %%i in (install_portal_2007_resizer.exe install_portal_2007_resizer.zip install_portal_rtx_resizer.exe install_portal_rtx_resizer.zip ) do gh release upload --clobber %tag% %%i
cd ..\..\..