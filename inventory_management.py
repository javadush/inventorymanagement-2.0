import sqlite3
from faker import Faker
import random

# Connect to SQLite database
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Create inventory table
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY,
    name TEXT,
    quantity INTEGER,
    price REAL
)
''')

# Create orders table
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    item_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    FOREIGN KEY (item_id) REFERENCES inventory(id)
)
''')

conn.commit()

# Functions to interact with the database

def add_item(name, quantity, price):
    cursor.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()

def update_item(item_id, name, quantity, price):
    cursor.execute("UPDATE inventory SET name = ?, quantity = ?, price = ? WHERE id = ?", (name, quantity, price, item_id))
    conn.commit()

def delete_item(item_id):
    cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    conn.commit()

def view_items():
    cursor.execute("SELECT * FROM inventory")
    return cursor.fetchall()

def clear_database():
    cursor.execute("DELETE FROM inventory")
    cursor.execute("DELETE FROM orders")
    conn.commit()

def generate_sample_data(num_items=10):
    fake = Faker()
    items = []
    for _ in range(num_items):
        name = fake.word().capitalize()
        quantity = random.randint(1, 100)
        price = round(random.uniform(5.0, 100.0), 2)
        items.append((name, quantity, price))
    cursor.executemany("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)", items)
    conn.commit()

def add_order(item_id, quantity, order_date):
    cursor.execute("INSERT INTO orders (item_id, quantity, order_date) VALUES (?, ?, ?)", (item_id, quantity, order_date))
    conn.commit()

def view_orders():
    cursor.execute('''SELECT orders.id, inventory.name, orders.quantity, orders.order_date 
                      FROM orders 
                      JOIN inventory ON orders.item_id = inventory.id''')
    return cursor.fetchall()

def generate_sample_orders(num_orders=10):
    fake = Faker()
    cursor.execute("SELECT id FROM inventory")
    item_ids = [row[0] for row in cursor.fetchall()]
    
    orders = []
    for _ in range(num_orders):
        item_id = random.choice(item_ids)
        quantity = random.randint(1, 10)
        order_date = fake.date_this_year().isoformat()
        orders.append((item_id, quantity, order_date))
    
    cursor.executemany("INSERT INTO orders (item_id, quantity, order_date) VALUES (?, ?, ?)", orders)
    conn.commit()

# Close the database connection
def close():
    conn.close()
