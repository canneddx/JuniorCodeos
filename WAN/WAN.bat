@echo off
openfiles >nul 2>nul
if '%errorlevel%' NEQ '0' (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

ipconfig /flushdns

netsh int tcp set global autotuninglevel=normal
netsh int tcp set global rss=enabled
netsh int tcp set global chimney=enabled
netsh int tcp set global dca=enabled
netsh int tcp set global ecncapability=enabled
netsh int tcp set global congestionprovider=ctcp

netsh interface ipv4 set subinterface "Ethernet" mtu=1500 store=persistent

netsh interface tcp set heuristics disabled
netsh int tcp set supplemental encryptedconnections=enabled

powercfg -change -standby-timeout-ac 0
powercfg -change -monitor-timeout-ac 0

netsh int tcp set global maxsynretransmissions=2
