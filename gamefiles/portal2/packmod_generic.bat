set robot=%1
set store=steam

del /s /q gamefiles\portal2\%robot%
mkdir gamefiles\portal2\%robot%
mkdir gamefiles\portal2\%robot%\portal2_dlc3
mkdir gamefiles\portal2\%robot%\portal2_dlc3\resource
mkdir gamefiles\portal2\%robot%\update
mkdir gamefiles\portal2\%robot%\update\resource
for %%J in (linux WIN) do (
    mkdir -p tempzip\portal2_dlc3
    mkdir -p tempzip\update
    mkdir -p tempzip\update\resource
    venv\Scripts\python.exe -c "from src.portal2.install_unattended import %store%_%robot%_%%J;%store%_%robot%_%%J()"
    for %%I in (cfg scripts resource media maps) do robocopy "%modpath%\%%I" tempzip\portal2_dlc3\%%I /e
    if "%%J" == "linux" (
      copy gamefiles\portal2\linux\media\sp_credits_bg.bik tempzip\portal2_dlc3\media\sp_credits_bg.bik
    )
    copy "%modpath%\portl.txt" tempzip\portal2_dlc3\portl.txt
    copy "%modpath%\pak01_dir.vpk" tempzip\portal2_dlc3\pak01_dir.vpk
    copy "%modpath%..\update\resource\basemodui_tu_english.txt" tempzip\update\resource\basemodui_tu_english.txt
    copy "%modpath%..\update\pak01_dir.vpk" tempzip\update\pak01_dir.vpk
    copy gamefiles\portal2\%%Jzip\hebrew-readme.txt tempzip
    if "%%J" == "WIN" (
      mkdir -p tempzip\bin
      copy gamefiles\portal2\bin\vguimatsurface.dll.patch tempzip\bin\vguimatsurface.dll.patch
    )
    cd tempzip
    start "" "c:\Program Files\7-Zip\7z.exe" a ..\gamefiles\portal2\dist\portal2-hebrew-%robot%-%%J.zip *
    :: wait 5 seconds. Seriously.
    ping 192.0.2.2 -n 1 -w 10000 > nul
    cd ..
    del /s /q tempzip
    rmdir /s /q tempzip
)

move "%modpath%resource\subtitles_english.dat" gamefiles\portal2\%robot%\portal2_dlc3\resource
move "%modpath%resource\subtitles_english.txt" gamefiles\portal2\%robot%\portal2_dlc3\resource
move "%modpath%resource\portal2_english.txt" gamefiles\portal2\%robot%\portal2_dlc3\resource
move "%modpath%resource\closecaption_english.dat" gamefiles\portal2\%robot%\portal2_dlc3\resource
move "%modpath%resource\closecaption_english.txt" gamefiles\portal2\%robot%\portal2_dlc3\resource
move "%modpath%\..\update\resource\basemodui_tu_english.txt" gamefiles\portal2\%robot%\update\resource
move "%modpath%pak01_dir.vpk" gamefiles\portal2\%robot%\portal2_dlc3


