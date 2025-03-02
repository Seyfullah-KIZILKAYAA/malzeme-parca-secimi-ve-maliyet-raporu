from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QMessageBox, QDialog, QScrollArea, QFrame)
from PyQt5.QtCore import Qt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import seaborn as sns
import os
from datetime import datetime

class RaporKarsilastirma(QDialog):
    def __init__(self, rapor1_yolu, rapor2_yolu):
        super().__init__()
        self.rapor1_yolu = rapor1_yolu
        self.rapor2_yolu = rapor2_yolu
        self.setWindowTitle("Rapor Karşılaştırma")
        self.setGeometry(100, 100, 1200, 800)
        
        # Matplotlib'in Türkçe karakter desteği için
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['figure.autolayout'] = True
        
        # Stil ayarları
        plt.style.use('bmh')
        sns.set_style("whitegrid")
        
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Başlık için frame
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 1px solid #ddd;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        
        # Başlık
        baslik = QLabel("Rapor Karşılaştırma Analizi")
        baslik.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        title_layout.addWidget(baslik)
        
        main_layout.addWidget(title_frame)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
        """)
        
        # İçerik widget'ı
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: white;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(30)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        try:
            # Dosyaların varlığını kontrol et
            if not os.path.exists(self.rapor1_yolu) or not os.path.exists(self.rapor2_yolu):
                raise FileNotFoundError("Karşılaştırılacak raporlardan biri veya her ikisi bulunamadı.")

            # Raporları oku
            try:
                df1 = pd.read_excel(self.rapor1_yolu)
                df2 = pd.read_excel(self.rapor2_yolu)
            except Exception as e:
                raise Exception(f"Excel dosyaları okunurken hata oluştu: {str(e)}")

            # Gerekli sütunların varlığını kontrol et
            required_columns = ['Alt Kategori', 'Parça Adı', 'Toplam Fiyat (TL)']
            for col in required_columns:
                if col not in df1.columns or col not in df2.columns:
                    raise ValueError(f"'{col}' sütunu bir veya her iki raporda eksik.")

            # NaN değerleri temizle
            df1 = df1.dropna(subset=['Alt Kategori', 'Parça Adı', 'Toplam Fiyat (TL)'])
            df2 = df2.dropna(subset=['Alt Kategori', 'Parça Adı', 'Toplam Fiyat (TL)'])

            # Veri varlığını kontrol et
            if df1.empty or df2.empty:
                raise ValueError("Bir veya her iki rapor boş veri içeriyor.")
            
            # Rapor isimlerini al
            rapor1_adi = os.path.basename(self.rapor1_yolu).split('_')[0]
            rapor2_adi = os.path.basename(self.rapor2_yolu).split('_')[0]
            
            # Özet bilgiler için frame
            ozet_frame = QFrame()
            ozet_frame.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                }
            """)
            ozet_layout = QVBoxLayout(ozet_frame)
            
            # Özet başlık
            ozet_label = QLabel("Özet Karşılaştırma")
            ozet_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            ozet_layout.addWidget(ozet_label)
            
            # Toplam maliyetleri karşılaştır
            toplam1 = df1['Toplam Fiyat (TL)'].sum()
            toplam2 = df2['Toplam Fiyat (TL)'].sum()
            fark = toplam2 - toplam1
            
            ozet_text = QLabel(f"""
            {rapor1_adi}: {toplam1:,.2f} TL
            {rapor2_adi}: {toplam2:,.2f} TL
            Fark: {abs(fark):,.2f} TL ({rapor2_adi} {'daha pahalı' if fark > 0 else 'daha ucuz'})
            """)
            ozet_text.setStyleSheet("""
                font-family: monospace;
                font-size: 14px;
                padding: 10px;
            """)
            ozet_layout.addWidget(ozet_text)
            
            content_layout.addWidget(ozet_frame)
            
            # Grafikler için frame'ler
            def create_graph_frame(title):
                frame = QFrame()
                frame.setStyleSheet("""
                    QFrame {
                        background-color: white;
                        border: 1px solid #dee2e6;
                        border-radius: 5px;
                    }
                """)
                layout = QVBoxLayout(frame)
                layout.setContentsMargins(10, 10, 10, 10)
                
                title_label = QLabel(title)
                title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #495057;")
                layout.addWidget(title_label)
                
                return frame, layout
            
            try:
                # Kategori karşılaştırma grafiği
                cat_frame, cat_layout = create_graph_frame("Kategori Bazlı Maliyet Karşılaştırması")
                self.create_category_comparison(cat_layout, df1, df2, rapor1_adi, rapor2_adi)
                content_layout.addWidget(cat_frame)
            except Exception as e:
                error_label = QLabel(f"Kategori karşılaştırması oluşturulurken hata: {str(e)}")
                error_label.setStyleSheet("color: red; padding: 10px;")
                content_layout.addWidget(error_label)
            
            try:
                # Parça karşılaştırma grafiği
                part_frame, part_layout = create_graph_frame("En Büyük Fiyat Farklılığı Olan Parçalar")
                self.create_part_comparison(part_layout, df1, df2, rapor1_adi, rapor2_adi)
                content_layout.addWidget(part_frame)
            except Exception as e:
                error_label = QLabel(f"Parça karşılaştırması oluşturulurken hata: {str(e)}")
                error_label.setStyleSheet("color: red; padding: 10px;")
                content_layout.addWidget(error_label)
            
            try:
                # Pasta grafikleri
                pie_frame, pie_layout = create_graph_frame("Maliyet Dağılımı")
                self.create_pie_charts(pie_layout, df1, df2, rapor1_adi, rapor2_adi)
                content_layout.addWidget(pie_frame)
            except Exception as e:
                error_label = QLabel(f"Pasta grafikleri oluşturulurken hata: {str(e)}")
                error_label.setStyleSheet("color: red; padding: 10px;")
                content_layout.addWidget(error_label)
            
        except Exception as e:
            error_label = QLabel(f"Hata oluştu: {str(e)}")
            error_label.setStyleSheet("""
                color: red;
                padding: 20px;
                background-color: #fff3cd;
                border: 1px solid #ffeeba;
                border-radius: 4px;
                margin: 10px;
            """)
            content_layout.addWidget(error_label)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # Kapat butonu için frame
        button_frame = QFrame()
        button_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-top: 1px solid #ddd;
            }
        """)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(10, 10, 10, 10)
        
        # Kapat butonu
        kapat_btn = QPushButton("Kapat")
        kapat_btn.setFixedWidth(120)
        kapat_btn.clicked.connect(self.close)
        kapat_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                font-weight: bold;
                padding: 8px 15px;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        button_layout.addWidget(kapat_btn, alignment=Qt.AlignRight)
        
        main_layout.addWidget(button_frame)

    def create_category_comparison(self, layout, df1, df2, rapor1_adi, rapor2_adi):
        try:
            # Kategori bazlı toplam maliyetler
            cat1 = df1[df1['Alt Kategori'].notna()].groupby('Alt Kategori')['Toplam Fiyat (TL)'].sum()
            cat2 = df2[df2['Alt Kategori'].notna()].groupby('Alt Kategori')['Toplam Fiyat (TL)'].sum()
            
            if cat1.empty and cat2.empty:
                raise ValueError("Her iki raporda da kategori verisi bulunamadı.")
            
            # Tüm kategorileri birleştir
            tum_kategoriler = sorted(set(cat1.index) | set(cat2.index))
            
            if not tum_kategoriler:
                raise ValueError("Karşılaştırılacak kategori bulunamadı.")
            
            # Ana frame oluştur
            main_frame = QFrame()
            main_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                    margin-bottom: 10px;
                }
            """)
            main_layout = QVBoxLayout(main_frame)
            main_layout.setSpacing(20)
            
            # Her kategori için grafik oluştur
            for kategori in tum_kategoriler:
                try:
                    # Kategori frame'i oluştur
                    cat_frame = QFrame()
                    cat_frame.setStyleSheet("""
                        QFrame {
                            background-color: #f8f9fa;
                            border: 1px solid #e9ecef;
                            border-radius: 5px;
                            margin: 5px;
                            padding: 5px;
                        }
                    """)
                    cat_layout = QVBoxLayout(cat_frame)
                    cat_layout.setContentsMargins(10, 10, 10, 10)
                    
                    # Kategori başlığı
                    baslik = QLabel(f"{kategori} Karşılaştırması")
                    baslik.setStyleSheet("""
                        font-size: 14px;
                        font-weight: bold;
                        color: #495057;
                        padding: 5px;
                        background-color: white;
                        border-radius: 3px;
                    """)
                    cat_layout.addWidget(baslik)
                    
                    # Değerleri al
                    deger1 = float(cat1[kategori] if kategori in cat1.index else 0)
                    deger2 = float(cat2[kategori] if kategori in cat2.index else 0)
                    
                    if deger1 == 0 and deger2 == 0:
                        continue
                    
                    # Grafik oluştur
                    plt.close('all')
                    fig, ax = plt.subplots(figsize=(8, 3))
                    
                    # Çubuk grafik
                    x = np.arange(2)
                    width = 0.35
                    
                    rects1 = ax.bar(x[0], deger1, width, label=rapor1_adi, color='#007bff')
                    rects2 = ax.bar(x[1], deger2, width, label=rapor2_adi, color='#28a745')
                    
                    # Grafik ayarları
                    ax.set_xticks(x)
                    ax.set_xticklabels([rapor1_adi, rapor2_adi])
                    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
                    ax.set_axisbelow(True)
                    
                    # Değerleri çubukların üzerine yaz
                    def autolabel(rect, value):
                        try:
                            height = float(value)
                            ax.annotate(f'{height:,.0f} TL',
                                      xy=(rect.get_x() + rect.get_width() / 2, height),
                                      xytext=(0, 3),
                                      textcoords="offset points",
                                      ha='center', va='bottom',
                                      fontsize=9,
                                      weight='bold')
                        except Exception:
                            pass
                    
                    autolabel(rects1[0], deger1)
                    autolabel(rects2[0], deger2)
                    
                    # Fark yüzdesini göster
                    if deger1 != 0:
                        try:
                            fark_yuzde = ((deger2 - deger1) / deger1) * 100
                            fark_text = f"Fark: %{abs(fark_yuzde):.1f} {'artış' if fark_yuzde > 0 else 'azalış'}"
                            ax.text(0.5, 1.05, fark_text,
                                  ha='center', va='bottom',
                                  transform=ax.transAxes,
                                  fontsize=9,
                                  color='#dc3545' if fark_yuzde > 0 else '#28a745')
                        except Exception:
                            pass
                    
                    plt.tight_layout()
                    
                    # Canvas oluştur ve ekle
                    canvas = FigureCanvas(fig)
                    canvas.setMinimumHeight(200)
                    cat_layout.addWidget(canvas)
                    
                    # Değerleri tablo olarak göster
                    degerler_text = QLabel(f"""
                    {rapor1_adi}: {deger1:,.2f} TL
                    {rapor2_adi}: {deger2:,.2f} TL
                    Fark: {abs(deger2 - deger1):,.2f} TL
                    """)
                    degerler_text.setStyleSheet("""
                        font-family: monospace;
                        font-size: 12px;
                        padding: 5px;
                        background-color: white;
                        border-radius: 3px;
                    """)
                    cat_layout.addWidget(degerler_text)
                    
                    main_layout.addWidget(cat_frame)
                    
                    plt.close(fig)
                    
                except Exception as e:
                    error_label = QLabel(f"{kategori} için grafik oluşturulurken hata: {str(e)}")
                    error_label.setStyleSheet("color: red; padding: 10px;")
                    main_layout.addWidget(error_label)
            
            layout.addWidget(main_frame)
            
        except Exception as e:
            raise Exception(f"Kategori karşılaştırması oluşturulurken hata: {str(e)}")
        
    def create_part_comparison(self, layout, df1, df2, rapor1_adi, rapor2_adi):
        try:
            # NaN değerleri temizle
            df1_clean = df1[df1['Parça Adı'].notna() & df1['Toplam Fiyat (TL)'].notna()]
            df2_clean = df2[df2['Parça Adı'].notna() & df2['Toplam Fiyat (TL)'].notna()]
            
            if df1_clean.empty and df2_clean.empty:
                raise ValueError("Her iki raporda da parça verisi bulunamadı.")
            
            # Ana frame oluştur
            main_frame = QFrame()
            main_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                    margin-bottom: 10px;
                    padding: 10px;
                }
            """)
            main_layout = QVBoxLayout(main_frame)
            main_layout.setSpacing(10)
            
            # Parçaları birleştir
            merged = pd.merge(
                df1_clean[['Parça Adı', 'Toplam Fiyat (TL)']],
                df2_clean[['Parça Adı', 'Toplam Fiyat (TL)']],
                on='Parça Adı',
                how='outer',
                suffixes=('_1', '_2')
            ).fillna(0)
            
            if len(merged) == 0:
                raise ValueError("Karşılaştırılabilir parça bulunamadı.")
            
            # Fark hesapla ve en büyük farklara sahip parçaları bul
            merged['Fark'] = abs(merged['Toplam Fiyat (TL)_2'] - merged['Toplam Fiyat (TL)_1'])
            top_diff = merged.nlargest(5, 'Fark')
            
            if len(top_diff) == 0:
                raise ValueError("Fiyat farkı olan parça bulunamadı.")
            
            # Grafik oluştur
            plt.close('all')
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Değerleri float'a çevir
            values1 = top_diff['Toplam Fiyat (TL)_1'].astype(float)
            values2 = top_diff['Toplam Fiyat (TL)_2'].astype(float)
            
            x = np.arange(len(top_diff))
            width = 0.35
            
            rects1 = ax.bar(x - width/2, values1, width, 
                           label=rapor1_adi, color='#007bff')
            rects2 = ax.bar(x + width/2, values2, width,
                           label=rapor2_adi, color='#28a745')
            
            # Grafik ayarları
            ax.set_xticks(x)
            
            def kisalt_metin(x):
                try:
                    metin = str(x)
                    return metin[:30] + '...' if len(metin) > 30 else metin
                except Exception:
                    return str(x)
            
            labels = top_diff['Parça Adı'].apply(kisalt_metin)
            ax.set_xticklabels(labels, rotation=45, ha='right')
            
            # Izgara ve kenar boşlukları
            ax.yaxis.grid(True, linestyle='--', alpha=0.7)
            ax.set_axisbelow(True)
            plt.subplots_adjust(bottom=0.25, left=0.1)
            
            # Değerleri çubukların üzerine yaz
            def autolabel(rects, values):
                for rect, val in zip(rects, values):
                    try:
                        height = float(val)
                        ax.annotate(f'{height:,.0f} TL',
                                  xy=(rect.get_x() + rect.get_width() / 2, height),
                                  xytext=(0, 3),
                                  textcoords="offset points",
                                  ha='center', va='bottom',
                                  fontsize=9,
                                  weight='bold')
                    except Exception:
                        pass
            
            autolabel(rects1, values1)
            autolabel(rects2, values2)
            
            # Başlık ve gösterge
            ax.set_title("En Büyük Fiyat Farklılığı Olan Parçalar", pad=20)
            ax.legend(loc='upper right')
            
            plt.tight_layout()
            
            # Canvas oluştur
            canvas = FigureCanvas(fig)
            canvas.setMinimumHeight(400)
            main_layout.addWidget(canvas)
            
            # Detaylı bilgi tablosu
            info_frame = QFrame()
            info_frame.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 5px;
                    margin-top: 10px;
                }
            """)
            info_layout = QVBoxLayout(info_frame)
            
            for _, row in top_diff.iterrows():
                parca_adi = row['Parça Adı']
                fiyat1 = row['Toplam Fiyat (TL)_1']
                fiyat2 = row['Toplam Fiyat (TL)_2']
                fark = abs(fiyat2 - fiyat1)
                
                info_text = QLabel(f"""
                Parça: {parca_adi}
                {rapor1_adi}: {fiyat1:,.2f} TL
                {rapor2_adi}: {fiyat2:,.2f} TL
                Fark: {fark:,.2f} TL
                """)
                info_text.setStyleSheet("""
                    font-family: monospace;
                    font-size: 12px;
                    padding: 5px;
                    background-color: white;
                    border-radius: 3px;
                    margin: 2px;
                """)
                info_layout.addWidget(info_text)
            
            main_layout.addWidget(info_frame)
            
            # Ana frame'i layout'a ekle
            layout.addWidget(main_frame)
            
            # Figürü kapat
            plt.close(fig)
            
        except Exception as e:
            raise Exception(f"Parça karşılaştırması oluşturulurken hata: {str(e)}")
        
    def create_pie_charts(self, layout, df1, df2, rapor1_adi, rapor2_adi):
        try:
            # Ana frame oluştur
            main_frame = QFrame()
            main_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                    margin-bottom: 10px;
                    padding: 10px;
                }
            """)
            main_layout = QVBoxLayout(main_frame)
            main_layout.setSpacing(10)
            
            # NaN değerleri temizle
            df1_clean = df1[df1['Alt Kategori'].notna()]
            df2_clean = df2[df2['Alt Kategori'].notna()]
            
            if df1_clean.empty and df2_clean.empty:
                raise ValueError("Her iki raporda da kategori verisi bulunamadı.")
            
            # Kategori bazlı toplam maliyetler
            cat1 = df1_clean.groupby('Alt Kategori')['Toplam Fiyat (TL)'].sum()
            cat2 = df2_clean.groupby('Alt Kategori')['Toplam Fiyat (TL)'].sum()
            
            plt.close('all')
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            
            colors = ['#007bff', '#28a745', '#ffc107', '#6f42c1', '#dc3545',
                     '#17a2b8', '#fd7e14', '#20c997', '#6c757d', '#343a40']
            
            def make_autopct(values):
                def my_autopct(pct):
                    try:
                        total = float(sum(values))
                        val = float(round(pct*total/100.0))
                        return f'{pct:.1f}%\n({val:,} TL)'
                    except Exception:
                        return ''
                return my_autopct
            
            # İlk pasta grafik
            if not cat1.empty:
                try:
                    values1 = cat1.values.astype(float)
                    wedges1, texts1, autotexts1 = ax1.pie(values1, 
                                                        labels=cat1.index, 
                                                        autopct=make_autopct(values1),
                                                        colors=colors[:len(cat1)],
                                                        textprops={'fontsize': 9})
                    ax1.set_title(f'{rapor1_adi} Maliyet Dağılımı', pad=20)
                    plt.setp(autotexts1, size=8, weight="bold")
                    plt.setp(texts1, size=8)
                except Exception as e:
                    ax1.text(0.5, 0.5, f'Grafik oluşturulamadı:\n{str(e)}', 
                            ha='center', va='center', color='red')
            else:
                ax1.text(0.5, 0.5, 'Veri Yok', ha='center', va='center')
            
            # İkinci pasta grafik
            if not cat2.empty:
                try:
                    values2 = cat2.values.astype(float)
                    wedges2, texts2, autotexts2 = ax2.pie(values2,
                                                        labels=cat2.index,
                                                        autopct=make_autopct(values2),
                                                        colors=colors[:len(cat2)],
                                                        textprops={'fontsize': 9})
                    ax2.set_title(f'{rapor2_adi} Maliyet Dağılımı', pad=20)
                    plt.setp(autotexts2, size=8, weight="bold")
                    plt.setp(texts2, size=8)
                except Exception as e:
                    ax2.text(0.5, 0.5, f'Grafik oluşturulamadı:\n{str(e)}', 
                            ha='center', va='center', color='red')
            else:
                ax2.text(0.5, 0.5, 'Veri Yok', ha='center', va='center')
            
            # Grafik konumlandırma
            plt.subplots_adjust(wspace=0.3)
            
            # Canvas oluştur
            canvas = FigureCanvas(fig)
            canvas.setMinimumHeight(400)
            main_layout.addWidget(canvas)
            
            # Detaylı bilgi tablosu
            info_frame = QFrame()
            info_frame.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 5px;
                    margin-top: 10px;
                }
            """)
            info_layout = QVBoxLayout(info_frame)
            
            # İlk rapor için dağılım tablosu
            if not cat1.empty:
                info_text1 = QLabel(f"\n{rapor1_adi} Maliyet Dağılımı:")
                info_text1.setStyleSheet("font-weight: bold; font-size: 12px;")
                info_layout.addWidget(info_text1)
                
                total1 = cat1.sum()
                for kategori, deger in cat1.items():
                    yuzde = (deger / total1) * 100
                    text = QLabel(f"{kategori}: {deger:,.2f} TL (%{yuzde:.1f})")
                    text.setStyleSheet("""
                        font-family: monospace;
                        font-size: 12px;
                        padding: 2px;
                    """)
                    info_layout.addWidget(text)
            
            # İkinci rapor için dağılım tablosu
            if not cat2.empty:
                info_text2 = QLabel(f"\n{rapor2_adi} Maliyet Dağılımı:")
                info_text2.setStyleSheet("font-weight: bold; font-size: 12px;")
                info_layout.addWidget(info_text2)
                
                total2 = cat2.sum()
                for kategori, deger in cat2.items():
                    yuzde = (deger / total2) * 100
                    text = QLabel(f"{kategori}: {deger:,.2f} TL (%{yuzde:.1f})")
                    text.setStyleSheet("""
                        font-family: monospace;
                        font-size: 12px;
                        padding: 2px;
                    """)
                    info_layout.addWidget(text)
            
            main_layout.addWidget(info_frame)
            
            # Ana frame'i layout'a ekle
            layout.addWidget(main_frame)
            
            # Figürü kapat
            plt.close(fig)
            
        except Exception as e:
            raise Exception(f"Pasta grafikleri oluşturulurken hata: {str(e)}") 