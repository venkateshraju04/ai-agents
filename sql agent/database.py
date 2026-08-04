import sqlite3
from pathlib import Path

DB_PATH = Path("data/ecommerce.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (

        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE,

        phone TEXT,

        city TEXT,

        created_at TEXT
    )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS categories(

    category_id INTEGER PRIMARY KEY AUTOINCREMENT,

    category_name TEXT NOT NULL
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS products(

    product_id INTEGER PRIMARY KEY AUTOINCREMENT,

    category_id INTEGER,

    product_name TEXT,

    price REAL,

    stock INTEGER,

    FOREIGN KEY(category_id)

        REFERENCES categories(category_id)
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(

    order_id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_id INTEGER,

    order_date TEXT,

    total_amount REAL,

    status TEXT,

    FOREIGN KEY(customer_id)

        REFERENCES customers(customer_id)
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items(

    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,

    order_id INTEGER,

    product_id INTEGER,

    quantity INTEGER,

    unit_price REAL,

    FOREIGN KEY(order_id)

        REFERENCES orders(order_id),

    FOREIGN KEY(product_id)

        REFERENCES products(product_id)
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS payments(

    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,

    order_id INTEGER,

    payment_method TEXT,

    payment_status TEXT,

    amount REAL,

    FOREIGN KEY(order_id)

        REFERENCES orders(order_id)
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews(

    review_id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_id INTEGER,

    product_id INTEGER,

    rating INTEGER,

    review_text TEXT,

    FOREIGN KEY(customer_id)

        REFERENCES customers(customer_id),

    FOREIGN KEY(product_id)

        REFERENCES products(product_id)
)
""")
    conn.commit()

    conn.close()

if __name__ == "__main__":

    create_tables()

    print("Database Created")