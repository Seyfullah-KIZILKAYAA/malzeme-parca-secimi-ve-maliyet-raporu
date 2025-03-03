# Malzeme ve Parça Seçimi & Maliyet Raporu Uygulaması

Bu uygulama, malzeme ve parça seçimi yaparak maliyet raporu oluşturmanıza olanak sağlayan kapsamlı bir yazılım çözümüdür.

## 🚀 Özellikler

- **Malzeme ve Parça Seçimi**: Geniş veritabanından malzeme ve parça seçimi
- **Maliyet Hesaplama**: Otomatik ve detaylı maliyet hesaplama
- **Rapor Oluşturma**: PDF formatında detaylı raporlar
- **Rapor Karşılaştırma**: Farklı raporları karşılaştırma imkanı
- **Görsel Gösterici**: Seçilen parçaların görsel önizlemesi
- **Veritabanı Entegrasyonu**: SQL Server ile güvenli veri yönetimi
- **Geçmiş Kayıtları**: Önceki raporlara kolay erişim

## 📋 Gereksinimler

- Python 3.12 veya üzeri
- SQL Server 2019 veya üzeri
- Windows 10/11 işletim sistemi

### Python Kütüphaneleri

## Kullanım

1. Ana kategoriden başlayarak parça seçimini yapın
2. Alt kategorileri seçerek detaylı parça seçimini tamamlayın
3. 3D modelde seçilen parçaları inceleyin
   - Fareyi sürükleyerek modeli döndürün
   - Görünüm butonları ile hazır açıları kullanın
4. Maliyet raporunu oluşturun

## Görsel Özellikler

- Her parça kendi özel rengiyle gösterilir
- Yeni seçilen veya değiştirilen parçalar altın sarısı renkte yanıp söner
- Parçalar yarı saydam gösterim ile iç detayları görülebilir
- Kenarlar siyah çizgilerle belirginleştirilmiştir

## Geliştirici Notları

- Parça eşleştirmeleri için alt_kategori ve parça adları kullanılır
- 3D model parçaları önceden tanımlı vertex ve face bilgileriyle oluşturulur
- Görsel performans için optimizasyonlar yapılmıştır
- Yanıp sönme efekti için QTimer kullanılmıştır

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.
