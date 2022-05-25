; Script generated by the HM NIS Edit Script Wizard.
Unicode True
SetCompressor /SOLID lzma

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "PyPlane"
!define PRODUCT_VERSION "2.0.1"
!define PRODUCT_PUBLISHER "Institute of Control Theory"
!define PRODUCT_WEB_SITE "https://github.com/TUD-RST/pyplane.git"

; MUI 1.67 compatible ------
!include "MUI2.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "..\..\pyplane\resources\pyplane_icon_32px.ico"

; Welcome page
;!define WELCOME_TITLE 'PyPlane will install a folder on your desktop which contains the required files. A shortcut for launching the program will be put on the desktop, too. No modifications will be done in the registry!'
;!define MUI_WELCOMEPAGE_TITLE '${WELCOME_TITLE}'
;!define MUI_WELCOMEPAGE_TITLE_3LINES

!define MUI_TEXT_WELCOME_INFO_TEXT "PyPlane ${PRODUCT_VERSION} will be installed into a new folder on your desktop . A short-cut for launching the program will be put on the desktop, too. No modifications will be done in the registry!$\n$\n\
Setup will guide you through the installation of PyPlane.$\n$\n\
Please check $\n$\n${PRODUCT_WEB_SITE} $\n$\nfor updates regularly!"
!define MUI_PAGE_CUSTOMFUNCTION_SHOW MyWelcomeShowCallback
!insertmacro MUI_PAGE_WELCOME

; License page
!insertmacro MUI_PAGE_LICENSE "..\..\LICENSE"

; Directory page
!insertmacro MUI_PAGE_DIRECTORY

; Instfiles page
!insertmacro MUI_PAGE_INSTFILES

; Finish page
!insertmacro MUI_PAGE_FINISH

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Function MyWelcomeShowCallback
SendMessage $mui.WelcomePage.Text ${WM_SETTEXT} 0 "STR:$(MUI_TEXT_WELCOME_INFO_TEXT)"
FunctionEnd

RequestExecutionLevel user

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "build\PyPlane_${PRODUCT_VERSION}_Setup.exe"
InstallDir "$DESKTOP\PyPlane"
ShowInstDetails show

Section "Hauptgruppe" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  File /r "build\PyPlane\*"
  CreateShortCut "$DESKTOP\PyPlane.lnk" "$INSTDIR\PyPlane.exe"
SectionEnd