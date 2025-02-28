-- Ana Kategoriler tablosu
CREATE TABLE AnaKategoriler (
    ID INT PRIMARY KEY IDENTITY(1,1),
    KategoriAdi NVARCHAR(100) NOT NULL,
    SiraNo INT NOT NULL,
    CONSTRAINT UC_KategoriAdi UNIQUE (KategoriAdi)
);

-- Alt Kategoriler tablosu
CREATE TABLE AltKategoriler (
    ID INT PRIMARY KEY IDENTITY(1,1),
    AltKategoriAdi NVARCHAR(100) NOT NULL,
    AnaKategoriID INT NOT NULL,
    SiraNo INT NOT NULL,
    CONSTRAINT FK_AltKategori_AnaKategori FOREIGN KEY (AnaKategoriID) REFERENCES AnaKategoriler(ID),
    CONSTRAINT UC_AltKategoriAdi UNIQUE (AltKategoriAdi)
);

-- Parçalar tablosu
CREATE TABLE Parcalar (
    ID INT PRIMARY KEY IDENTITY(1,1),
    ParcaAdi NVARCHAR(100) NOT NULL,
    AltKategoriID INT NOT NULL,
    BirimFiyat DECIMAL(10,2) NOT NULL,
    GorselYolu NVARCHAR(255),
    CONSTRAINT FK_Parca_AltKategori FOREIGN KEY (AltKategoriID) REFERENCES AltKategoriler(ID)
);

-- Tost Makinesi Parçaları tablosu
CREATE TABLE TostMakinesiParcalari (
    ID INT PRIMARY KEY IDENTITY(1,1),
    AltKategori NVARCHAR(100) NOT NULL,
    ParcaAdi NVARCHAR(100) NOT NULL,
    Cesit NVARCHAR(100),
    BirimFiyat DECIMAL(10,2) NOT NULL
);
