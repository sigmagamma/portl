::This should be run from the main project folder
FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\The Stanley Parable\thestanleyparable_dlc1\
    )
gamefiles\stanley\packmod_generic.bat steam female
gamefiles\stanley\packmod_generic.bat steam male