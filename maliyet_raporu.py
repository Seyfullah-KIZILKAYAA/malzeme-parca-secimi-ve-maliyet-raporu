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
        self.layout.setContentsMargins(10, 15, 10, 15)  # Kenar boşluklarını artır
        self.layout.setSpacing(15)  # Bileşenler arası boşluğu artır
        
        # Başlık etiketi
        self.baslik_label = QLabel("Maliyet Raporu")
        self.baslik_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; padding: 5px;")
        self.layout.addWidget(self.baslik_label)
        
        # Parça listesi için tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(3)
        self.tablo.setHorizontalHeaderLabels(["Alt Kategori", "Seçilen Parça", "Fiyat"])
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
        self.tablo.setMinimumWidth(500)   # Tablo minimum genişliğini ayarla
        
        # Sütun genişliklerini ayarla
        header = self.tablo.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)  # Alt Kategori sütunu
        header.setSectionResizeMode(1, QHeaderView.Stretch)      # Seçilen Parça sütunu
        header.setSectionResizeMode(2, QHeaderView.Interactive)  # Fiyat sütunu
        
        # Sütun genişliklerini başlangıç için ayarla
        self.tablo.setColumnWidth(0, 150)  # Alt Kategori sütunu genişliği
        self.tablo.setColumnWidth(2, 100)  # Fiyat sütunu genişliği
        
        # Satır yüksekliğini artır ve metni sarma özelliğini etkinleştir
        self.tablo.verticalHeader().setDefaultSectionSize(40)
        self.tablo.setWordWrap(True)
        
        self.layout.addWidget(self.tablo)
        
        # Maliyet bilgileri için bir çerçeve
        maliyet_frame = QWidget()
        maliyet_frame.setStyleSheet("background-color: #f9f9f9; border-radius: 5px; padding: 10px;")
        maliyet_layout = QVBoxLayout(maliyet_frame)
        
        # Toplam maliyet göstergesi
        self.toplam_label = QLabel("Toplam Maliyet: 0 TL")
        self.toplam_label.setStyleSheet("font-style: italic; font-size: 15px; padding: 5px; color: #555;")
        maliyet_layout.addWidget(self.toplam_label)
        
        # Tahmini maliyet aralığı göstergesi
        self.tahmini_label = QLabel("Tahmini Maliyet Aralığı: 0 TL - 0 TL")
        self.tahmini_label.setStyleSheet("font-style: italic; font-size: 15px; padding: 5px; color: #555;")
        maliyet_layout.addWidget(self.tahmini_label)
        
        self.layout.addWidget(maliyet_frame)
        
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
            
            # Fiyat
            fiyat_item = QTableWidgetItem(f"{bilgi['fiyat']} TL")
            fiyat_item.setFlags(fiyat_item.flags() & ~Qt.ItemIsEditable)
            fiyat_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tablo.setItem(row, 2, fiyat_item)
            
            toplam_maliyet += bilgi["fiyat"]
        
        # Satır yüksekliklerini içeriğe göre otomatik ayarla
        for row in range(self.tablo.rowCount()):
            self.tablo.resizeRowToContents(row)
        
        # Toplam maliyeti güncelle
        self.toplam_label.setText(f"Toplam Maliyet: {toplam_maliyet:.2f} TL")
        
        # Tahmini maliyet aralığını güncelle (toplam maliyetin 500 TL altı ve üstü)
        alt_sinir = max(0, toplam_maliyet - 500)
        ust_sinir = toplam_maliyet + 500
        self.tahmini_label.setText(f"Tahmini Maliyet Aralığı: {alt_sinir:.2f} TL - {ust_sinir:.2f} TL")
        
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
        
        # Tahmini maliyet aralığını güncelle (toplam maliyetin 500 TL altı ve üstü)
        alt_sinir = max(0, toplam_maliyet - 500)
        ust_sinir = toplam_maliyet + 500
        self.tahmini_label.setText(f"Tahmini Maliyet Aralığı: {alt_sinir:,.2f} TL - {ust_sinir:,.2f} TL") 