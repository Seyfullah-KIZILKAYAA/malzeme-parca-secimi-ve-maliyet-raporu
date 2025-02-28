from db_connection import DatabaseConnection

def check_table_structure(table_name):
    db = DatabaseConnection()
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = '{table_name}'
        """)
        columns = cursor.fetchall()
        print(f"\nTablo: {table_name}")
        for column in columns:
            print(f"Sütun: {column[0]}, Tip: {column[1]}")

if __name__ == '__main__':
    # Örnek bir tablo adı ile test et
    check_table_structure('Cihaz_Ayaklari') 