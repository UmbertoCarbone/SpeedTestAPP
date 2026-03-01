; Script Inno Setup per SpeedApp
; Compila con Inno Setup Compiler: https://jrsoftware.org/isdl.php

[Setup]
AppName=SpeedTest App
AppVersion=1.0.1
AppPublisher=UmbertoCarbone
DefaultDirName={autopf}\SpeedApp
DefaultGroupName=SpeedTest App
OutputDir=installer_output
OutputBaseFilename=SpeedApp_Setup_1.0.1
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\SpeedApp.exe
SetupIconFile=icon.ico

[Languages]
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Crea un'icona sul desktop"; GroupDescription: "Icone aggiuntive:"

[Files]
Source: "dist\SpeedApp.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\SpeedTest App"; Filename: "{app}\SpeedApp.exe"
Name: "{group}\Disinstalla SpeedTest App"; Filename: "{uninstallexe}"
Name: "{autodesktop}\SpeedTest App"; Filename: "{app}\SpeedApp.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\SpeedApp.exe"; Description: "Avvia SpeedTest App"; Flags: postinstall nowait skipifsilent
