from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, 
                            QFileDialog, QInputDialog, QLineEdit, QDialog, QFormLayout, QHBoxLayout)
from PyQt5.QtCore import Qt
from datetime import datetime
import pandas as pd
import os
import shutil

class RaporKaydet(QWidget):
    def __init__(self, maliyet_raporu):
        super().__init__()
        self.maliyet_raporu = maliyet_raporu
        self.setup_ui()
        
    def setup_ui(self):
        """Arayüz bileşenlerini oluşturur."""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 15)
        self.layout.setSpacing(15)
        
        # Başlık etiketi
        self.baslik_label = QLabel("Rapor Kaydetme")
        self.baslik_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; padding: 5px;")
        self.layout.addWidget(self.baslik_label)
        
        # Açıklama etiketi
        self.aciklama_label = QLabel("Mevcut raporu kaydetmek için aşağıdaki butonları kullanabilirsiniz.")
        self.aciklama_label.setStyleSheet("font-size: 14px; color: #555; padding: 5px;")
        self.layout.addWidget(self.aciklama_label)
        
        # Butonlar için yatay düzen
        buton_layout = QHBoxLayout()
        
        # Raporu otomatik kaydet butonu
        self.kaydet_button = QPushButton("Raporu Kaydet")
        self.kaydet_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.kaydet_button.clicked.connect(self.raporu_kaydet)
        buton_layout.addWidget(self.kaydet_button)
        
        # Raporu farklı konuma kaydet butonu
        self.farkli_kaydet_button = QPushButton("Farklı Konuma Kaydet")
        self.farkli_kaydet_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        self.farkli_kaydet_button.clicked.connect(self.raporu_farkli_kaydet)
        buton_layout.addWidget(self.farkli_kaydet_button)
        
        self.layout.addLayout(buton_layout)
        
        # Kayıt yeri bilgisi
        self.kayit_bilgisi = QLabel("Raporlar 'gecmis' klasörüne kaydedilir.")
        self.kayit_bilgisi.setStyleSheet("font-style: italic; color: #777; padding: 5px;")
        self.layout.addWidget(self.kayit_bilgisi)
        
    def raporu_kaydet(self):
        """Mevcut raporu 'gecmis' klasörüne kaydeder."""
        # Tablodaki verileri kontrol et
        if self.maliyet_raporu.tablo.rowCount() == 0:
            QMessageBox.warning(self, "Uyarı", "Kaydedilecek rapor bulunamadı! Önce parça seçimi yapın.")
            return
        
        # Rapor adını kullanıcıdan al
        rapor_adi, ok = QInputDialog.getText(self, "Rapor Adı", "Rapor için bir isim girin:", QLineEdit.Normal, "")
        if not ok or not rapor_adi:
            return
        
        # Geçmiş klasörünü kontrol et ve oluştur
        gecmis_klasoru = "gecmis"
        if not os.path.exists(gecmis_klasoru):
            os.makedirs(gecmis_klasoru)
        
        # Dosya adını oluştur (rapor adı + tarih)
        tarih_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        dosya_adi = f"{rapor_adi}_{tarih_str}.xlsx"
        dosya_yolu = os.path.join(gecmis_klasoru, dosya_adi)
        
        try:
            # Excel dosyasını oluştur
            self._excel_olustur(dosya_yolu, rapor_adi)
            QMessageBox.information(self, "Başarılı", f"Rapor başarıyla kaydedildi:\n{dosya_yolu}")
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Rapor kaydedilirken bir hata oluştu:\n{str(e)}")
    
    def raporu_farkli_kaydet(self):
        """Mevcut raporu kullanıcının seçtiği konuma kaydeder."""
        # Tablodaki verileri kontrol et
        if self.maliyet_raporu.tablo.rowCount() == 0:
            QMessageBox.warning(self, "Uyarı", "Kaydedilecek rapor bulunamadı! Önce parça seçimi yapın.")
            return
        
        # Rapor adını kullanıcıdan al
        rapor_adi, ok = QInputDialog.getText(self, "Rapor Adı", "Rapor için bir isim girin:", QLineEdit.Normal, "")
        if not ok or not rapor_adi:
            return
        
        # Dosya adını oluştur (rapor adı + tarih)
        tarih_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        dosya_adi = f"{rapor_adi}_{tarih_str}.xlsx"
        
        # Kayıt yerini kullanıcıdan al
        dosya_yolu, _ = QFileDialog.getSaveFileName(
            self, "Raporu Kaydet", dosya_adi, "Excel Dosyaları (*.xlsx)"
        )
        
        if not dosya_yolu:
            return  # Kullanıcı iptal etti
        
        try:
            # Excel dosyasını oluştur
            self._excel_olustur(dosya_yolu, rapor_adi)
            
            # Ayrıca gecmis klasörüne de bir kopya kaydet
            gecmis_klasoru = "gecmis"
            if not os.path.exists(gecmis_klasoru):
                os.makedirs(gecmis_klasoru)
            
            gecmis_dosya_yolu = os.path.join(gecmis_klasoru, os.path.basename(dosya_yolu))
            
            # Eğer seçilen konum zaten gecmis klasörü değilse, kopyala
            if os.path.normpath(os.path.dirname(dosya_yolu)) != os.path.normpath(gecmis_klasoru):
                shutil.copy2(dosya_yolu, gecmis_dosya_yolu)
            
            QMessageBox.information(self, "Başarılı", f"Rapor başarıyla kaydedildi:\n{dosya_yolu}")
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Rapor kaydedilirken bir hata oluştu:\n{str(e)}")
    
    def _excel_olustur(self, dosya_yolu, rapor_adi):
        """Excel dosyasını oluşturur."""
        # Tablodaki verileri al
        veri = []
        for row in range(self.maliyet_raporu.tablo.rowCount()):
            kategori = self.maliyet_raporu.tablo.item(row, 0).text()
            parca = self.maliyet_raporu.tablo.item(row, 1).text()
            birim_fiyat_text = self.maliyet_raporu.tablo.item(row, 2).text()
            toplam_fiyat_text = self.maliyet_raporu.tablo.item(row, 3).text()
            
            # Fiyatları sayıya çevir
            try:
                birim_fiyat = float(birim_fiyat_text.replace("TL", "").strip())
                toplam_fiyat = float(toplam_fiyat_text.replace("TL", "").strip())
            except:
                birim_fiyat = 0.0
                toplam_fiyat = 0.0
            
            # Parça adından fiyat bilgisini çıkar
            parca_adi = parca.split("(")[0].strip() if "(" in parca else parca
            
            # Parça sayısını belirle
            parca_sayisi = self.maliyet_raporu.parca_sayilari.get(kategori, 1)
            
            veri.append([kategori, parca_adi, birim_fiyat, parca_sayisi, toplam_fiyat])
        
        # DataFrame oluştur
        df = pd.DataFrame(veri, columns=["Alt Kategori", "Parça Adı", "Birim Fiyat (TL)", "Adet", "Toplam Fiyat (TL)"])
        
        # Toplam maliyet hesapla
        toplam_maliyet = df["Toplam Fiyat (TL)"].sum()
        
        # Excel dosyasına kaydet
        with pd.ExcelWriter(dosya_yolu, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Maliyet Raporu", index=False)
            
            # Toplam maliyet bilgisini ekle
            workbook = writer.book
            worksheet = writer.sheets["Maliyet Raporu"]
            
            # Toplam satırı ekle
            son_satir = len(df) + 2  # Başlık satırı ve boş satır için +2
            worksheet.cell(row=son_satir, column=1, value="TOPLAM")
            worksheet.cell(row=son_satir, column=5, value=toplam_maliyet)
            
            # Rapor adı ve tarih bilgisini ekle
            worksheet.cell(row=son_satir+2, column=1, value=f"Rapor Adı: {rapor_adi}")
            worksheet.cell(row=son_satir+3, column=1, value=f"Oluşturma Tarihi: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}") 