#database_integration.py
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

def load_inventory_from_db():
    cursor.execute("SELECT * FROM inventory")
    return cursor.fetchall()

def load_orders_from_db():
    cursor.execute("SELECT * FROM orders")
    return cursor.fetchall()

# Close the database connection
def close():
    conn.close()

