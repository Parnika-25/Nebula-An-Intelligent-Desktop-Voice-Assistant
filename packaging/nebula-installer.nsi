; =====================================================
; Nebula AI Assistant - NSIS Installer
; =====================================================

!include "MUI2.nsh"

; =====================================================
; BASIC INFO
; =====================================================

Name "Nebula AI Assistant"
OutFile "Nebula.exe"
InstallDir "$PROGRAMFILES64\Nebula"
InstallDirRegKey HKLM "Software\Nebula" "InstallDir"
RequestExecutionLevel admin

; =====================================================
; ICON
; =====================================================

Icon "..\apps\backend\nebula.ico"
!define MUI_ICON "..\apps\backend\nebula.ico"
!define MUI_UNICON "..\apps\backend\nebula.ico"

; =====================================================
; UI SETTINGS
; =====================================================

!define MUI_ABORTWARNING
!define MUI_WELCOMEPAGE_TITLE "Welcome to Nebula AI Assistant"
!define MUI_WELCOMEPAGE_TEXT "Nebula is your intelligent AI voice assistant for Windows.$\n$\nThis will install Nebula on your computer.$\n$\nClick Next to continue."
!define MUI_FINISHPAGE_RUN "$INSTDIR\Nebula.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Launch Nebula now"
!define MUI_FINISHPAGE_TITLE "Nebula Installed!"
!define MUI_FINISHPAGE_TEXT "Nebula has been installed successfully.$\n$\nIt will start automatically every time Windows starts.$\n$\nClick Finish to complete."

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; =====================================================
; INSTALL SECTION
; =====================================================

Section "Install Nebula" SecMain

    SetOutPath "$INSTDIR"

    ; Copy ALL files from the Nebula folder
    File /r "..\apps\backend\dist\Nebula\*.*"

    ; ---- AUTO START FOR ALL USERS ----
    WriteRegStr HKLM \
        "Software\Microsoft\Windows\CurrentVersion\Run" \
        "Nebula" "$INSTDIR\Nebula.exe"

    ; ---- DESKTOP SHORTCUT ----
    CreateShortCut "$DESKTOP\Nebula.lnk" \
        "$INSTDIR\Nebula.exe" "" \
        "$INSTDIR\Nebula.exe" 0

    ; ---- START MENU ----
    CreateDirectory "$SMPROGRAMS\Nebula"
    CreateShortCut "$SMPROGRAMS\Nebula\Nebula AI.lnk" "$INSTDIR\Nebula.exe"
    CreateShortCut "$SMPROGRAMS\Nebula\Uninstall.lnk" "$INSTDIR\Uninstall.exe"

    ; ---- REGISTRY ----
    WriteRegStr HKLM "Software\Nebula" "InstallDir" "$INSTDIR"
    WriteRegStr HKLM "Software\Nebula" "Version" "1.1.0"

    ; ---- UNINSTALLER ----
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ; ---- ADD/REMOVE PROGRAMS ----
    WriteRegStr HKLM \
        "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nebula" \
        "DisplayName" "Nebula AI Assistant"
    WriteRegStr HKLM \
        "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nebula" \
        "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM \
        "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nebula" \
        "DisplayVersion" "1.1.0"
    WriteRegStr HKLM \
        "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nebula" \
        "Publisher" "Praveen-1810"
    WriteRegStr HKLM \
        "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nebula" \
        "DisplayIcon" "$INSTDIR\Nebula.exe"

SectionEnd

; =====================================================
; UNINSTALL SECTION
; =====================================================

Section "Uninstall"

    ; Stop Nebula if running
    ExecWait 'taskkill /F /IM Nebula.exe'

    ; Remove all installed files
    RMDir /r "$INSTDIR"

    ; Remove shortcuts
    Delete "$DESKTOP\Nebula.lnk"
    Delete "$SMPROGRAMS\Nebula\Nebula AI.lnk"
    Delete "$SMPROGRAMS\Nebula\Uninstall.lnk"
    RMDir "$SMPROGRAMS\Nebula"

    ; Remove auto-start
    DeleteRegValue HKLM \
        "Software\Microsoft\Windows\CurrentVersion\Run" "Nebula"

    ; Remove registry
    DeleteRegKey HKLM "Software\Nebula"
    DeleteRegKey HKLM \
        "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nebula"

SectionEnd
