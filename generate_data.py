import random
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import execute_values

# PostgreSQL bağlantı ayarları
DB_CONFIG = {
    "dbname": "ecommerce_oltp",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5433
}

def generate_full_dataset():
    print("🚀 Sentetik veri üretimi ve veritabanı aktarımı başlatılıyor...")
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # 1. Kategoriler (10 adet)
        print("-> Kategoriler üretiliyor...")
        categories = [(f"Category_{i}", f"Description for category {i}") for i in range(1, 11)]
        execute_values(cursor, "INSERT INTO categories (name, description) VALUES %s", categories)
        conn.commit()
        
        # 2. Kullanıcılar (20,000 adet)
        print("-> Kullanıcılar üretiliyor (20k)...")
        users = []
        for i in range(1, 20001):
            email = f"user_{i}@example.com"
            first_name = f"Name{i}"
            last_name = f"Surname{i}"
            created_at = datetime.now() - timedelta(days=random.randint(1, 365))
            status = 'active' if random.random() > 0.05 else 'suspended'
            users.append((email, first_name, last_name, created_at, status))
        execute_values(cursor, "INSERT INTO users (email, first_name, last_name, created_at, status) VALUES %s", users)
        conn.commit()

        # 3. Ürünler (1,000 adet)
        print("-> Ürünler üretiliyor (1k)...")
        products = []
        for i in range(1, 1001):
            cat_id = random.randint(1, 10)
            name = f"Product_{i}"
            price = round(random.expovariate(1/100) + 10, 2)
            stock = random.randint(0, 500)
            products.append((cat_id, name, price, stock))
        execute_values(cursor, "INSERT INTO products (category_id, name, price, stock_quantity) VALUES %s", products)
        conn.commit()

        # 4. Kuponlar (50 adet)
        print("-> Kuponlar üretiliyor...")
        coupons = []
        for i in range(1, 51):
            code = f"DISCOUNT_{i}0"
            discount = random.choice([5, 10, 15, 20, 25, 50])
            min_spend = random.choice([0, 100, 250, 500])
            expires_at = datetime.now() + timedelta(days=random.randint(10, 90))
            coupons.append((code, discount, min_spend, expires_at))
        execute_values(cursor, "INSERT INTO coupons (code, discount_percent, min_spend, expires_at) VALUES %s", coupons)
        conn.commit()

        # 5. Siparişler ve Kalemleri (~80,000 sipariş, ~350,000 order_items)
        print("-> Siparişler ve detayları üretiliyor (Büyük veri yükü)...")
        orders = []
        order_items = []
        payments = []
        shipments = []
        
        order_id_counter = 1
        for _ in range(80000):
            user_id = random.randint(1, 20000)
            coupon_id = random.choice([None, random.randint(1, 50)]) if random.random() > 0.4 else None
            status = random.choice(['completed', 'pending', 'cancelled', 'refunded'])
            created_at = datetime.now() - timedelta(days=random.randint(1, 180))
            
            item_count = random.choices([1, 2, 3, 4, 5, 6], weights=[40, 30, 15, 8, 5, 2])[0]
            total_amount = 0
            
            current_order_items = []
            for _ in range(item_count):
                prod_id = random.randint(1, 1000)
                qty = random.randint(1, 5)
                unit_price = round(random.uniform(15, 750), 2)
                
                # %2 anomali (Miktar negatif yapılamayacağı için kaldırıldı veya yoksayıldı)

                total_amount += max(0, qty * unit_price)
                current_order_items.append((order_id_counter, prod_id, qty, unit_price))
            
            orders.append((user_id, coupon_id, status, round(total_amount, 2), created_at))
            order_items.extend(current_order_items)
            
            pay_status = 'failed' if status == 'cancelled' else 'success'
            payments.append((order_id_counter, random.choice(['credit_card', 'paypal', 'apple_pay']), round(total_amount, 2), pay_status, created_at))
            
            tracking = f"TRK{order_id_counter}XYZ"
            ship_status = 'delivered' if status == 'completed' else 'processing'
            shipments.append((order_id_counter, tracking, random.choice(['Aras', 'MNG', 'Yurtiçi']), ship_status, created_at, created_at + timedelta(days=2)))
            
            order_id_counter += 1

        execute_values(cursor, "INSERT INTO orders (user_id, coupon_id, status, total_amount, created_at) VALUES %s", orders)
        execute_values(cursor, "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES %s", order_items)
        execute_values(cursor, "INSERT INTO payments (order_id, payment_method, amount, status, paid_at) VALUES %s", payments)
        execute_values(cursor, "INSERT INTO shipments (order_id, tracking_number, carrier, status, shipped_at, delivered_at) VALUES %s", shipments)
        conn.commit()

        # 6. Ürün Yorumları (Reviews - 40,000 adet)
        print("-> Ürün yorumları üretiliyor...")
        reviews = []
        for _ in range(40000):
            prod_id = random.randint(1, 1000)
            user_id = random.randint(1, 20000)
            rating = random.choices([1, 2, 3, 4, 5], weights=[5, 5, 10, 30, 50])[0]
            comment = None if random.random() < 0.05 else f"Comment rating {rating} for product."
            reviews.append((prod_id, user_id, rating, comment))
        execute_values(cursor, "INSERT INTO reviews (product_id, user_id, rating, comment) VALUES %s", reviews)
        conn.commit()

        # 7. Stok Hareketleri (Inventory Movements - 50,000 adet)
        print("-> Stok hareketleri üretiliyor...")
        inventory_movs = []
        for _ in range(50000):
            prod_id = random.randint(1, 1000)
            change = random.randint(-20, 50) 
            m_type = 'restock' if change > 0 else 'sale'
            inventory_movs.append((prod_id, change, m_type))
        execute_values(cursor, "INSERT INTO inventory_movements (product_id, change_amount, movement_type) VALUES %s", inventory_movs)
        conn.commit()

        print("🎉 Başarılı! 500k+ satırlık tüm sentetik veri tablolara başarıyla basıldı.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Hata oluştu: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    generate_full_dataset()