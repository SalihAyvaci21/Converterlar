@echo off
color 0A
title Salih Atolye - Otomatik Kurulum Sihirbazi

echo ========================================================
echo   SALIH'IN DIJITAL ATOLYESI - KURULUM BASLIYOR
echo ========================================================
echo.
echo [1/4] Python kontrol ediliyor...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo HATA: Bilgisayarda Python yuklu degil veya PATH'e eklenmemis!
    echo Lutfen once Python yukleyin (Microsoft Store'dan indirebilirsiniz).
    pause
    exit
)
echo Python bulundu. Devam ediliyor...
echo.

echo [2/4] Gerekli kutuphaneler internetten indiriliyor...
echo Lutfen bekleyin, bu islem internet hizina gore surebilir.
pip install -r requirements.txt
echo.

echo [3/4] EXE dosyasi olusturuluyor (Derleme)...
echo Bu islem biraz zaman alabilir, lutfen kapatmayin.
pyinstaller --noconsole --onefile Converterlar.py
echo.

echo [4/4] Temizlik yapiliyor ve dosya hazirlaniyor...
:: Eski gereksiz dosyalari temizle
if exist "Converterlar.py" del "Converterlar.py"
if exist "build" rmdir /s /q "build"

:: EXE'yi dist klasorunden ana dizine tasi
if exist "dist\Converterlar.exe" (
    move "dist\Converterlar.exe" ".\Converterlar.exe"
    rmdir /s /q "dist"
    echo.
    echo ========================================================
    echo   BASARILI! KURULUM TAMAMLANDI.
    echo   'SalihAtolye_Calistir.exe' dosyasi olusturuldu.
    echo ========================================================
) else (
    echo.
    echo HATA: EXE dosyasi olusturulamadi. Bir sorun var.
)

pause