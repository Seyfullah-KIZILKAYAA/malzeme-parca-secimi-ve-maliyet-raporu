from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                            QPushButton, QLabel, QMessageBox, QHeaderView, QFileDialog)
from PyQt5.QtCore import Qt
from datetime import datetime
import pandas as pd
import os

class MaliyetRaporu(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        # Parça sayıları sözlüğü - her parça kategorisi için tipik sayılar
        self.parca_sayilari = {
            # Ana Gövde ve Mekanik Parçalar
            "Dis_Govde": 1,
            "Ic_Govde_Kaplamasi": 1,
            "Kapak_Mentesesi": 2,
            "Kapak_Yaylari": 2,
            "Tutma_Kolu": 1,
            "Kilitleme_Mandali": 1,
            "Cihaz_Ayaklari": 4,
            "Havalandirma_Delikleri": 1,
            "Yag_Toplama_Haznesi": 1,
            
            # Isıtma ve Elektrik Aksamı
            "Rezistans": 2,
            "Rezistans_Baglanti_Uclari": 4,
            "Rezistans_Sabitleme_Vidalari": 8,
            "Termostat": 1,
            "Termostat_Baglanti_Kablolari": 2,
            "Plaka_Baglanti_Elemanlari": 4,
            "Elektrik_Kablosu": 1,
            "Ic_Elektrik_Devresi": 1,
            "Topraklama_Kablosu": 1,
            
            # Kontrol ve Kullanıcı Arayüzü
            "Ana_Acma_Kapama_Dugmesi": 1,
            "Gosterge_Isiklari": 2,
            "Gosterge_Isigi_Yuvasi": 2,
            "Dugme_Yaylari": 3,
            "Sicaklik_Ayar_Dugmesi": 1,
            "Zamanlayici_Dugmesi": 1,
            
            # Isıtma Plakaları ve Yüzey Kaplamaları
            "Ust_Izgara_Plakasi": 1,
            "Alt_Izgara_Plakasi": 1,
            "Plaka_Kaplamasi": 2,
            "Plaka_Tutturma_Vidalari": 8,
            
            # Güvenlik ve Destek Parçaları
            "Isiya_Dayanikli_Plastik_Parcalar": 4,
            "Ic_Yalitim_Malzemesi": 2,
            "Sigorta": 1,
            "Topraklama_Plakasi": 1,
            
            # Vidalar, Civatalar ve Küçük Parçalar
            "Kapak_Mentese_Vidalari": 4,
            "Rezistans_Sabitleme_Vidalari": 8,
            "Plaka_Sabitleme_Vidalari": 8,
            "Govde_Montaj_Vidalari": 12,
            "Elektrik_Devresi_Lehimleri": 10,
            "Dugme_Yaylari": 3,
            "Termostat_Baglanti_Elemanlari": 2,
            
            # Ekstra Parçalar
            "Degistirilebilir_Plakalar": 2
        }
        
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 15)  # Kenar boşluklarını artır
        self.layout.setSpacing(15)  # Bileşenler arası boşluğu artır
        
        # Başlık etiketi
        self.baslik_label = QLabel("Maliyet Raporu")
        self.baslik_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; padding: 5px;")
        self.layout.addWidget(self.baslik_label)
        
        # Parça listesi için tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(4)  # 4 sütun: Alt Kategori, Seçilen Parça, Birim Fiyat, Toplam Fiyat
        self.tablo.setHorizontalHeaderLabels(["Alt Kategori", "Seçilen Parça", "Birim Fiyat", "Toplam Fiyat"])
        self.tablo.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                gridline-color: #d0d0d0;
                border: 1px solid #c0c0c0;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 6px;
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #c0c0c0;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        self.tablo.setMinimumHeight(250)  # Tablo yüksekliğini artır
        self.tablo.setMinimumWidth(600)   # Tablo minimum genişliğini artır
        
        # Sütun genişliklerini ayarla
        header = self.tablo.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)  # Alt Kategori sütunu
        header.setSectionResizeMode(1, QHeaderView.Stretch)      # Seçilen Parça sütunu
        header.setSectionResizeMode(2, QHeaderView.Interactive)  # Birim Fiyat sütunu
        header.setSectionResizeMode(3, QHeaderView.Interactive)  # Toplam Fiyat sütunu
        
        # Sütun genişliklerini başlangıç için ayarla
        self.tablo.setColumnWidth(0, 150)  # Alt Kategori sütunu genişliği
        self.tablo.setColumnWidth(2, 100)  # Birim Fiyat sütunu genişliği
        self.tablo.setColumnWidth(3, 100)  # Toplam Fiyat sütunu genişliği
        
        # Satır yüksekliğini artır ve metni sarma özelliğini etkinleştir
        self.tablo.verticalHeader().setDefaultSectionSize(40)
        self.tablo.setWordWrap(True)
        
        self.layout.addWidget(self.tablo)
        
        # Maliyet bilgileri için bir çerçeve
        maliyet_frame = QWidget()
        maliyet_frame.setStyleSheet("background-color: #f9f9f9; border-radius: 5px; padding: 10px;")
        maliyet_layout = QVBoxLayout(maliyet_frame)
        
        # Toplam maliyet göstergesi (gizli)
        self.toplam_label = QLabel("Toplam Maliyet: 0 TL")
        self.toplam_label.setStyleSheet("font-style: italic; font-size: 15px; padding: 5px; color: #555;")
        self.toplam_label.setVisible(False)  # Toplam maliyeti gizle
        maliyet_layout.addWidget(self.toplam_label)
        
        # Tahmini maliyet aralığı göstergesi
        self.tahmini_label = QLabel("Tahmini Maliyet Aralığı: 0 TL - 0 TL")
        self.tahmini_label.setStyleSheet("font-style: italic; font-size: 15px; padding: 5px; color: #555;")
        maliyet_layout.addWidget(self.tahmini_label)
        
        self.layout.addWidget(maliyet_frame)
        
        # Excel'e kaydetme butonu
        self.excel_button = QPushButton("Maliyet Raporunu Excel'e Kaydet")
        self.excel_button.setStyleSheet("""
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
        self.excel_button.clicked.connect(self.excel_kaydet)
        self.layout.addWidget(self.excel_button)
        
    def guncelle_parcalar(self, secili_parcalar):
        self.tablo.setRowCount(len(secili_parcalar))
        toplam_maliyet = 0
        
        for row, (kategori, bilgi) in enumerate(secili_parcalar.items()):
            # Alt kategori
            kategori_item = QTableWidgetItem(kategori)
            kategori_item.setFlags(kategori_item.flags() & ~Qt.ItemIsEditable)
            kategori_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.tablo.setItem(row, 0, kategori_item)
            
            # Seçilen parça
            parca_item = QTableWidgetItem(bilgi["parca_adi"])
            parca_item.setFlags(parca_item.flags() & ~Qt.ItemIsEditable)
            parca_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.tablo.setItem(row, 1, parca_item)
            
            # Toplam fiyat
            toplam_fiyat = bilgi["fiyat"]
            toplam_fiyat_item = QTableWidgetItem(f"{toplam_fiyat:.2f} TL")
            toplam_fiyat_item.setFlags(toplam_fiyat_item.flags() & ~Qt.ItemIsEditable)
            toplam_fiyat_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tablo.setItem(row, 3, toplam_fiyat_item)
            
            # Birim fiyat
            parca_sayisi = self.parca_sayilari.get(kategori, 1)
            if parca_sayisi > 0:
                birim_fiyat = toplam_fiyat / parca_sayisi
            else:
                birim_fiyat = 0.0
            
            birim_fiyat_item = QTableWidgetItem(f"{birim_fiyat:.2f} TL")
            birim_fiyat_item.setFlags(birim_fiyat_item.flags() & ~Qt.ItemIsEditable)
            birim_fiyat_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tablo.setItem(row, 2, birim_fiyat_item)
            
            toplam_maliyet += toplam_fiyat
        
        # Satır yüksekliklerini içeriğe göre otomatik ayarla
        for row in range(self.tablo.rowCount()):
            self.tablo.resizeRowToContents(row)
        
        # Toplam maliyeti güncelle (gizli)
        self.toplam_label.setText(f"Toplam Maliyet: {toplam_maliyet:.2f} TL")
        
        # Tahmini maliyet aralığını güncelle (toplam maliyetin 500 TL altı ve üstü)
        alt_sinir = max(0, toplam_maliyet - 500)
        ust_sinir = toplam_maliyet + 500
        self.tahmini_label.setText(f"Tahmini Maliyet Aralığı: {alt_sinir:.2f} TL - {ust_sinir:.2f} TL")
        
        self.tablo.sortItems(0)  # Alt kategorilere göre sırala
        
    def excel_kaydet(self):
        """Maliyet raporunu Excel dosyasına kaydeder."""
        try:
            # Tablodaki verileri al
            veri = []
            for row in range(self.tablo.rowCount()):
                kategori = self.tablo.item(row, 0).text()
                parca = self.tablo.item(row, 1).text()
                birim_fiyat_text = self.tablo.item(row, 2).text()
                toplam_fiyat_text = self.tablo.item(row, 3).text()
                
                # Fiyatları sayıya çevir
                try:
                    birim_fiyat = float(birim_fiyat_text.replace("TL", "").strip())
                    toplam_fiyat = float(toplam_fiyat_text.replace("TL", "").strip())
                except:
                    birim_fiyat = 0.0
                    toplam_fiyat = 0.0
                
                # Parça adından fiyat bilgisini çıkar
                parca_adi = parca.split("(")[0].strip()
                
                # Parça sayısını belirle
                parca_sayisi = self.parca_sayilari.get(kategori, 1)
                
                veri.append([kategori, parca_adi, birim_fiyat, parca_sayisi, toplam_fiyat])
            
            # Veri yoksa uyarı ver
            if not veri:
                QMessageBox.warning(self, "Uyarı", "Kaydedilecek veri bulunamadı!")
                return
            
            # Toplam maliyet ve tahmini maliyet aralığı bilgilerini al
            toplam_maliyet = self.toplam_label.text()
            tahmini_aralik = self.tahmini_label.text()
            
            # Dosya kaydetme diyaloğunu göster
            dosya_adi, _ = QFileDialog.getSaveFileName(
                self, 
                "Excel Dosyasını Kaydet", 
                os.path.expanduser("~/Desktop/Maliyet_Raporu.xlsx"),
                "Excel Dosyaları (*.xlsx)"
            )
            
            if not dosya_adi:  # Kullanıcı iptal ettiyse
                return
            
            # Pandas DataFrame oluştur
            df = pd.DataFrame(veri, columns=["Alt Kategori", "Seçilen Parça", "Birim Fiyat (TL)", "Parça Sayısı", "Toplam Fiyat (TL)"])
            
            # Excel dosyasına yaz
            with pd.ExcelWriter(dosya_adi, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Maliyet Raporu', index=False)
                
                # Çalışma kitabını al
                workbook = writer.book
                worksheet = writer.sheets['Maliyet Raporu']
                
                # Sütun genişliklerini ayarla
                worksheet.column_dimensions['A'].width = 20  # Alt Kategori
                worksheet.column_dimensions['B'].width = 40  # Seçilen Parça
                worksheet.column_dimensions['C'].width = 15  # Birim Fiyat
                worksheet.column_dimensions['D'].width = 12  # Parça Sayısı
                worksheet.column_dimensions['E'].width = 18  # Toplam Fiyat
                
                # Toplam maliyet ve tahmini maliyet aralığı bilgilerini ekle
                son_satir = len(veri) + 2
                worksheet.cell(row=son_satir, column=1, value=toplam_maliyet)
                worksheet.cell(row=son_satir+1, column=1, value=tahmini_aralik)
                
                # Genel toplam maliyeti hesapla ve ekle
                genel_toplam = sum(item[4] for item in veri)
                worksheet.cell(row=son_satir+2, column=1, value=f"Genel Toplam Maliyet: {genel_toplam:.2f} TL")
            
            QMessageBox.information(self, "Başarılı", f"Maliyet raporu başarıyla kaydedildi:\n{dosya_adi}")
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Excel dosyası kaydedilirken bir hata oluştu:\n{str(e)}")

    def fiyat_guncelle(self):
        try:
            # Parça verilerini yeniden yükle
            self.parent().parca_verileri = self.parent().parca_verileri.__class__()
            self.guncelleme_label.setText(
                f"Son Güncelleme: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            )
            QMessageBox.information(self, "Başarılı", "Fiyatlar güncellendi.")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Güncelleme hatası: {str(e)}")

    def guncelle_rapor(self, parca_detaylari, secili_parcalar, secili_alt_parca=None):
        self.tablo.setRowCount(0)
        toplam_maliyet = 0
        
        for parca, detay in parca_detaylari.items():
            if parca in secili_parcalar:
                maliyet = detay.get("maliyet", {})
                for alt_parca, fiyat in maliyet.items():
                    if secili_alt_parca is None or alt_parca == secili_alt_parca:
                        row = self.tablo.rowCount()
                        self.tablo.insertRow(row)
                        
                        # Alt parça
                        self.tablo.setItem(row, 0, QTableWidgetItem(alt_parca))
                        
                        # Toplam fiyat
                        toplam_fiyat_item = QTableWidgetItem(f"{fiyat:,.2f} TL")
                        toplam_fiyat_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        self.tablo.setItem(row, 3, toplam_fiyat_item)
                        
                        # Birim fiyat
                        parca_sayisi = self.parca_sayilari.get(alt_parca, 1)
                        if parca_sayisi > 0:
                            birim_fiyat = fiyat / parca_sayisi
                        else:
                            birim_fiyat = 0.0
                        
                        birim_fiyat_item = QTableWidgetItem(f"{birim_fiyat:,.2f} TL")
                        birim_fiyat_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        self.tablo.setItem(row, 2, birim_fiyat_item)
                        
                        toplam_maliyet += fiyat
        
        # Toplam maliyeti güncelle (gizli)
        self.toplam_label.setText(f"Toplam Maliyet: {toplam_maliyet:,.2f} TL")
        
        # Tahmini maliyet aralığını güncelle (toplam maliyetin 500 TL altı ve üstü)
        alt_sinir = max(0, toplam_maliyet - 500)
        ust_sinir = toplam_maliyet + 500
        self.tahmini_label.setText(f"Tahmini Maliyet Aralığı: {alt_sinir:,.2f} TL - {ust_sinir:,.2f} TL") 