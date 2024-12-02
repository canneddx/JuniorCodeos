@echo off


:: Отключение лимитов резервирования пропускной способности
netsh interface tcp set global autotuninglevel=high
netsh interface tcp set global rss=enabled

:: Отключение задержек обработки пакетов
netsh int tcp set global timestamps=disabled

:: Установка более короткого интервала отправки
netsh interface tcp set global congestionprovider=ctcp

:: Очистка и обновление DNS-кеша
ipconfig /flushdns
ipconfig /registerdns

:: Освобождение и обновление IP-адреса
ipconfig /release
ipconfig /renew
