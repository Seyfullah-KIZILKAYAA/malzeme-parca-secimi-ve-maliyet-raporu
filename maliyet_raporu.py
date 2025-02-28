from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                            QPushButton, QLabel, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt
from datetime import datetime

class MaliyetRaporu(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        
        # Parça listesi için tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(3)
        self.tablo.setHorizontalHeaderLabels(["Alt Kategori", "Seçilen Parça", "Fiyat"])
        header = self.tablo.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.layout.addWidget(self.tablo)
        
        # Toplam maliyet göstergesi
        self.toplam_label = QLabel("Toplam Maliyet: 0 TL")
        self.toplam_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 10px;")
        self.layout.addWidget(self.toplam_label)
        
    def guncelle_parcalar(self, secili_parcalar):
        self.tablo.setRowCount(len(secili_parcalar))
        toplam_maliyet = 0
        
        for row, (kategori, bilgi) in enumerate(secili_parcalar.items()):
            # Alt kategori
            kategori_item = QTableWidgetItem(kategori)
            kategori_item.setFlags(kategori_item.flags() & ~Qt.ItemIsEditable)
            self.tablo.setItem(row, 0, kategori_item)
            
            # Seçilen parça
            parca_item = QTableWidgetItem(bilgi["parca_adi"])
            parca_item.setFlags(parca_item.flags() & ~Qt.ItemIsEditable)
            self.tablo.setItem(row, 1, parca_item)
            
            # Fiyat
            fiyat_item = QTableWidgetItem(f"{bilgi['fiyat']} TL")
            fiyat_item.setFlags(fiyat_item.flags() & ~Qt.ItemIsEditable)
            self.tablo.setItem(row, 2, fiyat_item)
            
            toplam_maliyet += bilgi["fiyat"]
            
        self.toplam_label.setText(f"Toplam Maliyet: {toplam_maliyet:.2f} TL")
        self.tablo.sortItems(0)  # Alt kategorilere göre sırala

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
                        self.tablo.setItem(row, 0, QTableWidgetItem(alt_parca))
                        self.tablo.setItem(row, 1, QTableWidgetItem(f"{fiyat:,.2f} TL"))
                        toplam_maliyet += fiyat
        
        # Toplam maliyeti güncelle
        self.toplam_label.setText(f"Toplam Maliyet: {toplam_maliyet:,.2f} TL") 