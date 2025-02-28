import pyodbc as odbc
from typing import Dict, List, Any

class DatabaseConnection:
    def __init__(self, server="SQL", database="MALZEME_LIST", username="sa", password="Password1"):
        # SQL Server bağlantı bilgileri
        self.connection_string = (
            f"DRIVER={{SQL Server}};"
            f"SERVER=tcp:{server},1433;"  # TCP/IP protokolü ve varsayılan port
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            "TrustServerCertificate=yes;"
        )

    def get_connection(self):
        try:
            print(f"Bağlantı deneniyor...")
            conn = odbc.connect(self.connection_string)
            print(f"Bağlantı başarılı!")
            return conn
        except Exception as e:
            print(f"Bağlantı hatası: {str(e)}")
            raise
    
    def get_ana_kategoriler(self) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT KategoriAdi FROM AnaKategoriler ORDER BY SiraNo")
            return [row[0] for row in cursor.fetchall()]
    
    def get_alt_kategoriler(self, ana_kategori_id: int) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT AltKategoriAdi 
                FROM AltKategoriler 
                WHERE AnaKategoriID = ? 
                ORDER BY SiraNo
            """, ana_kategori_id)
            return [row[0] for row in cursor.fetchall()]
    
    def get_parcalar(self, alt_kategori: str) -> Dict[str, Any]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Alt kategori adını SQL tablo adına çevir
                tablo_adi = f"dbo.{alt_kategori}"
                
                # Önce tablo yapısını kontrol et
                cursor.execute(f"""
                    SELECT COLUMN_NAME 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = '{alt_kategori}'
                    ORDER BY COLUMN_NAME
                """)
                columns = [row[0] for row in cursor.fetchall()]
                
                # Fiyat sütununu bul
                price_column = None
                if 'PRICE' in columns:
                    price_column = 'PRICE'
                elif 'PRİCE' in columns:
                    price_column = 'PRİCE'
                
                # Sorguyu oluştur
                if price_column:
                    query = f"""
                        SELECT [ID], [MATERIAL_NAME], ISNULL([{price_column}], 0) as PRICE 
                        FROM {tablo_adi}
                        ORDER BY [ID]
                    """
                else:
                    query = f"""
                        SELECT [ID], [MATERIAL_NAME], 0 as PRICE 
                        FROM {tablo_adi}
                        ORDER BY [ID]
                    """
                
                # Sorguyu çalıştır
                cursor.execute(query)
                
                parcalar = []
                for row in cursor.fetchall():
                    # Fiyat NULL ise 0 kullan
                    fiyat = float(row[2]) if row[2] is not None else 0.0
                    # MATERIAL_NAME'deki boşlukları temizle
                    material_name = row[1].strip() if row[1] else ""
                    parca_adi = f"{material_name} ({fiyat} TL)"
                    parcalar.append({
                        "parca_adi": parca_adi,
                        "birim_fiyat": fiyat
                    })
                
                return {
                    "parcalar": [p["parca_adi"] for p in parcalar],
                    "gorsel_klasor": alt_kategori.lower().replace(" ", "_"),
                    "maliyet": {p["parca_adi"]: p["birim_fiyat"] for p in parcalar}
                }
                
        except Exception as e:
            print(f"Parçalar getirilirken hata: {str(e)}")
            return {
                "parcalar": ["Veri bulunamadı"],
                "gorsel_klasor": alt_kategori.lower().replace(" ", "_"),
                "maliyet": {"Veri bulunamadı": 0.0}
            }

    def get_all_tables(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE = 'BASE TABLE'
                    ORDER BY TABLE_NAME
                """)
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Tablolar listelenirken hata: {str(e)}")
            return [] 