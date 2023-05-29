#In order to create the patches, run:
#
# "C:\Program Files (x86)\NSIS\Bin\GenPat.exe" "C:\Zvika\Games\Broken Sword - Shadow of the Templars - GOG.clean\clusters\general.clu" "C:\Zvika\Games\Broken Sword - The Shadow of the Templars\clusters\general.clu" general.clu.patch /r
# "C:\Program Files (x86)\NSIS\Bin\GenPat.exe" "C:\Zvika\Games\Broken Sword - Shadow of the Templars - GOG.clean\clusters\swordres.rif" "C:\Zvika\Games\Broken Sword - The Shadow of the Templars\clusters\swordres.rif" swordres.rif.patch /r
# "C:\Program Files (x86)\NSIS\Bin\GenPat.exe" "C:\Zvika\Games\Broken Sword - Shadow of the Templars - GOG.clean\clusters\text.clu" "C:\Zvika\Games\Broken Sword - The Shadow of the Templars\clusters\text.clu" text.clu.patch /r
# .\GenPat.exe 'C:\Program Files (x86)\Steam\steamapps\common\The Stanley Parable Demo\bin\vguimatsurface.dll' 'C:\Program Files (x86)\Steam\steamapps\common\The Stanley Parable\bin\vguimatsurface.dll' C:\projects\portalhebrew\gamefiles\stanleydemo\vguimatsurface.patch
!include MUI2.nsh

!define BACKUPDIR "ORIG_ENGLISH"
!define UNINSTALLER_NAME "tspd_heb_uninstaller.exe"

;;;;; this nsis file isn't standard, and shouldn't (usually) be used as a simple template for other files!!!

; note the unique 'clusters' for Broken Sword all over this file!!
!macro BackupAndUpdateFile FILE
   IfFileExists "$INSTDIR\${BACKUPDIR} \*.*" +2
       CreateDirectory "$INSTDIR\${BACKUPDIR}"

   IfFileExists "$INSTDIR\${BACKUPDIR}\${FILE}" +2
       CopyFiles "$INSTDIR\${FILE}" "$INSTDIR\${BACKUPDIR}\${FILE}"

   DetailPrint "Updating ${FILE} using patch..."
   !insertmacro VPatchFile ${FILE}.patch "$INSTDIR\${FILE}" "$INSTDIR\${FILE}.tmp"

   IfErrors 0 +2
       abort
!macroend



!macro CopyFile FILE
   IfFileExists "$INSTDIR\${BACKUPDIR} \*.*" +2
       CreateDirectory "$INSTDIR\${BACKUPDIR}"

   IfFileExists "$INSTDIR\${BACKUPDIR}\${FILE}" +2
       CopyFiles "$INSTDIR\${FILE}" "$INSTDIR\${BACKUPDIR}\${FILE}"

   DetailPrint "Updating ${FILE}"


   IfErrors 0 +2
       abort
!macroend


Name "התרגום העברי של סטנלי כמשל - ההדגמה"

OutFile "tspd-hebrew-installer.exe"

BrandingText "הרפתקה עברית"

Unicode true

!define MUI_TEXT_WELCOME_INFO_TEXT "ברוכים הבאים.$\r$\n \
$\r$\n \
לפני שנמשיך, יש לוודא כי:$\r$\n$\r$\n  \
• יש ברשותך עותק תקין של סטנלי כמשל - ההדגמה מסטים$\r$\n "

!define MUI_FINISHPAGE_TEXT  "ההתקנה הושלמה בהצלחה.$\r$\n$\r$\n \
נשמח לשמור על קשר! $\r$\n \
חפשו 'הרפתקה עברית' או 'פורטל בעברית' בפייסבוק.$\r$\n \
מוזמנים להצטרף לדיונים, או סתם לראות איך דברים נראים מאחורי הקלעים, בערוץ הדיסקורד שלנו:"

!define MUI_TEXT_ABORT_SUBTITLE "ההתקנה לא הושלמה במלואה"

!define MUI_FINISHPAGE_LINK "הצטרפות לדיסקורד 'הרפתקה עברית'"
!define MUI_FINISHPAGE_LINK_LOCATION https://discord.gg/yvr2m2jYRG

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "Hebrew"

; The text to prompt the user to enter game's directory
DirText "בחר את התיקייה שקבצי סטנלי כמשל - ההדגמה נמצאים בה"

!include "VPatchLib.nsh"

Section "Update file"
   IfFileExists $INSTDIR\${UNINSTALLER_NAME} 0 +4
       MessageBox MB_OK "יש להסיר תחילה את ההתקנה הישנה"
       Exec $INSTDIR\${UNINSTALLER_NAME}
       MessageBox MB_OK "אשר סיום הסרת התקנה ישנה"

   ; Set output path to the installation directory
   SetOutPath $INSTDIR

   WriteUninstaller $INSTDIR\${UNINSTALLER_NAME}

   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TSPD_Hebrew" \
                    "DisplayName" "The Stanley Parable Demo Hebrew translation"
   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TSPD_Hebrew" \
                    "UninstallString" "$INSTDIR\${UNINSTALLER_NAME}"


   !insertmacro BackupAndUpdateFile bin\vguimatsurface.dll
   ifFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource" +2
       CreateDirectory "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource"
   IfFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\subtitles_english.dat" +2
       CopyFiles "$INSTDIR\thestanleyparabledemo\resource\subtitles_english.dat" "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\subtitles_english.dat"
   IfFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\subtitles_english.dat" +2
       CopyFiles "$INSTDIR\thestanleyparabledemo\resource\subtitles_english.dat" "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\subtitles_english.dat"
   File /r thestanleyparabledemo
SectionEnd

Section "Uninstall"
   CopyFiles "$INSTDIR\${BACKUPDIR}\*.*" $INSTDIR
   Rmdir /r "$INSTDIR\${BACKUPDIR}"
   Delete $INSTDIR\${UNINSTALLER_NAME}
   DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TSPD_Hebrew"
SectionEnd
