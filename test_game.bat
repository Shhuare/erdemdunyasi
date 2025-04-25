@echo off
echo Erdem Dunyasi - Test Araci
echo ==========================

rem Python kontrolü
echo Python kontrolu yapiliyor...
python --version
if %errorlevel% neq 0 (
    echo Python bulunamadi! Lutfen Python 3.7 veya daha yeni bir surumu yukleyin.
    pause
    exit /b 1
)

echo Oyun testleri baslatiliyor...
python src/run_test.py

pause 