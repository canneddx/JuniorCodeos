@ECHO OFF
PUSHD "%~dp0.."

set _arch=x86
IF "%PROCESSOR_ARCHITECTURE%"=="AMD64" (set _arch=x86_64)
IF DEFINED PROCESSOR_ARCHITEW6432 (set _arch=x86_64)

start /realtime "JuniorCodeos: discord-youtube" "%~dp0..\winws.exe" ^
--wf-tcp=80,443,50000-65535 --wf-udp=443,50000-65535 ^
--filter-udp=443 --hostlist="%~dp0..\domeins\general.txt" --dpi-desync=fake ^
--dpi-desync-udplen-increment=10 --dpi-desync-repeats=3 --dpi-desync-udplen-pattern=0xDEADBEEF ^
--dpi-desync-fake-quic="%~dp0..\bin\quic_initial_www_google_com.bin" --new ^
--filter-udp=50000-65535 --dpi-desync=fake,tamper --dpi-desync-any-protocol ^
--dpi-desync-fake-quic="%~dp0..\bin\quic_initial_www_google_com.bin" --new ^
--filter-tcp=80 --dpi-desync=fake,split2 --dpi-desync-autottl=3 --dpi-desync-fooling=md5sig --new ^
--filter-tcp=443 --hostlist="%~dp0..\domeins\general.txt" --dpi-desync=fake,split2 ^
--dpi-desync-autottl=1 --dpi-desync-fooling=md5sig --dpi-desync-repeats=3 ^
--dpi-desync-fake-tls="%~dp0..\bin\tls_clienthello_www_youtube_com.bin" --new ^
--filter-tcp=1935 --filter-udp=1935 --dpi-desync=fake,split2 ^
--dpi-desync-autottl=3 --dpi-desync-fooling=md5sig ^
--filter-tcp=50000 --dpi-desync=fake,split2 --dpi-desync-autottl=3 --dpi-desync-fooling=md5sig --new ^
--filter-tcp=443 --dpi-desync=fake,split2 --dpi-desync-autottl=2 --dpi-desync-fooling=md5sig --new

POPD
