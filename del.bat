@echo off
openfiles >nul 2>nul
if '%errorlevel%' NEQ '0' (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo Script is running with administrator privileges.

sc stop windivert
