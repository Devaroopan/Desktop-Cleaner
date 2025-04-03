[Setup]
AppName=Desktop Cleaner
AppVersion=1.0
DefaultDirName={pf}\DesktopCleaner
DefaultGroupName=Desktop Cleaner
OutputDir=D:\DesktopCleaner\installer
OutputBaseFilename=Desktop_Cleaner_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "D:\Desktop_cleaner\dist\desktop_cleaner.exe"; DestDir: "{app}"

[Icons]
Name: "{commondesktop}\Desktop Cleaner"; Filename: "{app}\desktop_cleaner.exe"

[Run]
Filename: "{app}\desktop_cleaner.exe"; Description: "Launch Desktop Cleaner"; Flags: nowait postinstall
