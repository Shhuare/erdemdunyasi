@echo off
title Erdem Dunyasi - Gelismis Baslatici
color 0A

echo ============================================================
echo                 ERDEM DUNYASI BASLATICI
echo                    GELISMIS SURUM
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
echo Erdem Dunyasi - Gelismis Baslatici
echo ===================================
echo.
echo Secenekler:
echo -------------------
echo 1. Tam Oyun (Gelismis Baslatici ile)
echo 2. Test Modu (Debug aktivasyon ile)
echo 3. Performans Modu (Dusuk Grafik)
echo 4. Varliklari Yapılandir
echo 5. Yardim
echo 6. Cikis
echo.

choice /C 123456 /M "Secim yapiniz"
set CHOICE=%ERRORLEVEL%

if %CHOICE% EQU 1 (
    goto :TAM_OYUN
) else if %CHOICE% EQU 2 (
    goto :TEST_MODU
) else if %CHOICE% EQU 3 (
    goto :PERFORMANS_MODU
) else if %CHOICE% EQU 4 (
    goto :VARLIK_YAPILANDIR
) else if %CHOICE% EQU 5 (
    goto :YARDIM
) else if %CHOICE% EQU 6 (
    goto :CIKIS
)

:TAM_OYUN
cls
echo Erdem Dunyasi Tam Surum baslatiyor...
echo.
echo Secenekler:
echo 1. Normal Mod
echo 2. Tam Ekran Mod
echo 3. Geri Don
echo.
choice /C 123 /M "Secim yapiniz"
if %ERRORLEVEL% EQU 1 (
    python yeni_launcher.py --skip-intro
) else if %ERRORLEVEL% EQU 2 (
    python yeni_launcher.py --skip-intro --fullscreen
) else if %ERRORLEVEL% EQU 3 (
    goto :MENU
)
goto :OYUN_SONRASI

:TEST_MODU
cls
echo Test Modu baslatiyor...
echo Bu modda debug secenekleri aktiftir.
echo.
python yeni_launcher.py --debug
goto :OYUN_SONRASI

:PERFORMANS_MODU
cls
echo Performans Modu baslatiyor...
echo Bu mod dusuk grafik ayarlari ile calisir.
echo.
set PYGAME_HIDE_SUPPORT_PROMPT=1
python -c "import os; os.environ['ERDEM_DUNYASI_LOW_GRAPHICS'] = '1'; __import__('yeni_launcher').main()"
goto :OYUN_SONRASI

:VARLIK_YAPILANDIR
cls
echo Varliklar yapılandiricı baslatılıyor...
echo.
if exist configure_assets.bat (
    call configure_assets.bat
) else (
    echo Varlik yapilandirma dosyasi (configure_assets.bat) bulunamadi!
)
echo.
pause
goto :MENU

:YARDIM
cls
echo Erdem Dunyasi - Yardim
echo =====================
echo.
echo Kontroller:
echo - W,A,S,D: Hareket etme
echo - E: Esya kullanma / Etkilesim
echo - I: Envanter
echo - Q: Gorev menusu
echo - Space: Ruh hayvanina donusme
echo - ESC: Oyun menusu
echo.
echo Oyun Modlari:
echo - Tam Oyun: Tum ozelliklerin aktif oldugu normal mod
echo - Test Modu: Gelistirici ozelliklerini aktive eder
echo - Performans: Dusuk grafik ayarlari ile calisir
echo.
echo Sorun Giderme:
echo - Eger oyun calismiyorsa, once varliklari yapilandirin
echo - Hata mesajlarini okuyun ve hatanin nedenini anlayin
echo - Sorun devam ederse sorunu raporlayin
echo.
pause
goto :MENU

:CIKIS
cls
echo Erdem Dunyasi Baslatici kapatiliyor...
exit /b 0

:OYUN_SONRASI
echo.
echo Oyun sonlandi.
pause
goto :MENU 