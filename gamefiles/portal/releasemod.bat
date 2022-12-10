set token=%1
set tag=%2
echo %token% | gh auth login --with-token
gh release create %tag% --title "Portal and Portal RTX" --notes "See [Installation guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2554472476)."
cd gamefiles\portal\dist
for /r %%i in (install_portal_2007_heb_win_ltr.exe install_portal_2007_heb_win_ltr.zip install_portal_2007_heb_win_rtl.zip install_portal_2007_heb_win_rtl_ex.zip install_portal_rtx_heb_win_ltr.exe install_portal_rtx_heb_win_ltr.zip install_portal_rtx_heb_win_rtl.zip install_portal_rtx_heb_win_rtl_ex.zip ) do gh release upload --clobber %tag% %%i
cd ..\..\..