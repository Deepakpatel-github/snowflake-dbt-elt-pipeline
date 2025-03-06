import datetime
import random
import psycopg2
import os
from faker import Faker
from psycopg2 import sql

# Initialize Faker
fake = Faker()

# PostgreSQL Connection Details (Use environment variables for security)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "ecommerce_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "root@123"),
    "options": "-c search_path=public"  # Ensure correct schema
}

# Product options
PRODUCTS = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"]
ORDER_STATUSES = ["Shipped", "Pending", "Delivered", "Cancelled"]

def insert_fake_data(num_customers=10, num_orders=20):
    """Inserts fake customers and their orders into the database."""
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                
                # Insert fake customers
                customer_ids = []
                for _ in range(num_customers):
                    customer_name = fake.name()[:20]
                    email = fake.email()[:20]
                    phone = fake.phone_number()[:20]
                    address = fake.address()[:20]

                    print(f"Inserting Customer: {customer_name}, {email}, {phone}")  # Debugging
                    cur.execute(
                        sql.SQL("INSERT INTO customers (customer_name, email, phone, address) VALUES (%s, %s, %s, %s) RETURNING customer_id"),
                        (customer_name, email, phone, address)
                    )
                    customer_ids.append(cur.fetchone()[0])  # Store customer_id
                
                # Insert fake orders
                for _ in range(num_orders):
                    customer_id = random.choice(customer_ids)
                    product_name = random.choice(PRODUCTS)
                    quantity = random.randint(1, 5)
                    total_price = round(random.uniform(10, 500), 2)
                    order_status = random.choice(ORDER_STATUSES)
                    order_date = fake.date_time_between(start_date="-1y", end_date="now")

                    print(f"Inserting Order: Customer={customer_id}, Product={product_name}, Quantity={quantity}, Price={total_price}")  # Debugging
                    cur.execute(
                        sql.SQL("INSERT INTO orders (customer_id, product_name, quantity, total_price, order_status, order_date) VALUES (%s, %s, %s, %s, %s, %s)"),
                        (customer_id, product_name, quantity, total_price, order_status, order_date)
                    )

                conn.commit()  # Ensure data is saved
                print(f"✅ Inserted {num_customers} customers and {num_orders} orders successfully!")

    except Exception as e:
        print(f"❌ Error inserting data: {e}")

# Run the function
if __name__ == "__main__":
    insert_fake_data(num_customers=10, num_orders=20)
