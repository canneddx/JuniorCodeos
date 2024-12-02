@echo off
:: Устанавливаем переменные
set "REPO_URL=https://github.com/canneddx/JuniorCodeos/archive/refs/heads/main.zip"
set "TEMP_DIR=%TEMP%\repo_download"
set "TARGET_DIR=%~dp0"
set "EXECUTABLE=JuniorCodeos.exe"

:: Завершаем выполнение файла JuniorCodeos.exe, если он запущен
taskkill /f /im "%EXECUTABLE%" >nul 2>&1

:: Создаем временную папку для загрузки
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

:: Загружаем ZIP-архив репозитория
GitHub...
curl -L "%REPO_URL%" -o "%TEMP_DIR%\repo.zip" || (
    echo Ошибка загрузки файлов. Убедитесь, что у вас есть доступ к интернету.
    exit /b 1
)

:: Распаковываем ZIP-архив
echo Распаковка файлов...
powershell -Command "Expand-Archive -Path '%TEMP_DIR%\repo.zip' -DestinationPath '%TEMP_DIR%' -Force" || (
    echo Ошибка распаковки. Убедитесь, что PowerShell установлен.
    exit /b 1
)

:: Перемещаем новые файлы в целевую папку
echo Обновление файлов...
for /d %%d in ("%TEMP_DIR%\JuniorCodeos-main\*") do move "%%d" "%TARGET_DIR%" >nul
for %%f in ("%TEMP_DIR%\JuniorCodeos-main\*") do move "%%f" "%TARGET_DIR%" >nul

:: Удаляем временные файлы
rd /s /q "%TEMP_DIR%"

:: Перезапуск JuniorCodeos.exe
echo Перезапуск программы...
start "" "%TARGET_DIR%\%EXECUTABLE%"

