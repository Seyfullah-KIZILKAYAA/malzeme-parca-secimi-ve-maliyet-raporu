import pyodbc as odbc

def create_database_tables():
    conn_str = 'DRIVER={SQL Server};SERVER=tcp:SQL,1433;DATABASE=MALZEME_LIST;UID=sa;PWD=Password1;TrustServerCertificate=yes;'
    conn = odbc.connect(conn_str)
    cursor = conn.cursor()

    # Ana Kategoriler tablosu
    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'AnaKategoriler')
    CREATE TABLE AnaKategoriler (
        ID INT PRIMARY KEY IDENTITY(1,1),
        KategoriAdi NVARCHAR(100) NOT NULL,
        SiraNo INT NOT NULL
    )
    ''')

    # Alt Kategoriler tablosu
    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'AltKategoriler')
    CREATE TABLE AltKategoriler (
        ID INT PRIMARY KEY IDENTITY(1,1),
        AltKategoriAdi NVARCHAR(100) NOT NULL,
        AnaKategoriID INT NOT NULL,
        SiraNo INT NOT NULL,
        FOREIGN KEY (AnaKategoriID) REFERENCES AnaKategoriler(ID)
    )
    ''')

    # Parcalar tablosu
    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Parcalar')
    CREATE TABLE Parcalar (
        ID INT PRIMARY KEY IDENTITY(1,1),
        ParcaAdi NVARCHAR(100) NOT NULL,
        BirimFiyat DECIMAL(10,2) NOT NULL,
        GorselYolu NVARCHAR(200),
        AltKategoriID INT NOT NULL,
        FOREIGN KEY (AltKategoriID) REFERENCES AltKategoriler(ID)
    )
    ''')

    # Ana kategorileri ekle
    ana_kategoriler = [
        (1, 'Ana Gövde ve Mekanik Parçalar'),
        (2, 'Isıtma ve Elektrik Aksamı'),
        (3, 'Kontrol ve Kullanıcı Arayüzü Parçaları'),
        (4, 'Isıtma Plakaları ve Yüzey Kaplamaları'),
        (5, 'Güvenlik ve Destek Parçaları'),
        (6, 'Vidalar, Civatalar ve Küçük Parçalar'),
        (7, 'Ekstra Parçalar (Bazı Modellerde Bulunanlar)')
    ]

    cursor.execute('DELETE FROM AnaKategoriler')  # Mevcut verileri temizle
    for sira, ad in ana_kategoriler:
        cursor.execute('INSERT INTO AnaKategoriler (SiraNo, KategoriAdi) VALUES (?, ?)', (sira, ad))

    conn.commit()
    print('Veritabanı tabloları ve ana kategoriler başarıyla oluşturuldu!')

if __name__ == '__main__':
    create_database_tables() 