import psycopg2

DB_CONFIG = {
    "dbname": "ecommerce_oltp",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5433
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # Mevcut tabloları ve bağımlılıklarını tamamen temizle
    print("🧹 Eski tablolar temizleniyor...")
    cur.execute("DROP SCHEMA public CASCADE;")
    cur.execute("CREATE SCHEMA public;")
    conn.commit()
    
    # schema.sql dosyasını oku ve çalıştır
    print("🛠️ Yeni tablolar oluşturuluyor...")
    with open("schema.sql", "r", encoding="utf-8") as f:
        schema_sql = f.read()
        
    cur.execute(schema_sql)
    conn.commit()
    print("✅ Tablolar başarıyla yeniden oluşturuldu!")
    
except Exception as e:
    conn.rollback()
    print(f"❌ Hata oluştu: {e}")
finally:
    cur.close()
    conn.close()