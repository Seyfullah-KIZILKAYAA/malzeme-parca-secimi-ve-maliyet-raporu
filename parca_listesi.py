from db_connection import DatabaseConnection

class ParcaVerileri:
    def __init__(self):
        self.db = DatabaseConnection()
        self.parca_detaylari = {}
        
        # Ana kategoriler
        self.ana_kategoriler = [
            "1. Ana Gövde ve Mekanik Parçalar",
            "2. Isıtma ve Elektrik Aksamı",
            "3. Kontrol ve Kullanıcı Arayüzü Parçaları",
            "4. Isıtma Plakaları ve Yüzey Kaplamaları",
            "5. Güvenlik ve Destek Parçaları",
            "6. Vidalar, Civatalar ve Küçük Parçalar",
            "7. Ekstra Parçalar (Bazı Modellerde Bulunanlar)"
        ]
        
        # Alt kategoriler - veritabanındaki tablo adlarıyla eşleşecek şekilde
        self.alt_kategoriler = {
            0: [  # Ana Gövde ve Mekanik Parçalar
                "Dis_Govde",
                "Ic_Govde_Kaplamasi",
                "Kapak_Mentesesi",
                "Kapak_Yaylari",
                "Tutma_Kolu",
                "Kilitleme_Mandali",
                "Cihaz_Ayaklari",
                "Havalandirma_Delikleri",
                "Yag_Toplama_Haznesi"
            ],
            1: [  # Isıtma ve Elektrik Aksamı
                "Rezistans",
                "Rezistans_Baglanti_Uclari",
                "Rezistans_Sabitleme_Vidalari",
                "Termostat",
                "Termostat_Baglanti_Kablolari",
                "Plaka_Baglanti_Elemanlari",
                "Elektrik_Kablosu",
                "Ic_Elektrik_Devresi",
                "Topraklama_Kablosu"
            ],
            2: [  # Kontrol ve Kullanıcı Arayüzü
                "Ana_Acma_Kapama_Dugmesi",
                "Gosterge_Isiklari",
                "Gosterge_Isigi_Yuvasi",
                "Dugme_Yaylari",
                "Sicaklik_Ayar_Dugmesi",
                "Zamanlayici_Dugmesi"
            ],
            3: [  # Isıtma Plakaları ve Yüzey Kaplamaları
                "Ust_Izgara_Plakasi",
                "Alt_Izgara_Plakasi",
                "Plaka_Kaplamasi",
                "Plaka_Tutturma_Vidalari"
            ],
            4: [  # Güvenlik ve Destek Parçaları
                "Isiya_Dayanikli_Plastik_Parcalar",
                "Ic_Yalitim_Malzemesi",
                "Sigorta",
                "Topraklama_Plakasi"
            ],
            5: [  # Vidalar, Civatalar ve Küçük Parçalar
                "Kapak_Mentese_Vidalari",
                "Rezistans_Sabitleme_Vidalari",
                "Plaka_Sabitleme_Vidalari",
                "Govde_Montaj_Vidalari",
                "Elektrik_Devresi_Lehimleri",
                "Dugme_Yaylari",
                "Termostat_Baglanti_Elemanlari"
            ],
            6: [  # Ekstra Parçalar
                "Degistirilebilir_Plakalar"
            ]
        }

    def get_parcalar(self, alt_kategori):
        try:
            # Parçaları veritabanından al
            parca_detaylari = self.db.get_parcalar(alt_kategori)
            self.parca_detaylari[alt_kategori] = parca_detaylari
            return parca_detaylari

        except Exception as e:
            print(f"Parçalar getirilirken hata: {str(e)}")
            return {
                "parcalar": ["Veri bulunamadı"],
                "gorsel_klasor": alt_kategori.lower().replace(" ", "_"),
                "maliyet": {"Veri bulunamadı": 0.0}
            } 