#In order to create the patch, run:
#
# .\GenPat.exe 'C:\Program Files (x86)\Steam\steamapps\common\The Stanley Parable Demo\bin\vguimatsurface.dll' 'C:\Program Files (x86)\Steam\steamapps\common\The Stanley Parable\bin\vguimatsurface.dll' C:\projects\portalhebrew\gamefiles\stanleydemo\vguimatsurface.dll.patch
!include MUI2.nsh

!define BACKUPDIR "ORIG_ENGLISH"
!define UNINSTALLER_NAME "stanley-parable-demo-hebrew-uninstaller.exe"

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

Var GenderChoice
 	
Var SteamDir
Var Title
 
Function .onInit
 
   StrCpy $Title "התרגום העברי של סטנלי כמשל - ההדגמה"
 
FunctionEnd

Function un.onInit

   StrCpy $Title "התרגום העברי של סטנלי כמשל - ההדגמה"

FunctionEnd

Name $Title

OutFile "stanley-parable-demo-hebrew-installer.exe"

BrandingText "הרפתקה עברית"

Unicode true

!define MUI_TEXT_WELCOME_INFO_TEXT "ברוכים הבאים.$\r$\n \
$\r$\n \
לפני שנמשיך, יש לוודא כי:$\r$\n$\r$\n  \
• יש ברשותך עותק תקין של סטנלי כמשל - ההדגמה מסטים$\r$\n "

!define MUI_FINISHPAGE_TEXT  "ההתקנה הושלמה בהצלחה.$\r$\n$\r$\n \
נשמח לשמור על קשר! $\r$\n \
חפשו 'הרפתקה עברית' או 'פורטל בעברית' בפייסבוק.$\r$\n \
מוזמנים ומוזמנות להצטרף לדיונים, או סתם לראות איך דברים נראים מאחורי הקלעים, בערוץ הדיסקורד שלנו:"

!define MUI_TEXT_ABORT_SUBTITLE "ההתקנה לא הושלמה במלואה"

!define MUI_FINISHPAGE_LINK "הצטרפות לדיסקורד 'הרפתקה עברית'"
!define MUI_FINISHPAGE_LINK_LOCATION https://discord.gg/yvr2m2jYRG



!insertmacro MUI_PAGE_WELCOME
Page Custom MyPageCreate MyPageLeave
!define MUI_PAGE_HEADER_TEXT  "בחירת מיקום להתקנה"
!define MUI_PAGE_HEADER_SUBTEXT "יש לבחור את התיקייה שבה נדרש להתקין את $Title"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_WELCOME
!define MUI_PAGE_HEADER_TEXT  "הסרת $Title"
!define MUI_PAGE_HEADER_SUBTEXT "הסרת $Title מהמחשב"
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "Hebrew"

; The text to prompt the user to enter game's directory
DirText "יש לבחור את התיקייה שקבצי סטנלי כמשל - ההדגמה נמצאים בה"

!include "VPatchLib.nsh"


Function MyPageCreate
!insertmacro MUI_HEADER_TEXT "בחירת לשון פניה" "יש לבחור את לשון הפניה של התרגום"	
nsDialogs::Create 1018
Pop $0
${NSD_CreateFirstRadioButton} 0 0 40% 6% "אתה"
Pop $1
SendMessage $1 ${BM_CLICK} "" "" ; Must select a default
${NSD_CreateAdditionalRadioButton} 0 12% 40% 6% "את"
Pop $2
${IfThen} $GenderChoice == "female" ${|} SendMessage $2 ${BM_CLICK} "" "" ${|}
nsDialogs::Show
FunctionEnd
 
Function MyPageLeave
${NSD_GetChecked} $1 $3
${If} $3 <> ${BST_UNCHECKED}
	StrCpy $GenderChoice "male"
${Else}
	StrCpy $GenderChoice "female"
${EndIf}
ReadRegStr $SteamDir HKLM "SOFTWARE\WOW6432Node\Valve\Steam" "InstallPath"
ifFileExists "$SteamDir\steamapps\common\The Stanley Parable Demo\*.*" 0
    StrCpy $INSTDIR "$SteamDir\steamapps\common\The Stanley Parable Demo"
FunctionEnd

Section
DetailPrint "Turning the dial to $GenderChoice"
SectionEnd


Section "Update file"
   IfFileExists $INSTDIR\${UNINSTALLER_NAME} 0 +4
       MessageBox MB_OK "יש להסיר תחילה את ההתקנה הישנה"
       Exec $INSTDIR\${UNINSTALLER_NAME}
       MessageBox MB_OK "אישורך לסיום הסרת התקנה ישנה"

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
   IfFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\basemodui_scheme.res" +2
       CopyFiles "$INSTDIR\thestanleyparabledemo\resource\basemodui_scheme.res" "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\basemodui_scheme.res"
   IfFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\cfg\autoexec.cfg" +2
       CopyFiles "$INSTDIR\thestanleyparabledemo\cfg\autoexec.cfg" "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\cfg\autoexec.cfg"
   IfFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\subtitles_english.txt" +2
       CopyFiles "$INSTDIR\thestanleyparabledemo\resource\subtitles_english.txt" "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\subtitles_english.txt"
   IfFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\basemodui_english.txt" +2
       CopyFiles "$INSTDIR\thestanleyparabledemo\resource\basemodui_english.txt" "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\basemodui_english.txt"
   IfFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\gameui_english.txt" +2
       CopyFiles "$INSTDIR\thestanleyparabledemo\resource\gameui_english.txt" "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\gameui_english.txt"
   IfFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\ui\basemodui\mainmenu_tsp.res" +2
       CopyFiles "$INSTDIR\thestanleyparabledemo\resource\ui\basemodui\mainmenu_tsp.res" "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\ui\basemodui\mainmenu_tsp.res"
   IfFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\ui\tspvideo.res" +2
       CopyFiles "$INSTDIR\thestanleyparabledemo\resource\ui\tspvideo.res" "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\ui\tspvideo.res"
   IfFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\ui\basemodui\audio.res" +2
       CopyFiles "$INSTDIR\thestanleyparabledemo\resource\ui\basemodui\audio.res" "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\ui\basemodui\audio.res"
   IfFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\ui\basemodui\ingamemainmenu.res" +2
       CopyFiles "$INSTDIR\thestanleyparabledemo\resource\ui\basemodui\ingamemainmenu.res" "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\ui\basemodui\ingamemainmenu.res"
   IfFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\ui\basemodui\keyboardmouse.res" +2
       CopyFiles "$INSTDIR\thestanleyparabledemo\resource\ui\basemodui\keyboardmouse.res" "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\ui\basemodui\keyboardmouse.res"
   IfFileExists "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\ui\basemodui\options.res" +2
       CopyFiles "$INSTDIR\thestanleyparabledemo\resource\ui\basemoduioptions.res" "$INSTDIR\${BACKUPDIR}\thestanleyparabledemo\resource\ui\basemodui\options.res"

   ${If} $GenderChoice == "male"
	File /r male\thestanleyparabledemo
   ${Else}
	File /r female\thestanleyparabledemo
     ${EndIf}
   File /r generic\thestanleyparabledemo
SectionEnd

Section "Uninstall"
   CopyFiles "$INSTDIR\${BACKUPDIR}\*.*" $INSTDIR
   Rmdir /r "$INSTDIR\${BACKUPDIR}"
   Delete $INSTDIR\${UNINSTALLER_NAME}
   DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TSPD_Hebrew"
SectionEnd
