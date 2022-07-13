FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\Black Mesa\bms\custom\portl\
    )
ECHO %modpath%
..\..\venv\Scripts\pyinstaller.exe  --clean .\install_black_mesa_heb_win_testers.spec