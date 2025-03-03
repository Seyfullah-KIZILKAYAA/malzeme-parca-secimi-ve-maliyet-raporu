# Tost Makinesi Parça Seçimi ve Maliyet Raporu

Bu proje, bir tost makinesinin parçalarını seçmenize, 3D görsel olarak incelemenize ve maliyet raporunu oluşturmanıza olanak sağlayan bir uygulamadır.

## Özellikler

### Parça Seçimi
- Ana kategori ve alt kategori bazında parça seçimi
- Her parça için detaylı bilgi ve fiyat görüntüleme
- Çift tıklama ile hızlı parça seçimi
- Seçilen parçaların listesini görüntüleme

### 3D Görsel Gösterim
- İnteraktif 3D tost makinesi modeli
- Fare ile modeli döndürme ve inceleme
- Seçilen parçaların gerçek zamanlı görsel gösterimi
- Parça değişimlerinde altın sarısı yanıp sönme efekti
- Önceden tanımlanmış görünüm açıları (Ön, Yan, Üst, İzometrik)

### Maliyet Raporu
- Seçilen parçaların detaylı maliyet analizi
- Toplam maliyet hesaplama
- Parça bazlı maliyet dökümü
- PDF formatında rapor oluşturma

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

## Gereksinimler

- Python 3.x
- PyQt5
- Matplotlib
- NumPy
- ReportLab (PDF raporu için)

## Kurulum

1. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı çalıştırın:
```bash
python main.py
```

## Geliştirici Notları

- Parça eşleştirmeleri için alt_kategori ve parça adları kullanılır
- 3D model parçaları önceden tanımlı vertex ve face bilgileriyle oluşturulur
- Görsel performans için optimizasyonlar yapılmıştır
- Yanıp sönme efekti için QTimer kullanılmıştır

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.
