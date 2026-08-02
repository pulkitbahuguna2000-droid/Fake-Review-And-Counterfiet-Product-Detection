import sqlite3
import os

# Ensure the Database directory exists
os.makedirs("Database", exist_ok=True)

connection = sqlite3.connect(
    "Database/products.db"
)
cursor = connection.cursor()

# Drop old tables if exist to clear plaintext passwords and start fresh
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("DROP TABLE IF EXISTS admins")
cursor.execute("DROP TABLE IF EXISTS customers")
cursor.execute("DROP TABLE IF EXISTS audit_logs")

# Create products table
cursor.execute(
    """
    CREATE TABLE products (
        unique_id TEXT PRIMARY KEY,
        product_name TEXT,
        manufacturer TEXT,
        batch_no TEXT,
        manufacture_date TEXT,
        expiry_date TEXT,
        verification_status TEXT,
        scan_count INTEGER,
        status TEXT
    )
    """
)

# Create audit logs table
cursor.execute(
    """
    CREATE TABLE audit_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        username TEXT,
        product_id TEXT,
        product_name TEXT,
        status TEXT
    )
    """
)
connection.commit()
connection.close()
print(
    "Product Database Created/Reset Successfully"
)