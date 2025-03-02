from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as mcolors

class GorselGosterici(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel)
        self.secili_parcalar = {}
        self.onceki_parcalar = {}  # Önceki seçili parçaları saklamak için
        self.yanip_sonen_parcalar = set()  # Yanıp sönen parçaları takip etmek için
        self.flash_count = 0  # Yanıp sönme sayacı
        
        # Yanıp sönme için timer
        self.flash_timer = QTimer()
        self.flash_timer.timeout.connect(self.flash_effect)
        
        self.setup_ui()
        self.setup_toaster_model()
        
        # Performans iyileştirmesi için fare olaylarını bağla
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.mouse_pressed = False
        self.last_x = 0
        self.last_y = 0
        
    def on_mouse_press(self, event):
        """Fare basıldığında çağrılır"""
        if event.button == 1:  # Sol fare tuşu
            self.mouse_pressed = True
            self.last_x = event.xdata if event.xdata else 0
            self.last_y = event.ydata if event.ydata else 0
    
    def on_mouse_release(self, event):
        """Fare bırakıldığında çağrılır"""
        if event.button == 1:  # Sol fare tuşu
            self.mouse_pressed = False
    
    def on_mouse_move(self, event):
        """Fare hareket ettiğinde çağrılır"""
        if self.mouse_pressed and event.xdata and event.ydata:
            # Fare hareketine göre görünümü döndür
            dx = event.xdata - self.last_x
            dy = event.ydata - self.last_y
            
            # Mevcut görünüm açılarını al
            current_elev, current_azim = self.ax.elev, self.ax.azim
            
            # Yeni açıları hesapla (daha hassas hareket için katsayıları ayarla)
            new_azim = current_azim + dx * 2.0
            new_elev = current_elev - dy * 2.0
            
            # Açıları sınırla
            new_elev = max(-90, min(90, new_elev))
            
            # Görünümü güncelle
            self.ax.view_init(elev=new_elev, azim=new_azim)
            
            # Son konumu güncelle
            self.last_x = event.xdata
            self.last_y = event.ydata
            
            # Sadece ekranı yenile, tüm çizimi yeniden yapma
            self.canvas.draw_idle()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title label
        title_label = QLabel("3D Tost Makinesi Modeli")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Create matplotlib figure and canvas
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(600, 400)
        layout.addWidget(self.canvas)
        
        # Create 3D axes
        self.ax = self.figure.add_subplot(111, projection='3d')
        
        # Set viewing angle and limits
        self.ax.view_init(elev=30, azim=45)
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_zlim(-1, 10)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        
        # Performans iyileştirmeleri
        self.figure.tight_layout()
        self.ax.set_box_aspect([1, 1, 1.2])  # Daha iyi oran
        
        # Görünüm kalitesini artır
        self.ax.set_facecolor('#f0f0f0')  # Arka plan rengi
        
        # Performans için eksen çizgilerini basitleştir
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.xaxis.pane.set_edgecolor('lightgrey')
        self.ax.yaxis.pane.set_edgecolor('lightgrey')
        self.ax.zaxis.pane.set_edgecolor('lightgrey')
        self.ax.grid(False)  # Izgara çizgilerini kapat
        
        # Fare ile döndürme talimatı
        mouse_label = QLabel("Modeli döndürmek için fareyi sürükleyin")
        mouse_label.setAlignment(Qt.AlignCenter)
        mouse_label.setStyleSheet("font-style: italic; color: #666;")
        layout.addWidget(mouse_label)
        
        # Add view control buttons
        view_layout = QHBoxLayout()
        
        # Front view button
        front_btn = QPushButton("Ön Görünüm")
        front_btn.clicked.connect(lambda: self.change_view(0, 0))
        view_layout.addWidget(front_btn)
        
        # Side view button
        side_btn = QPushButton("Yan Görünüm")
        side_btn.clicked.connect(lambda: self.change_view(0, 90))
        view_layout.addWidget(side_btn)
        
        # Top view button
        top_btn = QPushButton("Üst Görünüm")
        top_btn.clicked.connect(lambda: self.change_view(90, 0))
        view_layout.addWidget(top_btn)
        
        # Isometric view button
        iso_btn = QPushButton("İzometrik Görünüm")
        iso_btn.clicked.connect(lambda: self.change_view(30, 45))
        view_layout.addWidget(iso_btn)
        
        layout.addLayout(view_layout)
        
    def change_view(self, elev, azim):
        # Görünümü değiştir
        self.ax.view_init(elev=elev, azim=azim)
        
        # Görünümü yenile - daha hızlı yenileme için
        self.canvas.draw_idle()
        
    def setup_toaster_model(self):
        # Define toaster parts with more detail
        self.parts = {
            'Dis_Govde': {
                'vertices': np.array([
                    [-4, -3, 0], [4, -3, 0], [4, 3, 0], [-4, 3, 0],  # bottom
                    [-4, -3, 2], [4, -3, 2], [4, 3, 2], [-4, 3, 2],  # top
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # bottom, top
                    [0, 1, 5, 4], [1, 2, 6, 5],  # sides
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ],
                'color': '#C0C0C0',  # Silver
                'visible': False
            },
            'Ic_Govde_Kaplamasi': {
                'vertices': np.array([
                    [-3.8, -2.8, 0.2], [3.8, -2.8, 0.2], [3.8, 2.8, 0.2], [-3.8, 2.8, 0.2],  # bottom
                    [-3.8, -2.8, 1.8], [3.8, -2.8, 1.8], [3.8, 2.8, 1.8], [-3.8, 2.8, 1.8],  # top
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # bottom, top
                    [0, 1, 5, 4], [1, 2, 6, 5],  # sides
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ],
                'color': '#A9A9A9',  # Dark gray
                'visible': False
            },
            'Ust_Izgara_Plakasi': {
                'vertices': np.array([
                    [-3.5, -2.5, 2], [3.5, -2.5, 2], [3.5, 2.5, 2], [-3.5, 2.5, 2],  # bottom
                    [-3.5, -2.5, 2.2], [3.5, -2.5, 2.2], [3.5, 2.5, 2.2], [-3.5, 2.5, 2.2],  # top
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # bottom, top
                    [0, 1, 5, 4], [1, 2, 6, 5],  # sides
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ],
                'color': '#8B0000',  # Dark red
                'visible': False
            },
            'Alt_Izgara_Plakasi': {
                'vertices': np.array([
                    [-3.5, -2.5, 0.5], [3.5, -2.5, 0.5], [3.5, 2.5, 0.5], [-3.5, 2.5, 0.5],  # bottom
                    [-3.5, -2.5, 0.7], [3.5, -2.5, 0.7], [3.5, 2.5, 0.7], [-3.5, 2.5, 0.7],  # top
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # bottom, top
                    [0, 1, 5, 4], [1, 2, 6, 5],  # sides
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ],
                'color': '#8B0000',  # Dark red
                'visible': False
            },
            'Kapak_Mentesesi': {
                'vertices': np.array([
                    [-4, 3, 2], [-3.8, 3, 2], [-3.8, 3, 6], [-4, 3, 6],  # left hinge
                    [3.8, 3, 2], [4, 3, 2], [4, 3, 6], [3.8, 3, 6],  # right hinge
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # hinges
                ],
                'color': '#808080',  # Gray
                'visible': False
            },
            'Kapak_Yaylari': {
                'vertices': np.array([
                    [-3.9, 3, 2.2], [-3.9, 3, 5.8], [-3.9, 3.2, 5.8], [-3.9, 3.2, 2.2],  # left spring
                    [3.9, 3, 2.2], [3.9, 3, 5.8], [3.9, 3.2, 5.8], [3.9, 3.2, 2.2],  # right spring
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # springs
                ],
                'color': '#A9A9A9',  # Dark gray
                'visible': False
            },
            'Tutma_Kolu': {
                'vertices': np.array([
                    [-1, 3, 4], [1, 3, 4], [1, 3.5, 4], [-1, 3.5, 4],  # handle base
                    [-1, 3, 3.8], [1, 3, 3.8], [1, 3.5, 3.8], [-1, 3.5, 3.8],  # handle bottom
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # handle faces
                    [0, 1, 5, 4], [1, 2, 6, 5],  # sides
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ],
                'color': '#000000',  # Black
                'visible': False
            },
            'Ana_Acma_Kapama_Dugmesi': {
                'vertices': np.array([
                    [-3.5, -3, 1], [-2.5, -3, 1], [-2.5, -3, 1.5], [-3.5, -3, 1.5],  # button face
                    [-3.5, -3.2, 1], [-2.5, -3.2, 1], [-2.5, -3.2, 1.5], [-3.5, -3.2, 1.5],  # button back
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # front, back
                    [0, 1, 5, 4], [1, 2, 6, 5],  # sides
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ],
                'color': '#FF0000',  # Red
                'visible': False
            },
            'Sicaklik_Ayar_Dugmesi': {
                'vertices': np.array([
                    [-2, -3, 1], [-1, -3, 1], [-1, -3, 1.5], [-2, -3, 1.5],  # button face
                    [-2, -3.2, 1], [-1, -3.2, 1], [-1, -3.2, 1.5], [-2, -3.2, 1.5],  # button back
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # front, back
                    [0, 1, 5, 4], [1, 2, 6, 5],  # sides
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ],
                'color': '#0000FF',  # Blue
                'visible': False
            },
            'Rezistans': {
                'vertices': np.array([
                    [-3, -2, 1], [3, -2, 1], [3, 2, 1], [-3, 2, 1],  # bottom resistor
                    [-3, -2, 1.8], [3, -2, 1.8], [3, 2, 1.8], [-3, 2, 1.8],  # top resistor
                ]),
                'faces': [
                    [0, 1, 5, 4], [1, 2, 6, 5],  # sides
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ],
                'color': '#FF4500',  # Orange-red
                'visible': False
            },
            'Elektrik_Kablosu': {
                'vertices': np.array([
                    [-4, -3, 0.5], [-4, -3.5, 0.5], [-4, -3.5, 1], [-4, -3, 1],  # cable start
                    [-4, -5, 0.5], [-4, -5, 1],  # cable end
                    [-4.2, -5, 0.5], [-4.2, -5, 1],  # plug width
                    [-4.2, -5.5, 0.5], [-4.2, -5.5, 1],  # plug length
                    [-4, -5.5, 0.5], [-4, -5.5, 1],  # plug other side
                ]),
                'faces': [
                    [0, 1, 2, 3], [1, 4, 5, 2],  # cable
                    [4, 6, 7, 5], [6, 8, 9, 7],  # plug
                    [8, 10, 11, 9], [10, 4, 5, 11]  # plug end
                ],
                'color': '#000000',  # Black
                'visible': False
            },
            'Cihaz_Ayaklari': {
                'vertices': np.array([
                    [-3.5, -2.5, 0], [-3, -2.5, 0], [-3, -2.5, -0.3], [-3.5, -2.5, -0.3],  # foot 1
                    [3, -2.5, 0], [3.5, -2.5, 0], [3.5, -2.5, -0.3], [3, -2.5, -0.3],  # foot 2
                    [-3.5, 2.5, 0], [-3, 2.5, 0], [-3, 2.5, -0.3], [-3.5, 2.5, -0.3],  # foot 3
                    [3, 2.5, 0], [3.5, 2.5, 0], [3.5, 2.5, -0.3], [3, 2.5, -0.3],  # foot 4
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15],  # feet
                ],
                'color': '#000000',  # Black
                'visible': False
            },
            'Kapak': {
                'vertices': np.array([
                    [-4, 3, 2], [4, 3, 2], [4, 3, 6], [-4, 3, 6],  # inner face
                    [-4, 4, 2], [4, 4, 2], [4, 4, 6], [-4, 4, 6],  # outer face
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # faces
                    [0, 1, 5, 4], [1, 2, 6, 5],  # sides
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ],
                'color': '#C0C0C0',  # Silver
                'visible': False
            },
            'Ekmek_Sol': {
                'vertices': np.array([
                    [-3, -1.5, 2.2], [-1.5, -1.5, 2.2], [-1.5, 1.5, 2.2], [-3, 1.5, 2.2],  # bottom
                    [-3, -1.5, 4], [-1.5, -1.5, 4], [-1.5, 1.5, 4], [-3, 1.5, 4],  # top
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # bottom, top
                    [0, 1, 5, 4], [1, 2, 6, 5],  # sides
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ],
                'color': '#DEB887',  # Burlywood
                'visible': False
            },
            'Ekmek_Sag': {
                'vertices': np.array([
                    [1.5, -1.5, 2.2], [3, -1.5, 2.2], [3, 1.5, 2.2], [1.5, 1.5, 2.2],  # bottom
                    [1.5, -1.5, 4], [3, -1.5, 4], [3, 1.5, 4], [1.5, 1.5, 4],  # top
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # bottom, top
                    [0, 1, 5, 4], [1, 2, 6, 5],  # sides
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ],
                'color': '#DEB887',  # Burlywood
                'visible': False
            },
            'Termostat': {
                'vertices': np.array([
                    [-0.5, -2.8, 0.8], [0.5, -2.8, 0.8], [0.5, -2.5, 0.8], [-0.5, -2.5, 0.8],  # bottom
                    [-0.5, -2.8, 1.2], [0.5, -2.8, 1.2], [0.5, -2.5, 1.2], [-0.5, -2.5, 1.2],  # top
                ]),
                'faces': [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # bottom, top
                    [0, 1, 5, 4], [1, 2, 6, 5],  # sides
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ],
                'color': '#4682B4',  # Steel blue
                'visible': False
            },
            'Ic_Elektrik_Devresi': {
                'vertices': np.array([
                    [-3, -2.5, 0.3], [-1, -2.5, 0.3], [-1, -1.5, 0.3], [-3, -1.5, 0.3],  # circuit board
                ]),
                'faces': [
                    [0, 1, 2, 3],  # board
                ],
                'color': '#006400',  # Dark green
                'visible': False
            }
        }
        
        # Create collections to store the 3D polygons
        self.collections = {}
        
        # Tüm parçaları önceden oluştur ama görünmez yap
        self._create_all_parts()
        
    def _create_all_parts(self):
        """Tüm parçaları önceden oluştur ama görünmez yap"""
        # Performans için önce tüm parçaları temizle
        for collection in self.collections.values():
            if collection in self.ax.collections:
                collection.remove()
        self.collections = {}
        
        # Parçaları oluştur
        for part_name, part_info in self.parts.items():
            vertices = part_info['vertices']
            faces = part_info['faces']
            polygons = []
            
            for face in faces:
                polygon = [vertices[i] for i in face]
                polygons.append(polygon)
            
            # Daha iyi görünüm için ayarlar
            collection = Poly3DCollection(
                polygons, 
                alpha=0.95,  # Biraz şeffaflık
                linewidths=0.5,  # İnce kenarlar
                edgecolors='black',
                antialiaseds=True  # Kenarları yumuşat
            )
            collection.set_facecolor(part_info['color'])
            collection.set_visible(False)
            
            # Performans için z-order ayarı
            collection.set_sort_zpos(0)  # Z-sıralama için sabit değer
            
            self.ax.add_collection3d(collection)
            self.collections[part_name] = collection
        
        # Görünümü yenile
        self.canvas.draw_idle()
        
    def goster_gorsel(self, gorsel_yolu=None):
        # This method is kept for compatibility with the original interface
        # but now it doesn't use image files
        pass
        
    def update_part_visibility(self, part_name, visible=True):
        """Parçanın görünürlüğünü güncelle"""
        if part_name in self.parts:
            self.parts[part_name]['visible'] = visible
            
            if part_name in self.collections:
                self.collections[part_name].set_visible(visible)
            
        self.canvas.draw_idle()
    
    def update_model_from_selection(self, secili_parcalar):
        # Değişen parçaları belirle
        degisen_parcalar = set()
        for alt_kategori, parca_bilgisi in secili_parcalar.items():
            if alt_kategori not in self.onceki_parcalar or self.onceki_parcalar[alt_kategori] != parca_bilgisi:
                degisen_parcalar.add(alt_kategori)
        
        # Update the model based on selected parts
        self.secili_parcalar = secili_parcalar.copy()
        
        # Önce tüm parçaları gizle
        for part_name in self.parts:
            if part_name in self.collections:
                self.collections[part_name].set_visible(False)
                self.collections[part_name].set_sort_zpos(0)
            self.parts[part_name]['visible'] = False
        
        # Yanıp sönecek parçaları belirle
        self.yanip_sonen_parcalar.clear()
        
        # Map selected parts to 3D model parts
        for alt_kategori, parca_bilgisi in secili_parcalar.items():
            parca_adi = parca_bilgisi["parca_adi"]
            
            # Alt kategori ve parça adını küçük harfe çevir
            alt_kategori_lower = alt_kategori.lower().replace("_", " ")
            parca_adi_lower = parca_adi.split('(')[0].strip().lower()
            
            # Try to find a matching part in our 3D model
            for part_name in self.parts:
                part_name_lower = part_name.lower().replace("_", " ")
                
                # Eğer parça adı alt kategori veya seçilen parça adı ile eşleşiyorsa
                if (part_name_lower in alt_kategori_lower or 
                    alt_kategori_lower in part_name_lower or
                    part_name_lower in parca_adi_lower or
                    parca_adi_lower in part_name_lower):
                    
                    self.parts[part_name]['visible'] = True
                    if part_name in self.collections:
                        collection = self.collections[part_name]
                        collection.set_visible(True)
                        # Parçanın orijinal rengini ayarla
                        collection.set_facecolor(self.parts[part_name]['color'])
                        # Eğer bu parça değiştiyse, yanıp sönme listesine ekle
                        if alt_kategori in degisen_parcalar:
                            self.yanip_sonen_parcalar.add(part_name)
            
            # Special case for bread
            if "ekmek" in alt_kategori_lower or "ekmek" in parca_adi_lower:
                for bread_part in ["Ekmek_Sol", "Ekmek_Sag"]:
                    self.parts[bread_part]['visible'] = True
                    if bread_part in self.collections:
                        collection = self.collections[bread_part]
                        collection.set_visible(True)
                        # Ekmek parçalarının orijinal rengini ayarla
                        collection.set_facecolor(self.parts[bread_part]['color'])
                        if alt_kategori in degisen_parcalar:
                            self.yanip_sonen_parcalar.add(bread_part)
        
        # Yanıp sönme efektini başlat
        if self.yanip_sonen_parcalar:
            self.flash_count = 0
            if hasattr(self, 'flash_timer'):
                self.flash_timer.stop()  # Varolan timer'ı durdur
            self.flash_timer = QTimer()
            self.flash_timer.timeout.connect(self.flash_effect)
            self.flash_timer.start(500)  # Her 500ms'de bir yanıp sönme
            # İlk yanıp sönmeyi hemen başlat
            self.flash_effect()
        
        # Önceki parçaları güncelle
        self.onceki_parcalar = secili_parcalar.copy()
        
        # Görünümü yenile
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    
    def flash_effect(self):
        """Yanıp sönme efektini uygula"""
        self.flash_count += 1
        
        # Yanıp sönen parçaların rengini değiştir
        for part_name in self.yanip_sonen_parcalar:
            if part_name in self.collections:
                collection = self.collections[part_name]
                if self.flash_count % 2 == 0:
                    # Normal renk
                    collection.set_facecolor(self.parts[part_name]['color'])
                else:
                    # Altın sarısı renk
                    collection.set_facecolor('#FFD700')  # Altın sarısı
                
                # Görünürlüğü zorla
                collection.set_visible(True)
                
                # Z-order'ı güncelle
                collection.set_sort_zpos(10 if self.flash_count % 2 == 1 else 0)
        
        # Axes'i yenile
        self.ax.set_title(f"Yanıp Sönme: {self.flash_count//2 + 1}/6", pad=10)
        
        # Görünümü yenile
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        
        # 6 kez yanıp söndükten sonra durdur (12 renk değişimi)
        if self.flash_count >= 12:
            self.flash_timer.stop()
            # Son olarak normal renklere döndür
            for part_name in self.yanip_sonen_parcalar:
                if part_name in self.collections:
                    self.collections[part_name].set_facecolor(self.parts[part_name]['color'])
                    self.collections[part_name].set_visible(True)
                    self.collections[part_name].set_sort_zpos(0)
            
            self.ax.set_title("")
            self.figure.canvas.draw()
            self.figure.canvas.flush_events()
    
    def reset_model(self):
        # Timer'ı durdur
        self.flash_timer.stop()
        
        # Tüm parçaları gizle
        for part_name in self.parts:
            if part_name in self.collections:
                self.collections[part_name].set_visible(False)
                self.collections[part_name].set_facecolor(self.parts[part_name]['color'])
            self.parts[part_name]['visible'] = False
        
        # Yanıp sönen parçaları temizle
        self.yanip_sonen_parcalar.clear()
        
        # Önceki parçaları temizle
        self.onceki_parcalar.clear()
        
        # Görünümü yenile
        self.canvas.draw_idle() 