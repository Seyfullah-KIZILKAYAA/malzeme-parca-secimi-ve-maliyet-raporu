from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
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
        self.setup_ui()
        self.setup_toaster_model()
        
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
        self.ax.view_init(elev=elev, azim=azim)
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
        
    def goster_gorsel(self, gorsel_yolu=None):
        # This method is kept for compatibility with the original interface
        # but now it doesn't use image files
        pass
        
    def update_part_visibility(self, part_name, visible=True):
        if part_name in self.parts:
            self.parts[part_name]['visible'] = visible
            
            # Update the visibility of the corresponding collection
            if part_name in self.collections:
                self.collections[part_name].set_visible(visible)
            else:
                # Create the collection if it doesn't exist
                vertices = self.parts[part_name]['vertices']
                faces = self.parts[part_name]['faces']
                polygons = []
                
                for face in faces:
                    polygon = [vertices[i] for i in face]
                    polygons.append(polygon)
                
                collection = Poly3DCollection(polygons, alpha=0.9)
                collection.set_facecolor(self.parts[part_name]['color'])
                collection.set_edgecolor('black')
                collection.set_visible(visible)
                
                self.ax.add_collection3d(collection)
                self.collections[part_name] = collection
            
            self.canvas.draw_idle()
    
    def update_model_from_selection(self, secili_parcalar):
        # Update the model based on selected parts
        self.secili_parcalar = secili_parcalar
        
        # Map selected parts to 3D model parts
        for alt_kategori, parca_bilgisi in secili_parcalar.items():
            parca_adi = parca_bilgisi["parca_adi"]
            
            # Extract the base part name from the part name (remove price info)
            base_part_name = parca_adi.split('(')[0].strip()
            
            # Try to find a matching part in our 3D model
            matching_part = None
            for part_name in self.parts:
                if part_name.lower() in alt_kategori.lower() or alt_kategori.lower() in part_name.lower():
                    matching_part = part_name
                    break
            
            if matching_part:
                self.update_part_visibility(matching_part, True)
                
                # Special case for bread
                if "ekmek" in alt_kategori.lower() or "ekmek" in parca_adi.lower():
                    self.update_part_visibility("Ekmek_Sol", True)
                    self.update_part_visibility("Ekmek_Sag", True)
        
        self.canvas.draw_idle()
        
    def reset_model(self):
        # Hide all parts
        for part_name in self.parts:
            if part_name in self.collections:
                self.collections[part_name].set_visible(False)
                self.parts[part_name]['visible'] = False
        
        self.canvas.draw_idle() 