# 🏭 Malzeme ve Parça Seçimi & Maliyet Raporu Uygulaması

<div align="center">
  <img src="icon.png" alt="Uygulama Logo" width="200"/>
  <br>
  <p>
    <strong>Endüstriyel malzeme ve parça seçimi için kapsamlı maliyet analizi çözümü</strong>
  </p>
</div>

## 📑 İçindekiler
1. [Özellikler](#-özellikler)
2. [Kullanım Kılavuzu](#-kullanım-kılavuzu)
3. [Raporlar](#-raporlar)
4. [Sık Karşılaşılan Sorunlar](#-sık-karşılaşılan-sorunlar)
5. [Güncelleme Geçmişi](#-güncelleme-geçmişi)
6. [Kurulum](#️-kurulum)
7. [Katkıda Bulunma](#-katkıda-bulunma)
8. [İletişim](#-iletişim)

## 🚀 Özellikler

### Ana Özellikler
- **Kapsamlı Malzeme Veritabanı**
  - 1000+ malzeme çeşidi
  - Detaylı teknik özellikler
  - Güncel fiyat bilgileri
  - Tedarikçi bilgileri

- **Gelişmiş Maliyet Hesaplama**
  - Otomatik birim fiyat hesaplama
  - İşçilik maliyeti hesaplama
  - Fire oranı hesaplama
  - Kur bazlı hesaplama
  - Vergiler ve ek maliyetler

- **Profesyonel Raporlama**
  - PDF formatında detaylı raporlar
  - Excel export özelliği
  - Özelleştirilebilir rapor şablonları
  - Grafik ve tablolar
  - Karşılaştırmalı analiz raporları

### Ek Özellikler
- **Görsel Analiz Araçları**
  - 3D parça önizleme
  - Teknik çizim görüntüleme
  - Zoom ve pan özellikleri
  - Ölçülendirme araçları

- **Veritabanı Yönetimi**
  - SQL Server entegrasyonu
  - Otomatik yedekleme
  - Veri senkronizasyonu
  - Çoklu kullanıcı desteği

## 💻 Kullanım Kılavuzu

### Ana Menü Özellikleri

#### 1. Yeni Rapor Oluşturma
1. Ana menüden "Yeni Rapor" seçin
2. Proje bilgilerini girin:
   - Proje adı
   - Müşteri bilgileri
   - Tarih
3. Malzeme seçimi yapın:
   - Kategoriden malzeme seçin
   - Miktarı belirleyin
   - Özel parametreleri ayarlayın
4. Hesaplama yapın
5. Raporu kaydedin

#### 2. Rapor Görüntüleme
- Kayıtlı raporları listeleyin
- Tarih aralığı filtreleme
- Müşteri bazlı filtreleme
- Rapor detaylarını görüntüleme
- Rapor karşılaştırma

#### 3. Maliyet Analizi
- Malzeme maliyeti analizi
- İşçilik maliyeti analizi
- Ek maliyet kalemleri
- Kâr marjı hesaplama
- Vergi hesaplamaları


## 📈 Raporlar

### 1. Temel Maliyet Raporu
- Toplam malzeme maliyeti
- İşçilik maliyeti
- Genel giderler
- Toplam maliyet
- Kâr marjı
- KDV

### 2. Detaylı Maliyet Raporu
- Parça bazlı maliyet analizi
- İşçilik süreleri
- Fire oranları
- Tedarikçi bilgileri
- Teslimat süreleri

### 3. Karşılaştırma Raporu
- Rapor farklılıkları
- Maliyet değişimleri
- Grafik gösterimi
- Trend analizi

## ❗ Sık Karşılaşılan Sorunlar

### Veritabanı Bağlantı Sorunları
1. SQL Server servisinin çalıştığından emin olun
2. Bağlantı bilgilerini kontrol edin
3. Firewall ayarlarını kontrol edin

### Performans Sorunları
1. Temp dosyalarını temizleyin
2. Veritabanı indekslerini yeniden oluşturun
3. RAM kullanımını kontrol edin

## 🔄 Güncelleme Geçmişi

### v1.0.0 (2024-03-03)
- İlk sürüm yayınlandı
- Temel özellikler eklendi
- Veritabanı entegrasyonu

### v1.0.1 (2024-03-04)
- Hata düzeltmeleri
- Performans iyileştirmeleri
- Yeni raporlama özellikleri

## 🛠️ Kurulum

### Sistem Gereksinimleri
- Windows 10/11 (64-bit)
- SQL Server 2019 veya üzeri
- Python 3.12 veya üzeri
- Minimum 4GB RAM

### Hızlı Kurulum
1. SQL Server'ı kurun ve MalzemeParcaDB veritabanını oluşturun
2. Python bağımlılıklarını yükleyin:
```bash
pip install -r requirements.txt
```
3. Veritabanı bağlantı ayarlarını yapın:
```python
# db_connection.py
SERVER = 'your_server_name'
DATABASE = 'MalzemeParcaDB'
USERNAME = 'your_username'
PASSWORD = 'your_password'
```
4. Uygulamayı başlatın:
```bash
python main.py
```

### Exe Oluşturma
```bash
python -m PyInstaller --onefile --windowed --icon=icon.png --add-data "icon.png;." main.py
```


## 📞 İletişim

### Geliştirici Bilgileri
- **İsim**: [Seyfullah KIZILKAYA]
- **E-posta**: [kizilkayasyfllh@gmail.com]
- **LinkedIn**: [www.linkedin.com/in/seyfullah-kizilkaya-651259222]

---

**Not**: Bu dokümantasyon sürekli güncellenmektedir. En son güncelleme: 04.03.2024
