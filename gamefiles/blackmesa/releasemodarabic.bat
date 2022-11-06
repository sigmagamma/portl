set token=%1
set tag=%2
echo %token% | gh auth login --with-token
::gh release create %tag% --title "Black Mesa Arabic" --notes "See [Installation guide](https://docs.google.com/document/d/1lsCQosS-TDPFxHi6mnZCE653AfrbqW5MhDCbnV-U_Ds/edit?usp=sharing)."
cd gamefiles\blackmesa\dist
for /r %%i in (install_black_mesa_a_win_ltr.exe install_black_mesa_a_win_ltr.zip) do gh release upload --clobber %tag% %%i
cd ..\..\..