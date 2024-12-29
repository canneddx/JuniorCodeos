@echo off
setlocal

cd /d "%~dp0"

REM Delete repo.zip if it exists
if exist repo.zip del /f /q repo.zip

REM Delete JuniorCodeos-main folder if it exists
if exist JuniorCodeos-main rmdir /s /q JuniorCodeos-main

pause
