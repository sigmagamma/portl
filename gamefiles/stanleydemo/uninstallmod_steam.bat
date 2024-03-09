::This should be run from the main project folder
set store=steam
FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\The Stanley Parable Demo\thestanleyparabledemo_dlc1\
    set origpath=%%A %%B\steamapps\common\The Stanley Parable Demo\thestanleyparabledemo\
    set backuppath=%%A %%B\steamapps\common\The Stanley Parable Demo\thestanleyparabledemo_backup\
    )
for %%I in (cfg materials resource scripts scenes sound) do robocopy "%backuppath%\%%I" "%origpath%\%%I" /e
venv\Scripts\python.exe -c "from src.stanleydemo.install_unattended import %store%_uninstall;%store%_uninstall()"