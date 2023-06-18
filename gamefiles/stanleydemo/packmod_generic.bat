set gender=%1
set store=steam

del /s /q  gamefiles\stanleydemo\%gender%
mkdir gamefiles\stanleydemo\%gender%
mkdir gamefiles\stanleydemo\%gender%\thestanleyparabledemo
mkdir gamefiles\stanleydemo\%gender%\thestanleyparabledemo\resource
::mkdir -p tempzip\thestanleyparabledemo
venv\Scripts\python.exe -c "from src.stanleydemo.install_unattended import %store%_uninstall;%store%_uninstall()"
venv\Scripts\python.exe -c "from src.stanleydemo.install_unattended import %store%_%gender%;%store%_%gender%()"
::for %%I in (cfg maps materials resource) do robocopy "%modpath%\%%I" tempzip\thestanleyparabledemo\%%I /e
::copy "%modpath%\portl.txt" tempzip\thestanleyparabledemo\portl.txt
::copy gamefiles\stanleydemo\%store%zip\readme.txt tempzip
::copy gamefiles\stanleydemo\bin\vguimatsurface.dll.patch tempzip
::cd tempzip
::start "" "D:\Program Files\7-Zip\7z.exe" a ..\gamefiles\stanleydemo\dist\stanley-parable-demo-hebrew-%gender%.zip *
move "%modpath%resource\subtitles_english.dat" gamefiles\stanleydemo\%gender%\thestanleyparabledemo\resource
move "%modpath%resource\basemodui_english.txt" gamefiles\stanleydemo\%gender%\thestanleyparabledemo\resource
:: wait 5 seconds. Seriously.
::ping 192.0.2.2 -n 1 -w 5000 > nul
::cd ..
::del /s /q tempzip
::rmdir /s /q tempzip
