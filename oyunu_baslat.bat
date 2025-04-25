@echo off
title Erdem Dunyasi - Duzeltmeli Baslatici
color 0A

echo ============================================================
echo                 ERDEM DUNYASI BASLATICI
echo                  DUZELTMELI SURUM v1.0
echo ============================================================
echo.

REM Python kontrolu
python --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo HATA: Python bulunamadi!
    echo Python'u yukleyiniz: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Pygame kontrolu
python -c "import pygame; print(f'pygame {pygame.version.ver}')" 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo HATA: Pygame bulunamadi!
    echo Pygame'i yuklemek icin: pip install pygame
    echo [Y] Evet, yukle  [N] Hayir, cikmak istiyorum
    choice /C YN /M "Pygame yuklensin mi"
    if %ERRORLEVEL% EQU 1 (
        echo Pygame yukleniyor...
        pip install pygame
    ) else (
        echo Islem iptal edildi.
        pause
        exit /b 2
    )
)

:MENU
cls
echo.
echo Erdem Dunyasi - Duzeltmeli Baslatici
echo ===================================
echo.
echo Secenekler:
echo -------------------
echo 1. Normal Mod (Duzeltmelerle)
echo 2. Tam Ekran Mod (Duzeltmelerle)
echo 3. Debug Modu (Gelistirici)
echo 4. Oyun Bilgileri
echo 5. Cikis
echo.

choice /C 12345 /M "Secim yapiniz"
set CHOICE=%ERRORLEVEL%

if %CHOICE% EQU 1 (
    echo Normal mod baslatiliyor...
    python oyunu_baslat.py
    goto :OYUN_SONRASI
) else if %CHOICE% EQU 2 (
    echo Tam ekran mod baslatiliyor...
    python oyunu_baslat.py --fullscreen
    goto :OYUN_SONRASI
) else if %CHOICE% EQU 3 (
    echo Debug modu baslatiliyor...
    python oyunu_baslat.py --debug
    goto :OYUN_SONRASI
) else if %CHOICE% EQU 4 (
    goto :BILGI
) else if %CHOICE% EQU 5 (
    goto :CIKIS
)

:BILGI
cls
echo.
echo Erdem Dunyasi - Oyun Bilgileri
echo ===========================
echo.
echo Bu baslatici, oyundaki cesitli hatalari duzeltmek icin
echo tasarlanmistir. Asagidaki hatalari otomatik duzelterek
echo oyunun daha sorunsuz calismasini saglar:
echo.
echo 1. Gorev sistemi duzenlemeleri
echo 2. Dunya render metodu hata duzeltmeleri
echo 3. Eksik UI elemanlarinin otomatik olusturulmasi
echo.
echo Kontroller:
echo - W,A,S,D: Hareket etme
echo - E: Esya kullanma / Etkilesim
echo - I: Envanter
echo - Q: Gorev menusu
echo - Space: Ruh hayvanina donusme
echo - ESC: Oyun menusu
echo.
pause
goto :MENU

:CIKIS
cls
echo.
echo Erdem Dunyasi Baslatici kapatiliyor...
exit /b 0

:OYUN_SONRASI
echo.
echo Oyun sonlandi.
pause
goto :MENU 