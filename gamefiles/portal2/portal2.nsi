#In order to create the patch, run:
#
# .\GenPat.exe  "C:\projects\portalhebrew\gamefiles\portal2\vguimatsurface_orig.dll" "C:\projects\portalhebrew\gamefiles\portal2\vguimatsurface.dll"  C:\projects\portalhebrew\gamefiles\portal2\bin\vguimatsurface.dll.patch
# .\GenPat.exe  "C:\projects\portalhebrew\gamefiles\portal2\pak01_dir_orig.vpk" "C:\Program Files (x86)\Steam\steamapps\common\Portal 2\update\pak01_dir.vpk"  C:\projects\portalhebrew\gamefiles\portal2\update_patch\pak01_dir.vpk.patch
!include MUI2.nsh

!define BACKUPDIR "ORIG_ENGLISH"
!define UNINSTALLER_NAME "portal2-hebrew-uninstaller.exe"

;;;;; this nsis file isn't standard, and shouldn't (usually) be used as a simple template for other files!!!

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
 
   StrCpy $Title "התרגום העברי של פורטל 2"
 
FunctionEnd

Function un.onInit

   StrCpy $Title "התרגום העברי של פורטל 2 - הסרה"

FunctionEnd

Name $Title

OutFile "portal-2-hebrew-installer.exe"

BrandingText "הרפתקה עברית"

Unicode true

!define MUI_TEXT_WELCOME_INFO_TEXT "ברוכים הבאים.$\r$\n \
$\r$\n \
לפני שנמשיך:$\r$\n$\r$\n  \
• יש לוודא כי יש ברשותך עותק תקין של פורטל 2 מסטים$\r$\n  \
• יש לוודא כי העותק מעודכן על ידי הרצה של המשחק ויציאה טרם המשך ההתקנה$\r$\n "

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
DirText "יש לבחור את התיקייה שקבצי פורטל 2 נמצאים בה"

!include "VPatchLib.nsh"


Function MyPageCreate
!insertmacro MUI_HEADER_TEXT "התאמה אישית" "בחרו שם מועדף לבינה מלאכותית סרקסטית"
nsDialogs::Create 1018
Pop $0
${NSD_CreateFirstRadioButton} 0 0 40% 6% "גלאדוס"
Pop $1
SendMessage $1 ${BM_CLICK} "" "" ; Must select a default
${NSD_CreateAdditionalRadioButton} 0 12% 40% 6% "מבסוט״ה"
Pop $2
${IfThen} $GenderChoice == "mabsuta" ${|} SendMessage $2 ${BM_CLICK} "" "" ${|}
nsDialogs::Show
FunctionEnd
 
Function MyPageLeave
${NSD_GetChecked} $1 $3
${If} $3 <> ${BST_UNCHECKED}
	StrCpy $GenderChoice "glados"
${Else}
	StrCpy $GenderChoice "mabsuta"
${EndIf}
ReadRegStr $SteamDir HKLM "SOFTWARE\WOW6432Node\Valve\Steam" "InstallPath"
ifFileExists "$SteamDir\steamapps\common\Portal 2\*.*" 0
    StrCpy $INSTDIR "$SteamDir\steamapps\common\Portal 2"
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

   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Portal2_Hebrew" \
                    "DisplayName" "Portal 2 Hebrew translation"
   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Portal2_Hebrew" \
                    "UninstallString" "$INSTDIR\${UNINSTALLER_NAME}"


   !insertmacro BackupAndUpdateFile bin\vguimatsurface.dll
   !insertmacro BackupAndUpdateFile update\pak01_dir.vpk
   ifFileExists "$INSTDIR\${BACKUPDIR}\portal2_dlc3\" +2
       CreateDirectory "$INSTDIR\${BACKUPDIR}\portal2_dlc3\"
       CopyFiles "$INSTDIR\portal2_dlc3" "$INSTDIR\${BACKUPDIR}"
   ifFileExists "$INSTDIR\${BACKUPDIR}\update\pak01_dir.vpk" +2
       CreateDirectory "$INSTDIR\${BACKUPDIR}\update\"
       CopyFiles "$INSTDIR\update\pak01_dir.vpk" "$INSTDIR\${BACKUPDIR}\update\pak01_dir.vpk"
   ifFileExists "$INSTDIR\${BACKUPDIR}\update\resource\basemodui_tu_english.txt" +2
       CreateDirectory "$INSTDIR\${BACKUPDIR}\update\resource\"
       CopyFiles "$INSTDIR\update\resource\basemodui_tu_english.txt" "$INSTDIR\${BACKUPDIR}\update\resource\basemodui_tu_english.txt"
   ${If} $GenderChoice == "glados"
	File /r glados\portal2_dlc3
	File /r glados\update
   ${Else}
	File /r mabsuta\portal2_dlc3
	File /r mabsuta\update
     ${EndIf}
   File /r generic\portal2_dlc3
   File /r generic\update
   File WINexe\hebrew-readme.txt
SectionEnd

Section "Uninstall"
   CopyFiles "$INSTDIR\${BACKUPDIR}\*.*" $INSTDIR
   Rmdir /r "$INSTDIR\${BACKUPDIR}"
   Rmdir /r "$INSTDIR\portal2_dlc3"
   Delete $INSTDIR\hebrew-readme.txt
   Delete $INSTDIR\${UNINSTALLER_NAME}
   DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Portal2_Hebrew"
SectionEnd
