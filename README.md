# Tost Makinesi Parça Seçimi ve Maliyet Raporu

Bu proje, bir tost makinesinin parçalarını seçip maliyet raporu oluşturabileceğiniz bir masaüstü uygulamasıdır. Uygulama, parça seçimlerini interaktif bir 3D model üzerinde görselleştirme özelliğine sahiptir.

## Özellikler

### Parça Seçimi
- Ana kategori ve alt kategori bazında parça seçimi
- Her parça için detaylı bilgi görüntüleme
- Çift tıklama ile hızlı parça seçimi
- Seçilen parçaların otomatik maliyetlendirmesi

### 3D Görselleştirme
- İnteraktif 3D tost makinesi modeli
- Seçilen parçaların gerçek zamanlı görselleştirilmesi
- Parça değişimlerinde altın sarısı yanıp sönme efekti
- Fare ile modeli döndürme ve inceleme
- Hazır görünüm açıları (Ön, Yan, Üst, İzometrik)

### Maliyet Raporu
- Seçilen parçaların detaylı maliyet analizi
- Toplam maliyet hesaplama
- Parça bazlı maliyet dökümü
- PDF formatında rapor oluşturma

## Kullanım

1. Ana kategoriden bir seçim yapın
2. Alt kategoriden parça seçin
3. 3D modelde seçilen parçanın konumunu görün
4. Parça değiştiğinde altın sarısı yanıp sönme efekti ile değişikliği takip edin
5. Tüm parçaları seçtikten sonra maliyet raporunu oluşturun

### Model Kontrolleri
- **Fare Sürükleme**: Modeli döndürme
- **Görünüm Butonları**: 
  - Ön Görünüm
  - Yan Görünüm
  - Üst Görünüm
  - İzometrik Görünüm

## Gereksinimler

- Python 3.8+
- PyQt5
- NumPy
- Matplotlib
- ReportLab (PDF raporu için)

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/kullanici/tost-makinesi-maliyet.git
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:
```bash
python main.py
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.
