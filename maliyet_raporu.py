from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                            QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from datetime import datetime

class MaliyetRaporu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Güncelleme butonu
        self.guncelle_btn = QPushButton("Fiyatları Güncelle")
        self.guncelle_btn.clicked.connect(self.fiyat_guncelle)
        layout.addWidget(self.guncelle_btn)
        
        # Son güncelleme zamanı
        self.guncelleme_label = QLabel("Son Güncelleme: -")
        layout.addWidget(self.guncelleme_label)
        
        # Tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(3)
        self.tablo.setHorizontalHeaderLabels(["Parça", "Birim Fiyat", "Toplam"])
        layout.addWidget(self.tablo)
        
        # Toplam maliyet etiketi
        self.toplam_label = QLabel()
        self.toplam_label.setAlignment(Qt.AlignRight)
        self.toplam_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.toplam_label)
    
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