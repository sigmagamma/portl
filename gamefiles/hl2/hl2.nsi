
!include MUI2.nsh
!include LogicLib.nsh

!define BACKUPDIR "ORIG_ENGLISH"
!define UNINSTALLER_NAME "hl2-arabic-uninstaller.exe"

;;;;; this nsis file isn't standard, and shouldn't (usually) be used as a simple template for other files!!!


!macro CopyFile FILE
   IfFileExists "$INSTDIR\${BACKUPDIR} \*.*" +2
       CreateDirectory "$INSTDIR\${BACKUPDIR}"

   IfFileExists "$INSTDIR\${BACKUPDIR}\${FILE}" +2
       CopyFiles "$INSTDIR\${FILE}" "$INSTDIR\${BACKUPDIR}\${FILE}"

   DetailPrint "Updating ${FILE}"


   IfErrors 0 +2
       abort
!macroend

Var Title
Var Subfolder
Var Index
Var Guid
Var Targetguid

Function .onInit
 
   StrCpy $Title "تعريب هالف-لايف 2"
   SetRebootFlag true
       StrCpy $Index "0"
    StrCpy $Subfolder ""
    StrCpy $Guid ""
    StrCpy $Targetguid "236c50c0-efc8-4d2b-9369-569e3a59bad3"

    loop_start:
        EnumRegKey $Subfolder HKCU "System\GameConfigStore\Children" $Index
        ${If} $Subfolder == ""
            MessageBox MB_OK "Target GUID not found"
            Goto done
        ${EndIf}

        ReadRegStr $Guid HKCU "System\GameConfigStore\Children\$Subfolder" "GameDVR_GameGUID"
        ${If} $Guid == $Targetguid
            ReadRegStr $INSTDIR HKCU "System\GameConfigStore\Children\$Subfolder" "MatchedExeFullPath"
            StrCpy $INSTDIR $INSTDIR -8
            Goto done
        ${EndIf}

        IntOp $Index $Index + 1
        Goto loop_start

    done:
FunctionEnd

Function un.onInit

   StrCpy $Title "برنامج إلغاء التثبيت تعريب هالف-لايف 2"

FunctionEnd

Name $Title

OutFile "hl2-arabic-installer.exe"

BrandingText "Something"

Unicode true
!define MUI_TEXT_WELCOME_INFO_TEXT "اهلاً بك.$\r$\n \
$\r$\n \
Before Proceeding:$\r$\n$\r$\n  \
•  يجب ان يكون لديك نسخة هالف-لايف 2 من ستيم.$\r$\n  \
• تأكد ان اللعبة محدثة بالفعل من خلال تشغيل اللعبة والخروج منها قبل تحميل التعريبة.$\r$\n "

!define MUI_FINISHPAGE_TEXT  "Installation successfully completed.$\r$\n$\r$\n \
Some text here $\r$\n"

!define MUI_TEXT_ABORT_SUBTITLE "Installation not completed"

!define MUI_FINISHPAGE_LINK "some link here'"
!define MUI_FINISHPAGE_LINK_LOCATION https://this.goes.somewhere



!insertmacro MUI_PAGE_WELCOME
!define MUI_PAGE_HEADER_TEXT  "إختر مجلد اللعبة لتحميل تعريب هالف-لايف 2"
!define MUI_PAGE_HEADER_SUBTEXT "إختر المجلد لتحميل تعريب هالف-لايف 2"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_WELCOME
;;;!define MUI_PAGE_HEADER_TEXT  "Remove $Title"
;;;!define MUI_PAGE_HEADER_SUBTEXT "Remove $Title from your computer"
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "Arabic"

; The text to prompt the user to enter game's directory
DirText "إختر المجلد التي يتكون فيه ملفات اللعبة"

Section "Update file"
   IfFileExists $INSTDIR\${UNINSTALLER_NAME} 0 +4
       MessageBox MB_OK "Please remove previous installation first"
       Exec $INSTDIR\${UNINSTALLER_NAME}
       MessageBox MB_OK "Confirm removal of previous installation"

   ; Set output path to the installation directory
   SetOutPath $INSTDIR

   WriteUninstaller $INSTDIR\${UNINSTALLER_NAME}

   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\hl2_arabic" \
                    "DisplayName" "Half Life 2 Arabic translation"
   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\hl2_arabic" \
                    "UninstallString" "$INSTDIR\${UNINSTALLER_NAME}"
   WriteRegStr HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" \
                    "Tahoma (TrueType)" ""
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" \
                    "Tahoma Bold (TrueType)" ""
   WriteRegStr HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes" \
                    "Tahoma" "Courier New"

   ifFileExists "$INSTDIR\${BACKUPDIR}\hl2\custom\portl" +2
       CreateDirectory "$INSTDIR\${BACKUPDIR}\hl2\custom\portl\"
       CopyFiles "$INSTDIR\hl2\custom\portl" "$INSTDIR\${BACKUPDIR}"
   ifFileExists "$INSTDIR\${BACKUPDIR}\hl2_complete\resource\clientscheme.res" +2
       CreateDirectory "$INSTDIR\${BACKUPDIR}\hl2_complete\resource\"
       CopyFiles "$INSTDIR\hl2_complete\resource\clientscheme.res" "$INSTDIR\${BACKUPDIR}\hl2_complete\resource\clientscheme.res"

   File /r hl2
   File /r hl2_complete
   File WINexe\arabic-readme.txt
SectionEnd

Section "Uninstall"
   CopyFiles "$INSTDIR\${BACKUPDIR}\*.*" $INSTDIR
   Rmdir /r "$INSTDIR\${BACKUPDIR}"
   Rmdir /r "$INSTDIR\hl2\custom\portl\"
   Delete $INSTDIR\arabic-readme.txt
   Delete $INSTDIR\${UNINSTALLER_NAME}
   DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\hl2_arabic"
   WriteRegStr HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" \
                    "Tahoma (TrueType)" "tahoma.ttf"
   WriteRegStr HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" \
                    "Tahoma Bold (TrueType)" "tahomabd.ttf"
   DeleteRegValue HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes\" "Tahoma"
SectionEnd
