from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os

class GorselGosterici(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.gorsel_label = QLabel()
        self.gorsel_label.setAlignment(Qt.AlignCenter)
        self.gorsel_label.setMinimumSize(600, 400)
        self.gorsel_label.setStyleSheet("background-color: white;")
        layout.addWidget(self.gorsel_label)
        
    def goster_gorsel(self, gorsel_yolu):
        if gorsel_yolu and os.path.exists(gorsel_yolu):
            pixmap = QPixmap(gorsel_yolu)
            scaled_pixmap = pixmap.scaled(
                self.gorsel_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.gorsel_label.setPixmap(scaled_pixmap)
        else:
            self.gorsel_label.setText("Görsel bulunamadı") 