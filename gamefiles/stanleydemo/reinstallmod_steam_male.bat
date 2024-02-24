::This should be run from the main project folder

FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\The Stanley Parable Demo\thestanleyparabledemo_dlc1\
    set origpath=%%A %%B\steamapps\common\The Stanley Parable Demo\thestanleyparabledemo\
    set backuppath=%%A %%B\steamapps\common\The Stanley Parable Demo\thestanleyparabledemo_backup\
    )
for %%I in (cfg materials resource scripts) do robocopy "%backuppath%\%%I" "%origpath%\%%I" /e
call gamefiles\stanleydemo\reinstall_generic.bat male
for %%I in (cfg materials resource scripts sound) do robocopy "%modpath%\%%I" "%origpath%\%%I" /e
copy "C:\Program Files (x86)\Steam\steamapps\common\The Stanley Parable\bin\vguimatsurface.dll" "C:\Program Files (x86)\Steam\steamapps\common\The Stanley Parable Demo\bin\vguimatsurface.dll"