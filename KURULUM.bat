@echo off
color 0B
title Salih Atolye - Otomatik Kurulum ve Derleme

:: ---------------------------------------------------------
:: AYARLAR (Dosya adını buraya yazın)
:: ---------------------------------------------------------
set DOSYA_ADI=Converterlar.py
set EXE_ADI=Salih_Atolye_App.exe

echo ========================================================
echo   SALIH'IN DIJITAL ATOLYESI - KURULUM BASLIYOR
echo ========================================================
echo.

:: ---------------------------------------------------------
:: ADIM 1: Python Varlik Kontrolü
:: ---------------------------------------------------------
echo [1/4] Python kontrol ediliyor...

:: Standart 'python' komutunu dener
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [HATA] Python bulunamadi!
    echo Lutfen Python'u indirip kurun ve kurulum sirasinda
    echo "Add Python to PATH" secenegini isaretlediginizden emin olun.
    pause
    exit
)

for /f "delims=" %%i in ('python --version') do set PYTHON_VER=%%i
echo %PYTHON_VER% bulundu. Islemlere baslaniyor...
echo.

:: ---------------------------------------------------------
:: ADIM 2: Kütüphane Yükleme
:: ---------------------------------------------------------
echo [2/4] Gerekli kutuphaneler yukleniyor...
echo (requirements.txt dosyasi okunuyor...)

if not exist requirements.txt (
    echo [UYARI] requirements.txt bulunamadi!
    echo Kutuphaneler manuel yuklenmek zorunda kalabilir.
    echo PyInstaller manuel olarak yukleniyor...
    python -m pip install pyinstaller
) else (
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
)
echo.

:: ---------------------------------------------------------
:: ADIM 3: EXE Oluşturma
:: ---------------------------------------------------------
echo [3/4] EXE dosyasi derleniyor...
echo Bu islem bilgisayar hizina gore biraz zaman alabilir...
echo.

:: Dosya var mı kontrol et
if not exist "%DOSYA_ADI%" (
    echo [HATA] '%DOSYA_ADI%' dosyasi bulunamadi!
    echo Lutfen Python dosyanizin adini bu bat dosyasinin basindaki
    echo 'set DOSYA_ADI=...' kisminda dogru yazdiginizdan emin olun.
    pause
    exit
)

:: --noconsole: Siyah konsol penceresi acilmaz
:: --onefile: Tek parca exe yapar
python -m PyInstaller --noconsole --onefile "%DOSYA_ADI%"
echo.

:: ---------------------------------------------------------
:: ADIM 4: Temizlik ve Düzenleme
:: ---------------------------------------------------------
echo [4/4] Gereksiz dosyalar temizleniyor...

:: .spec dosyasını sil (dosya adından türetilir)
if exist "*.spec" del "*.spec"

:: build klasörünü sil
if exist "build" rmdir /s /q "build"

:: EXE'yi dist klasöründen ana dizine taşı
if exist "dist\%DOSYA_ADI:.py=.exe%" (
    move "dist\%DOSYA_ADI:.py=.exe%" ".\%EXE_ADI%"
    rmdir /s /q "dist"
    echo.
    echo ========================================================
    echo   BASARILI! 
    echo   '%EXE_ADI%' dosyasi olusturuldu.
    echo ========================================================
) else (
    echo.
    echo [HATA] EXE olusturulamadi.
    echo Lutfen kodda hata olmadigindan emin olun.
)

pause
