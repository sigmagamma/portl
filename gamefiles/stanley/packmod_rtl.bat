FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\The Stanley Parable\thestanleyparable_dlc1\
    )
ECHO %modpath%
..\..\venv\Scripts\pyinstaller.exe  --clean .\install_stanley_heb_win_rtl.spec