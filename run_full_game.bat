@echo off
echo Erdem Dunyasi - Tam Surum
echo ========================

rem Python kontrolü
echo Python kontrolu yapiliyor...
python --version
if %errorlevel% neq 0 (
    echo Python bulunamadi! Lutfen Python 3.7 veya daha yeni bir surumu yukleyin.
    pause
    exit /b 1
)

rem Pygame kontrolü
echo Pygame kontrolu yapiliyor...
python -c "import pygame" 2>nul
if %errorlevel% neq 0 (
    echo Pygame bulunamadi! Yukleniyor...
    pip install pygame
    if %errorlevel% neq 0 (
        echo Pygame yuklenemedi! Lutfen manuel olarak 'pip install pygame' komutunu calistirin.
        pause
        exit /b 1
    )
)

rem Asset durumunu kontrol et
echo Assetler kontrol ediliyor...
IF NOT EXIST assets\sprites\player\hero_male.png (
    echo Assetler hazirlanmasi gerekiyor...
    call configure_assets.bat
)

echo Tam surum Erdem Dunyasi baslatiliyor...
python src/run_game.py

pause 