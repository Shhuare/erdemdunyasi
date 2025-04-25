@echo off
echo Erdem Dunyasi - Asset Yapilandirma Araci
echo =====================================

rem Python kontrolü
echo Python kontrolu yapiliyor...
python --version
if %errorlevel% neq 0 (
    echo Python bulunamadi! Lutfen Python 3.7 veya daha yeni bir surumu yukleyin.
    pause
    exit /b 1
)

echo Asset yapilandirici calistiriliyor...
python -m src.asset_configurator

if %errorlevel% neq 0 (
    echo Asset yapilandirma islemi sirasinda bir hata olustu!
    echo Hata kodu: %errorlevel%
    pause
    exit /b 1
)

echo.
echo Asset yapilandirma islemi basariyla tamamlandi!
echo Oyun icin tum resim, ses ve karakter dosyalari hazir.
pause 