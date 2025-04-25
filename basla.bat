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

echo.
echo Baslatici secimleri:
echo -------------------
echo 1. Normal mod
echo 2. Tam ekran mod
echo 3. Debug mod
echo 4. Hizli baslat (intro atla)
echo 5. Cikis
echo.

choice /C 12345 /M "Secim yapiniz"

if %ERRORLEVEL% EQU 1 (
    echo Normal mod baslatiliyor...
    python yeni_launcher.py
) else if %ERRORLEVEL% EQU 2 (
    echo Tam ekran mod baslatiliyor...
    python yeni_launcher.py --fullscreen
) else if %ERRORLEVEL% EQU 3 (
    echo Debug mod baslatiliyor...
    python yeni_launcher.py --debug
) else if %ERRORLEVEL% EQU 4 (
    echo Hizli baslatiliyor...
    python yeni_launcher.py --skip-intro
) else if %ERRORLEVEL% EQU 5 (
    echo Cikis yapiliyor...
    exit /b 0
)

echo.
echo Oyun sonlandi.
pause 