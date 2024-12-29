@echo off
openfiles >nul 2>nul
if '%errorlevel%' NEQ '0' (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

@echo off
set "REPO_URL=https://github.com/canneddx/JuniorCodeos/archive/refs/heads/main.zip"
set "TEMP_DIR=%TEMP%\repo_download"
set "TARGET_DIR=%~dp0"
set "EXECUTABLE=JuniorCodeos.exe"

taskkill /f /im "%EXECUTABLE%" >nul 2>&1

if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

echo Downloading files from GitHub...
curl -L "%REPO_URL%" -o "%TEMP_DIR%\repo.zip" || (
    echo Error downloading files.
    exit /b 1
)

echo Extracting files...
powershell -Command "Expand-Archive -Path '%TEMP_DIR%\repo.zip' -DestinationPath '%TEMP_DIR%' -Force" || (
    echo Extraction error.
    exit /b 1
)

echo Updating files...
for /d %%d in ("%TEMP_DIR%\JuniorCodeos-main\*") do move "%%d" "%TARGET_DIR%" >nul
for %%f in ("%TEMP_DIR%\JuniorCodeos-main\*") do move "%%f" "%TARGET_DIR%" >nul

rd /s /q "%TEMP_DIR%\JuniorCodeos-main" >nul
del /f /q "%TEMP_DIR%\repo.zip" >nul

rd /s /q "%TEMP_DIR%" >nul

echo Restarting the program...
start "" "%TARGET_DIR%\%EXECUTABLE%"
