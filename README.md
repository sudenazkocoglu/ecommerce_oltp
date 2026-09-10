# E-Commerce OLTP Database Project

## ER Diagram

```mermaid
erDiagram
    categories {
        int category_id PK
        varchar name
        text description
    }
    products {
        int product_id PK
        int category_id FK
        varchar name
        decimal price
        int stock_quantity
    }
    users {
        int user_id PK
        varchar email
        varchar first_name
        varchar last_name
        timestamp created_at
        varchar status
    }
    coupons {
        int coupon_id PK
        varchar code
        int discount_percent
        decimal min_spend
        timestamp expires_at
    }
    orders {
        int order_id PK
        int user_id FK
        int coupon_id FK
        varchar status
        decimal total_amount
        timestamp created_at
    }
    order_items {
        int order_item_id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
    }
    payments {
        int payment_id PK
        int order_id FK
        varchar payment_method
        decimal amount
        varchar status
        timestamp paid_at
    }
    shipments {
        int shipment_id PK
        int order_id FK
        varchar tracking_number
        varchar carrier
        varchar status
        timestamp shipped_at
        timestamp delivered_at
    }
    reviews {
        int review_id PK
        int product_id FK
        int user_id FK
        int rating
        text comment
    }
    inventory_movements {
        int movement_id PK
        int product_id FK
        int change_amount
        varchar movement_type
        timestamp created_at
    }

    categories ||--o{ products : "1-N"
    users ||--o{ orders : "1-N"
    coupons ||--o{ orders : "0-N"
    orders ||--|{ order_items : "1-N"
    products ||--o{ order_items : "1-N"
    orders ||--o| payments : "1-1/0"
    orders ||--o| shipments : "1-1/0"
    users ||--o{ reviews : "1-N"
    products ||--o{ reviews : "1-N"
    products ||--o{ inventory_movements : "1-N"