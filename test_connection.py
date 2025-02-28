import pyodbc as odbc

# Bağlantı bilgileri
connection_string = """
    DRIVER={SQL Server};
    SERVER=SQL;
    DATABASE=MALZEME_LIST;
    UID=sa;
    PWD=password1;
    TrustServerCertificate=yes;
"""

try:
    print("Bağlantı deneniyor...")
    conn = odbc.connect(connection_string)
    print("Bağlantı başarılı!")
    
    # Test sorgusu
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    print(f"SQL Server versiyonu: {row[0]}")
    
    conn.close()
except Exception as e:
    print(f"Hata: {str(e)}") 