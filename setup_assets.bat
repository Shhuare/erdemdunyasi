@echo off
echo Erdem Dunyasi - Asset Kurulum Araci
echo =====================================

rem Python kontrolü
echo Python kontrolu yapiliyor...
python --version
if %errorlevel% neq 0 (
    echo Python bulunamadi! Lutfen Python 3.7 veya daha yeni bir surumu yukleyin.
    pause
    exit /b 1
)

rem Asset import modülü kontrolü
echo Asset importer modulu kontrol ediliyor...
python -c "import sys; sys.path.append('.'); import src.asset_importer" 2>nul
if %errorlevel% neq 0 (
    echo src.asset_importer modulu yuklenemedi! Proje yapisi dogru mu?
    echo Hata kodu: %errorlevel%
    pause
    exit /b 1
)

rem Assets klasörü oluştur
echo Asset klasor yapisini kuruyorum...
python -m src.asset_importer --setup
if %errorlevel% neq 0 (
    echo Asset klasor yapisi kurulamadi!
    echo Hata kodu: %errorlevel%
    pause
    exit /b 1
)

rem Eğer asset paketi belirtilmişse
if not "%~1"=="" (
    echo %1 paketini isliyorum...
    python -m src.asset_importer --source "%~1" --recursive
    if %errorlevel% neq 0 (
        echo Asset paketi isleme hatasi!
        echo Hata kodu: %errorlevel%
        pause
        exit /b 1
    )
) else (
    echo Lutfen ice aktarilacak klasoru belirtin.
    echo Ornek: setup_assets.bat "C:\fantasy_rpg_asset_pack"
    pause
    exit /b 1
)

rem Asset kaydını güncelle
echo Asset kayitlarini guncelliyorum...
python -m src.asset_importer --update
if %errorlevel% neq 0 (
    echo Asset kayitlari guncellenemedi!
    echo Hata kodu: %errorlevel%
    pause
    exit /b 1
)

echo Islem tamamlandi!
pause 