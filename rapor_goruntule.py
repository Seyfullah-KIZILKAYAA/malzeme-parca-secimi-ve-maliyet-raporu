from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, 
                            QFileDialog, QInputDialog, QLineEdit, QDialog, QFormLayout, QHBoxLayout,
                            QListWidget, QListWidgetItem, QTableWidget, QHeaderView, QTableWidgetItem, QStyle)
from PyQt5.QtCore import Qt
from datetime import datetime
import pandas as pd
import os
import shutil
from rapor_karsilastirma import RaporKarsilastirma
from PyQt5.QtWidgets import QApplication

class RaporGoruntule(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Arayüz bileşenlerini oluşturur."""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 15)
        self.layout.setSpacing(15)
        
        # Başlık etiketi
        self.baslik_label = QLabel("Kayıtlı Raporlar")
        self.baslik_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; padding: 5px;")
        self.layout.addWidget(self.baslik_label)
        
        # Rapor listesi
        self.liste = QListWidget()
        self.liste.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e0e0e0;
                color: black;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
        """)
        self.liste.setSelectionMode(QListWidget.ExtendedSelection)  # Çoklu seçime izin ver
        self.layout.addWidget(self.liste)
        
        # Butonlar için yatay düzen
        buton_layout = QHBoxLayout()
        
        # Raporu aç butonu
        self.ac_button = QPushButton("Raporu Aç")
        self.ac_button.setStyleSheet("""
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
        self.ac_button.clicked.connect(self.raporu_ac)
        buton_layout.addWidget(self.ac_button)
        
        # Raporu sil butonu
        self.sil_button = QPushButton("Raporu Sil")
        self.sil_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
        """)
        self.sil_button.clicked.connect(self.raporu_sil)
        buton_layout.addWidget(self.sil_button)
        
        # Raporları karşılaştır butonu
        self.karsilastir_button = QPushButton("Raporları Karşılaştır")
        self.karsilastir_button.setStyleSheet("""
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
                background-color: #1565C0;
            }
        """)
        self.karsilastir_button.clicked.connect(self.raporlari_karsilastir)
        buton_layout.addWidget(self.karsilastir_button)
        
        # Listeyi yenile butonu
        self.yenile_button = QPushButton("Listeyi Yenile")
        self.yenile_button.setStyleSheet("""
            QPushButton {
                background-color: #9E9E9E;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #757575;
            }
            QPushButton:pressed {
                background-color: #616161;
            }
        """)
        self.yenile_button.clicked.connect(self.raporlari_listele)
        buton_layout.addWidget(self.yenile_button)
        
        self.layout.addLayout(buton_layout)
        
        # Raporları listele
        self.raporlari_listele()
        
    def raporlari_listele(self):
        """Kayıtlı raporları listeler."""
        self.liste.clear()
        
        # Geçmiş klasörünü kontrol et
        gecmis_klasoru = "gecmis"
        if not os.path.exists(gecmis_klasoru):
            os.makedirs(gecmis_klasoru)
            self.liste.addItem("Henüz kaydedilmiş rapor bulunmamaktadır.")
            return
        
        # Excel dosyalarını bul
        excel_dosyalari = [f for f in os.listdir(gecmis_klasoru) if f.endswith('.xlsx')]
        
        if not excel_dosyalari:
            self.liste.addItem("Henüz kaydedilmiş rapor bulunmamaktadır.")
            return
        
        # Dosyaları tarihe göre sırala (en yeni en üstte)
        excel_dosyalari.sort(reverse=True)
        
        # Listeye ekle
        for dosya in excel_dosyalari:
            # Dosya adından rapor adını ve tarihini çıkar
            try:
                rapor_adi = dosya.split('_')[0]
                tarih_str = '_'.join(dosya.split('_')[1:]).replace('.xlsx', '')
                tarih_obj = datetime.strptime(tarih_str, "%Y%m%d_%H%M%S")
                tarih_gosterim = tarih_obj.strftime("%d/%m/%Y %H:%M:%S")
                
                self.liste.addItem(f"{rapor_adi} - {tarih_gosterim}")
            except:
                # Hata durumunda dosya adını olduğu gibi göster
                self.liste.addItem(dosya)
    
    def raporu_ac(self):
        """Seçili raporu açar ve görüntüler."""
        secili_item = self.liste.currentItem()
        if not secili_item:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir rapor seçin.")
            return
        
        # Seçili öğeden dosya adını belirle
        secili_metin = secili_item.text()
        
        if secili_metin == "Henüz kaydedilmiş rapor bulunmamaktadır.":
            return
        
        try:
            # Dosya adını oluştur
            rapor_adi = secili_metin.split(' - ')[0]
            tarih_str = secili_metin.split(' - ')[1]
            tarih_obj = datetime.strptime(tarih_str, "%d/%m/%Y %H:%M:%S")
            dosya_tarih = tarih_obj.strftime("%Y%m%d_%H%M%S")
            dosya_adi = f"{rapor_adi}_{dosya_tarih}.xlsx"
            dosya_yolu = os.path.join("gecmis", dosya_adi)
            
            # Excel dosyasını pandas ile oku
            df = pd.read_excel(dosya_yolu)
            
            # Yeni dialog penceresi oluştur
            rapor_pencere = QDialog(self)
            rapor_pencere.setWindowTitle(f"Rapor: {rapor_adi}")
            rapor_pencere.setMinimumSize(800, 400)
            rapor_layout = QVBoxLayout(rapor_pencere)
            
            # Tablo oluştur
            tablo = QTableWidget()
            tablo.setColumnCount(len(df.columns))
            tablo.setRowCount(len(df))
            tablo.setHorizontalHeaderLabels(df.columns)
            
            # Verileri tabloya ekle
            for i in range(len(df)):
                for j in range(len(df.columns)):
                    item = QTableWidgetItem(str(df.iloc[i, j]))
                    tablo.setItem(i, j, item)
            
            # Tablo ayarları
            tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tablo.setStyleSheet("""
                QTableWidget {
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    background-color: white;
                    gridline-color: #eee;
                }
                QHeaderView::section {
                    background-color: #f8f9fa;
                    padding: 4px;
                    border: none;
                    border-bottom: 1px solid #ddd;
                }
            """)
            
            rapor_layout.addWidget(tablo)
            
            # Kapat butonu ekle
            kapat_btn = QPushButton("Kapat")
            kapat_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            kapat_btn.clicked.connect(rapor_pencere.close)
            rapor_layout.addWidget(kapat_btn)
            
            # Pencereyi göster
            rapor_pencere.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Rapor açılırken bir hata oluştu:\n{str(e)}")
    
    def raporu_sil(self):
        """Seçili raporu siler."""
        secili_item = self.liste.currentItem()
        if not secili_item:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir rapor seçin.")
            return
        
        # Seçili öğeden dosya adını belirle
        secili_metin = secili_item.text()
        
        if secili_metin == "Henüz kaydedilmiş rapor bulunmamaktadır.":
            return
        
        # Onay iste
        cevap = QMessageBox.question(self, "Onay", f"'{secili_metin}' raporunu silmek istediğinize emin misiniz?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if cevap != QMessageBox.Yes:
            return
        
        # Dosya adını oluştur
        try:
            rapor_adi = secili_metin.split(' - ')[0]
            tarih_str = secili_metin.split(' - ')[1]
            tarih_obj = datetime.strptime(tarih_str, "%d/%m/%Y %H:%M:%S")
            dosya_tarih = tarih_obj.strftime("%Y%m%d_%H%M%S")
            dosya_adi = f"{rapor_adi}_{dosya_tarih}.xlsx"
        except:
            # Hata durumunda tüm excel dosyalarını kontrol et
            gecmis_klasoru = "gecmis"
            excel_dosyalari = [f for f in os.listdir(gecmis_klasoru) if f.endswith('.xlsx')]
            
            # Seçili metni içeren dosyayı bul
            for dosya in excel_dosyalari:
                if rapor_adi in dosya:
                    dosya_adi = dosya
                    break
            else:
                QMessageBox.warning(self, "Hata", "Rapor dosyası bulunamadı.")
                return
        
        dosya_yolu = os.path.join("gecmis", dosya_adi)
        
        # Dosyanın varlığını kontrol et
        if not os.path.exists(dosya_yolu):
            QMessageBox.warning(self, "Hata", f"Rapor dosyası bulunamadı:\n{dosya_yolu}")
            return
        
        try:
            # Dosyayı sil
            os.remove(dosya_yolu)
            QMessageBox.information(self, "Başarılı", "Rapor başarıyla silindi.")
            
            # Listeyi güncelle
            self.raporlari_listele()
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Rapor silinirken bir hata oluştu:\n{str(e)}")
    
    def raporlari_karsilastir(self):
        """Seçili raporları karşılaştırır."""
        secili_itemler = self.liste.selectedItems()
        
        if len(secili_itemler) != 2:
            QMessageBox.warning(self, "Uyarı", "Lütfen karşılaştırmak için tam olarak 2 rapor seçin.")
            return
        
        # Seçili raporların dosya yollarını bul
        dosya_yollari = []
        for item in secili_itemler:
            secili_metin = item.text()
            
            if secili_metin == "Henüz kaydedilmiş rapor bulunmamaktadır.":
                return
            
            try:
                rapor_adi = secili_metin.split(' - ')[0]
                tarih_str = secili_metin.split(' - ')[1]
                tarih_obj = datetime.strptime(tarih_str, "%d/%m/%Y %H:%M:%S")
                dosya_tarih = tarih_obj.strftime("%Y%m%d_%H%M%S")
                dosya_adi = f"{rapor_adi}_{dosya_tarih}.xlsx"
                dosya_yolu = os.path.join("gecmis", dosya_adi)
                
                if not os.path.exists(dosya_yolu):
                    QMessageBox.warning(self, "Hata", f"Rapor dosyası bulunamadı:\n{dosya_yolu}")
                    return
                
                dosya_yollari.append(dosya_yolu)
                
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Rapor dosyası işlenirken hata oluştu:\n{str(e)}")
                return
        
        # Karşılaştırma penceresini aç
        karsilastirma = RaporKarsilastirma(dosya_yollari[0], dosya_yollari[1])
        karsilastirma.exec_() 