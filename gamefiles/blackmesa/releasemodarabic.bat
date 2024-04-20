set token=%1
set tag=%2
echo %token% | gh auth login --with-token
::gh release create %tag% --title "Black Mesa Arabic 04.2024" --notes "See [Installation guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2896432139)."
cd gamefiles\blackmesa\dist
for /r %%i in (install_black_mesa_a_win_ltr.exe install_black_mesa_a_win_ltr.zip install_black_mesa_a_win_rtl_ex.zip install_black_mesa_a_win_rtl.zip) do gh release upload --clobber %tag% %%i
cd ..\..\..