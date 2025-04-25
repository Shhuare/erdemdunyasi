@echo off
title Erdem Dunyasi Oyun Baslatici
color 0A

echo ====================================
echo =  ERDEM DUNYASI OYUN BASLATICI   =
echo ====================================
echo.

:: Python kontrolü yap
python --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo Python bulunamadi!
    echo.
    echo Oyunu calistirmak icin once Python'u kurmaniz gerekiyor.
    echo Python'u https://www.python.org/downloads/ adresinden indirebilirsiniz.
    echo.
    echo 1. Python'u indirin (Python 3.7 veya üstü önerilir)
    echo 2. Kurulum sirasinda "Add Python to PATH" secenegini isaretleyin
    echo 3. Kurulum tamamlandiktan sonra bu baslaticiyi tekrar calistirin
    echo.
    pause
    exit /b
)

:: Tkinter paketi kontrol et (başlatıcı GUI için gerekli)
python -c "import tkinter" 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo Tkinter bulunamadi! Python kurulumunuzu kontrol edin.
    echo Tkinter, Python'un standart kurulumunda gelmelidir.
    echo.
    pause
    exit /b
)

echo ====================================
echo =      BASLATIYOR...              =
echo ====================================
echo.

:: Başlatıcıyı çalıştır
if exist launcher.py (
    python launcher.py
) else (
    echo launcher.py dosyasi bulunamadi!
    echo.
    echo Oyun dosyalari düzgün yuklenemedi veya zarar gormus olabilir.
    echo.
    
    :: Ana oyun dosyasını doğrudan çalıştırmayı dene
    if exist main.py (
        echo Ana oyun dosyasi bulundu. Dogrudan ana oyunu baslatma deneniyor...
        python main.py
    ) else if exist src\main.py (
        echo src/main.py bulundu. Dogrudan ana oyunu baslatma deneniyor...
        python src\main.py
    ) else (
        echo Oyun dosyalari bulunamadi!
        echo Lutfen oyun dosyalarinin eksik veya bozuk olmadigindan emin olun.
    )
    
    pause
)

exit /b 