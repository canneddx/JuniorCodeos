::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAnk
::fBw5plQjdG8=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFBhVQgqHOG+iOYk47fvw++WXnkkUR+Ewaovnamc+/lHxWptUpyfGZq9myJ9CXUkWLEL5OjMgqH4PomvINMiSpx3uRgaM/k5Q
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
start "JuniorCodeos tap-to-control" /realtime "%~dp0winws.exe" ^
--wf-tcp=443 --wf-udp=443,50000-65535 ^
--filter-udp=443 --filter-tcp=443 ^
--hostlist="%~dp0domeins\russia-youtube.txt" ^
--dpi-desync=fake,split2 ^
--dpi-desync-udplen-increment=55 ^
--dpi-desync-udplen-pattern=0xCAFEBABE ^
--dpi-desync-repeats=20 ^
--dpi-desync-fake-quic="%~dp0bin\quic_initial_www_youtube_com.bin" ^
--dpi-desync-fake-tls="%~dp0bin\tls_clienthello_www_youtube_com.bin" ^
--dpi-desync-autottl=55 ^
--dpi-desync-fooling=md5sig ^
--new