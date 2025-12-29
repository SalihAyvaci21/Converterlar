# 🛠️ Dijital Mühendislik Atölyesi (Salih'in Atölyesi) v3.2

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Lisans](https://img.shields.io/badge/License-MIT-green)
![Durum](https://img.shields.io/badge/Status-Aktif-orange)

**Gömülü Sistem Mühendisleri**, **FPGA Geliştiricileri** ve **Maker**'lar için tasarlanmış kapsamlı bir "İsviçre Çakısı" masaüstü uygulamasıdır.

Tamamen **Python (Tkinter)** ile geliştirilen bu araç; dosya dönüştürücülerini, elektronik hesaplayıcıları ve görselleştirme araçlarını modern, koyu temalı tek bir arayüzde birleştirir.

## 🚀 Özellikler

### 1. 🔄 Dönüştürücüler
* **Belge:** Word ↔ PDF dönüşümü.
* **Medya:** Format değiştirici (PNG, JPG, WEBP, BMP) & Video'dan GIF yapma (FPS ayarlı).
* **Resim Araçları:** Resimleri PDF dosyasına çevirme.

### 2. ⚡ FPGA & Gömülü Sistem Araçları
* **Taban Çevirici:** Canlı olarak Decimal ↔ Hexadecimal ↔ Binary dönüşümü.
* **Timer Hesaplayıcı:** Sistem frekansına göre Baud Rate veya Zamanlayıcı sayaç (counter) değerlerini hesaplar.
* **Hex Araçları:** Resimleri OLED ekranlar için Hex dizisine (array) çevirir (veya tam tersi).
* **ASCII Aracı:** UART hata ayıklama için Metin ↔ Hex dönüşümü.
* **7-Segment Editörü:** Ortak Anot/Katot (Common Anode/Cathode) hex kodlarını üreten görsel editör.
* **RGB565 Seçici:** Renk seçip TFT ekranlar için 16-bit Hex kodunu verir.

### 3. 🔌 Elektronik Komponent Hesaplayıcıları
* **LED Direnci:** LED'ler için gerekli seri direnci hesaplar.
* **SMD Çözücü:** * SMD Dirençler (örn: `103`, `4R7`).
    * SMD Kapasitörler (örn: `104`, `475`).

### 4. 🛠️ 3D & Yardımcı Araçlar
* **STL Önizleme:** Bir STL dosyasının 4 açılı (Üst, Ön, Yan, İzo) teknik resmini çıkarır.
* **Lithophane Oluşturucu:** Herhangi bir resmi, 3D yazıcıdan basılabilir kabartma modele (STL) dönüştürür.
* **QR Oluşturucu:** Metin veya linklerden QR kod üretir ve kaydeder.

## 💿 Kurulum ve Çalıştırma

Bu projeyi bilgisayarınızda çalıştırmak için iki yöntem vardır:

### Yöntem 1: Otomatik Kurulum (Önerilen) ⚡
Kod veya kütüphanelerle uğraşmak istemiyorsanız:

1.  Bu depoyu indirin (ZIP olarak veya git clone ile).
2.  Klasörün içindeki **`KURULUM_YAP.bat`** dosyasına çift tıklayın.
3.  Sihirbaz otomatik olarak gerekli kütüphaneleri indirecek ve **`SalihAtolye_Calistir.exe`** dosyasını oluşturacaktır.
4.  Oluşan `.exe` dosyasına tıklayıp kullanmaya başlayabilirsiniz.

### Yöntem 2: Manuel Kurulum (Geliştiriciler İçin) 👨‍💻

1.  **Depoyu klonlayın:**
    ```bash
    git clone [https://github.com/SalihAyvaci21/Converterlar.git](https://github.com/SalihAyvaci21/Converterlar.git)
    cd Digital-Engineering-Workshop
    ```

2.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Uygulamayı başlatın:**
    ```bash
    python SalihAtolye.py
    ```

## 🧩 Kullanılan Teknolojiler
* **Arayüz (GUI):** `tkinter`, `ttk` (Özel Koyu Tema)
* **Görüntü İşleme:** `Pillow (PIL)`
* **3D İşleme:** `numpy-stl`, `matplotlib`, `numpy`
* **Video İşleme:** `moviepy`
* **Ofis Dosyaları:** `docx2pdf`, `pdf2docx`
* **Araçlar:** `qrcode`, `webbrowser`
* **Paketleme:** `PyInstaller`

## 👤 Geliştirici

**Salih Tekin Ayvacı**

* LinkedIn: [salih-tekin-ayvaci](https://linkedin.com/in/salih-tekin-ayvaci)
* GitHub: [@SalihAyvaci21](https://github.com/SalihAyvaci21)
* Instagram: [@salih_ayvaci21](https://instagram.com/salih_ayvaci21)

---
*Mühendisler için ❤️ ile tasarlandı.*# Converterlar
"# Converterlar" 
