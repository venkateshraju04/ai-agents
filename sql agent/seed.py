import random
from faker import Faker

from database import get_connection, create_tables

fake = Faker()

ORDER_STATUS = [
    "Pending",
    "Delivered",
    "Cancelled",
    "Returned"
]

PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery"
]

PAYMENT_STATUS = [
    "Paid",
    "Failed",
    "Refunded"
]

CATEGORIES = [
    "Electronics",
    "Clothing",
    "Books",
    "Home",
    "Sports",
    "Beauty",
    "Toys",
    "Groceries"
]

PRODUCTS = {
    "Electronics": [
        "iPhone 15",
        "MacBook Air",
        "Samsung TV",
        "Bluetooth Speaker",
        "Wireless Mouse",
        "Mechanical Keyboard",
        "Gaming Monitor",
        "Smart Watch",
        "Power Bank",
        "Laptop Stand"
    ],
    "Clothing": [
        "Nike Shoes",
        "Levi Jeans",
        "Puma T-Shirt",
        "Hoodie",
        "Jacket",
        "Shorts",
        "Formal Shirt",
        "Sneakers",
        "Cap",
        "Socks"
    ],
    "Books": [
        "Atomic Habits",
        "Clean Code",
        "Deep Learning",
        "Harry Potter",
        "Rich Dad Poor Dad",
        "The Alchemist",
        "Think and Grow Rich",
        "Python Crash Course",
        "Design Patterns",
        "Algorithms"
    ],
    "Home": [
        "Coffee Maker",
        "Vacuum Cleaner",
        "Mixer Grinder",
        "Dining Chair",
        "Study Table",
        "Bed Sheet",
        "Curtains",
        "Water Bottle",
        "Wall Clock",
        "Lamp"
    ],
    "Sports": [
        "Football",
        "Cricket Bat",
        "Yoga Mat",
        "Basketball",
        "Dumbbells",
        "Skipping Rope",
        "Tennis Racket",
        "Helmet",
        "Sports Bag",
        "Running Shoes"
    ],
    "Beauty": [
        "Face Wash",
        "Shampoo",
        "Perfume",
        "Lipstick",
        "Moisturizer",
        "Sunscreen",
        "Hair Oil",
        "Body Wash",
        "Conditioner",
        "Face Cream"
    ],
    "Toys": [
        "LEGO Set",
        "Remote Car",
        "Puzzle",
        "Action Figure",
        "Chess Board",
        "Barbie Doll",
        "Toy Train",
        "Building Blocks",
        "Rubik Cube",
        "Drone Toy"
    ],
    "Groceries": [
        "Rice",
        "Milk",
        "Bread",
        "Eggs",
        "Sugar",
        "Salt",
        "Cooking Oil",
        "Tea Powder",
        "Coffee",
        "Pasta"
    ]
}

REVIEWS = [
    "Excellent product",
    "Worth the money",
    "Highly recommended",
    "Average quality",
    "Good value",
    "Not satisfied",
    "Will buy again",
    "Packaging could be better",
    "Amazing quality",
    "Very useful"
]


def seed_categories(cursor):
    for category in CATEGORIES:
        cursor.execute(
            """
            INSERT INTO categories(category_name)
            VALUES(?)
            """,
            (category,)
        )


def seed_products(cursor):

    cursor.execute("SELECT category_id, category_name FROM categories")
    categories = cursor.fetchall()

    for category_id, category_name in categories:

        for _ in range(25):

            name = random.choice(PRODUCTS[category_name])

            cursor.execute(
                """
                INSERT INTO products(
                    category_id,
                    product_name,
                    price,
                    stock
                )
                VALUES(?,?,?,?)
                """,
                (
                    category_id,
                    name,
                    round(random.uniform(100, 100000), 2),
                    random.randint(10, 500)
                )
            )


def seed_customers(cursor):

    for _ in range(500):

        cursor.execute(
            """
            INSERT INTO customers(
                name,
                email,
                phone,
                city,
                created_at
            )
            VALUES(?,?,?,?,?)
            """,
            (
                fake.name(),
                fake.unique.email(),
                fake.phone_number(),
                fake.city(),
                fake.date_between("-3y", "today")
            )
        )


def seed_orders(cursor):

    cursor.execute("SELECT customer_id FROM customers")
    customers = [x[0] for x in cursor.fetchall()]

    for _ in range(5000):

        customer = random.choice(customers)

        total = round(random.uniform(500, 10000), 2)

        cursor.execute(
            """
            INSERT INTO orders(
                customer_id,
                order_date,
                total_amount,
                status
            )
            VALUES(?,?,?,?)
            """,
            (
                customer,
                fake.date_between("-2y", "today"),
                total,
                random.choice(ORDER_STATUS)
            )
        )


def seed_order_items(cursor):

    cursor.execute("SELECT order_id FROM orders")
    orders = [x[0] for x in cursor.fetchall()]

    cursor.execute("SELECT product_id, price FROM products")
    products = cursor.fetchall()

    for order in orders:

        num_items = random.randint(1, 5)

        total = 0

        for _ in range(num_items):

            product_id, price = random.choice(products)

            qty = random.randint(1, 3)

            total += qty * price

            cursor.execute(
                """
                INSERT INTO order_items(
                    order_id,
                    product_id,
                    quantity,
                    unit_price
                )
                VALUES(?,?,?,?)
                """,
                (
                    order,
                    product_id,
                    qty,
                    price
                )
            )

        cursor.execute(
            """
            UPDATE orders
            SET total_amount=?
            WHERE order_id=?
            """,
            (round(total, 2), order)
        )


def seed_payments(cursor):

    cursor.execute(
        """
        SELECT order_id,total_amount
        FROM orders
        """
    )

    for order_id, amount in cursor.fetchall():

        cursor.execute(
            """
            INSERT INTO payments(
                order_id,
                payment_method,
                payment_status,
                amount
            )
            VALUES(?,?,?,?)
            """,
            (
                order_id,
                random.choice(PAYMENT_METHODS),
                random.choices(
                    PAYMENT_STATUS,
                    weights=[90, 5, 5]
                )[0],
                amount
            )
        )


def seed_reviews(cursor):

    cursor.execute("SELECT customer_id FROM customers")
    customers = [x[0] for x in cursor.fetchall()]

    cursor.execute("SELECT product_id FROM products")
    products = [x[0] for x in cursor.fetchall()]

    for _ in range(2000):

        cursor.execute(
            """
            INSERT INTO reviews(
                customer_id,
                product_id,
                rating,
                review_text
            )
            VALUES(?,?,?,?)
            """,
            (
                random.choice(customers),
                random.choice(products),
                random.randint(1, 5),
                random.choice(REVIEWS)
            )
        )


def main():

    create_tables()

    conn = get_connection()
    cursor = conn.cursor()

    print("Seeding Categories...")
    seed_categories(cursor)

    print("Seeding Products...")
    seed_products(cursor)

    print("Seeding Customers...")
    seed_customers(cursor)

    print("Seeding Orders...")
    seed_orders(cursor)

    print("Seeding Order Items...")
    seed_order_items(cursor)

    print("Seeding Payments...")
    seed_payments(cursor)

    print("Seeding Reviews...")
    seed_reviews(cursor)

    conn.commit()
    conn.close()

    print("\nDatabase Seeded Successfully!")


if __name__ == "__main__":
    main()