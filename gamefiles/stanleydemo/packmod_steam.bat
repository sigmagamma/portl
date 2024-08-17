::This should be run from the main project folder
del /s /q  gamefiles\stanleydemo\dist

mkdir gamefiles\stanleydemo\dist
del /s /q  gamefiles\stanleydemo\generic
mkdir gamefiles\stanleydemo\generic
del /s /q gamefiles\stanleydemo\bin
mkdir gamefiles\stanleydemo\bin

FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam" /v InstallPath`) DO (
    set modpath=%%A %%B\steamapps\common\The Stanley Parable Demo\thestanleyparabledemo_dlc1\
    set stanleybinpath=%%A %%B\steamapps\common\The Stanley Parable\bin
    set stanleydemobinpath=%%A %%B\steamapps\common\The Stanley Parable Demo\bin
    )
set nsisbinpath="C:\Program Files (x86)\NSIS\Bin"
%nsisbinpath%\GenPat.exe "%stanleydemobinpath%\vguimatsurface.dll" "%stanleybinpath%\vguimatsurface.dll" gamefiles\stanleydemo\bin\vguimatsurface.dll.patch
for %%I in (female male) do call gamefiles\stanleydemo\packmod_generic.bat %%I
for %%I in (cfg materials resource) do robocopy "%modpath%\%%I" gamefiles\stanleydemo\generic\thestanleyparabledemo\%%I /e
copy "%modpath%\portl.txt" gamefiles\stanleydemo\generic\thestanleyparabledemo\portl.txt

cd gamefiles\stanleydemo
%nsisbinpath%\makensis.exe stanleydemo.nsi
move stanley-parable-demo-hebrew-installer.exe dist
cd ..\..
