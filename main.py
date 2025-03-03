import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                            QVBoxLayout, QComboBox, QLabel, QRadioButton, 
                            QButtonGroup, QFrame, QSplitter, QScrollArea, QPushButton, QTabWidget)
from PyQt5.QtCore import Qt
from parca_listesi import ParcaVerileri
from gorsel_gosterici import GorselGosterici
from maliyet_raporu import MaliyetRaporu
from db_connection import DatabaseConnection
from rapor_goruntule import RaporGoruntule
from detayli_maliyet_raporu import DetayliMaliyetRaporu

class TostMakinesiUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tost Makinesi Parçaları Kataloğu")
        self.setGeometry(100, 100, 1800, 800)
        
        self.parca_verileri = ParcaVerileri()
        self.secili_parcalar = {}  # {alt_kategori: {"parca_adi": str, "fiyat": float}}
        self.db = DatabaseConnection(
            server=r".\SQLEXPRESS",
            database="MALZEME_LIST",
            username="sa",
            password="Password1"
        )
        self.setup_ui()
        
    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Sol panel (parça seçimi)
        left_frame = QFrame()
        left_frame.setFrameStyle(QFrame.StyledPanel)
        left_frame.setMinimumWidth(300)
        left_layout = QVBoxLayout(left_frame)
        
        # Parça seçim alanı için grup
        secim_grup = QFrame()
        secim_layout = QVBoxLayout(secim_grup)
        
        # Ana Kategori
        secim_layout.addWidget(QLabel("Ana Kategori:"))
        self.ana_combo = QComboBox()
        self.ana_combo.addItems(self.parca_verileri.ana_kategoriler)
        self.ana_combo.currentIndexChanged.connect(self.ana_kategori_secildi)
        secim_layout.addWidget(self.ana_combo)
        
        # Alt Kategori
        secim_layout.addWidget(QLabel("Alt Kategori:"))
        self.alt_combo = QComboBox()
        self.alt_combo.currentIndexChanged.connect(self.alt_kategori_secildi)
        secim_layout.addWidget(self.alt_combo)
        
        # Radio butonlar için scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(300)
        radio_widget = QWidget()
        self.radio_layout = QVBoxLayout(radio_widget)
        self.radio_layout.setSpacing(2)
        self.radio_layout.setContentsMargins(5, 5, 5, 5)
        self.radio_layout.setAlignment(Qt.AlignTop)
        radio_widget.setStyleSheet("""
            QWidget {
                background-color: white;
            }
            QRadioButton {
                margin: 1px;
                padding: 1px;
                height: 20px;
                spacing: 5px;
                border: none;
            }
        """)
        scroll.setWidget(radio_widget)
        
        # Radio buton başlığı
        radio_baslik = QLabel("Parça Seçimi:")
        radio_baslik.setStyleSheet("""
            font-weight: bold;
            margin-top: 10px;
        """)
        secim_layout.addWidget(radio_baslik)
        secim_layout.addWidget(scroll)
        
        # Radio buton grubu
        self.radio_group = QButtonGroup()
        self.radio_group.buttonClicked.connect(self.parca_secildi)
        
        # Tüm seçimleri kaldır butonu
        self.reset_button = QPushButton("Tüm Seçimleri Kaldır")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 4px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.reset_button.clicked.connect(self.tum_secimleri_kaldir)
        secim_layout.addWidget(self.reset_button)
        
        # Seçim grubunu sol frame'e ekle
        left_layout.addWidget(secim_grup)
        
        # Sol frame'i ana layout'a ekle
        layout.addWidget(left_frame)
        
        # Orta panel (görsel)
        self.gorsel_gosterici = GorselGosterici()
        self.gorsel_gosterici.setMinimumWidth(800)
        layout.addWidget(self.gorsel_gosterici, 2)
        
        # Sağ panel (maliyet raporu ve kayıtlı raporlar)
        right_frame = QFrame()
        right_frame.setFrameStyle(QFrame.StyledPanel)
        right_frame.setMinimumWidth(400)
        right_layout = QVBoxLayout(right_frame)
        
        # Tab widget oluştur
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                background: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #f0f0f0;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
            }
            QTabBar::tab:hover {
                background: #e0e0e0;
            }
        """)
        
        # Maliyet raporu
        self.maliyet_raporu = MaliyetRaporu()
        self.maliyet_raporu.set_main_window(self)  # Ana pencere referansını ayarla
        self.tab_widget.addTab(self.maliyet_raporu, "Maliyet Raporu")
        
        # Kayıtlı raporlar sekmesi
        self.rapor_goruntule = RaporGoruntule()
        self.tab_widget.addTab(self.rapor_goruntule, "Kayıtlı Raporlar")
        
        right_layout.addWidget(self.tab_widget)
        
        # Detaylı Maliyet Raporu butonu
        self.detayli_rapor_btn = QPushButton("Detaylı Maliyet Raporu")
        self.detayli_rapor_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 4px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.detayli_rapor_btn.clicked.connect(self.detayli_rapor_goster)
        right_layout.addWidget(self.detayli_rapor_btn)
        
        # Sağ frame'i ana layout'a ekle
        layout.addWidget(right_frame)
        
        # İlk kategoriyi göster
        self.ana_kategori_secildi(0)
    
    def tum_secimleri_kaldir(self):
        # Tüm seçimleri temizle
        self.secili_parcalar = {}
        
        # Radio butonların seçimini kaldır
        for button in self.radio_group.buttons():
            button.setChecked(False)
        
        # 3D modeli sıfırla
        self.gorsel_gosterici.reset_model()
        
        # Maliyet raporunu güncelle
        self.maliyet_raporu.guncelle_parcalar(self.secili_parcalar)
    
    def ana_kategori_secildi(self, index):
        # Alt kategorileri güncelle
        self.alt_combo.clear()
        if index in self.parca_verileri.alt_kategoriler:
            self.alt_combo.addItems(self.parca_verileri.alt_kategoriler[index])
            self.alt_combo.setCurrentIndex(0)
            self.alt_kategori_secildi(0)
    
    def alt_kategori_secildi(self, index):
        # Radio butonları temizle
        for button in self.radio_group.buttons():
            self.radio_layout.removeWidget(button)
            button.deleteLater()
        
        # Seçilen alt kategoriye göre parçaları SQL'den çek ve radio buton olarak ekle
        secilen_kategori = self.alt_combo.currentText()
        try:
            parca_detaylari = self.parca_verileri.get_parcalar(secilen_kategori)
            
            if parca_detaylari and "parcalar" in parca_detaylari:
                for parca in parca_detaylari["parcalar"]:
                    radio = QRadioButton(parca)
                    radio.setStyleSheet("""
                        QRadioButton {
                            margin: 1px;
                            padding: 1px;
                            height: 20px;
                            spacing: 5px;
                            border: none;
                        }
                    """)
                    self.radio_group.addButton(radio)
                    self.radio_layout.addWidget(radio, 0, Qt.AlignTop)
                    
                    # Eğer bu alt kategori için daha önce seçim yapıldıysa, o seçimi işaretle
                    if secilen_kategori in self.secili_parcalar and self.secili_parcalar[secilen_kategori]["parca_adi"] == parca:
                        radio.setChecked(True)
                
                # 3D modeli güncelle
                self.gorsel_gosterici.update_model_from_selection(self.secili_parcalar)
                
                # Maliyet raporunu güncelle
                self.maliyet_raporu.guncelle_parcalar(self.secili_parcalar)
            else:
                # Eğer parça bulunamazsa bilgi mesajı göster
                radio = QRadioButton("Bu kategoride parça bulunamadı")
                radio.setEnabled(False)
                self.radio_layout.addWidget(radio)
                
        except Exception as e:
            print(f"Parçalar yüklenirken hata: {str(e)}")
            # Hata durumunda kullanıcıya bilgi ver
            radio = QRadioButton("Parçalar yüklenirken hata oluştu")
            radio.setEnabled(False)
            self.radio_layout.addWidget(radio)
    
    def parca_secildi(self, button):
        secilen_kategori = self.alt_combo.currentText()
        if secilen_kategori in self.parca_verileri.parca_detaylari:
            parca_adi = button.text()
            
            # Fiyatı güvenli bir şekilde al
            try:
                # Parantez içindeki son TL değerini bul
                fiyat_str = parca_adi.split('(')[-1].split(')')[0]
                # TL'yi kaldır ve sayıya çevir
                fiyat = float(fiyat_str.replace('TL', '').strip())
            except (ValueError, IndexError):
                print(f"Fiyat çıkarılamadı: {parca_adi}")
                fiyat = 0.0
            
            # Seçilen parçayı kaydet
            self.secili_parcalar[secilen_kategori] = {
                "parca_adi": parca_adi,
                "fiyat": fiyat
            }
            
            # 3D modeli güncelle
            self.gorsel_gosterici.update_model_from_selection(self.secili_parcalar)
            
            # Maliyet raporunu güncelle
            self.maliyet_raporu.guncelle_parcalar(self.secili_parcalar)
            
            # Bir sonraki alt kategoriye geç
            current_index = self.alt_combo.currentIndex()
            if current_index < self.alt_combo.count() - 1:
                self.alt_combo.setCurrentIndex(current_index + 1)
            elif self.ana_combo.currentIndex() < self.ana_combo.count() - 1:
                # Eğer son alt kategorideysek ve başka ana kategori varsa
                self.ana_combo.setCurrentIndex(self.ana_combo.currentIndex() + 1)

    def detayli_rapor_goster(self):
        """Detaylı maliyet raporu penceresini gösterir"""
        detayli_rapor = DetayliMaliyetRaporu(self.secili_parcalar)
        detayli_rapor.exec_()  # show() yerine exec_() kullan

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TostMakinesiUygulamasi()
    window.show()
    sys.exit(app.exec_()) 