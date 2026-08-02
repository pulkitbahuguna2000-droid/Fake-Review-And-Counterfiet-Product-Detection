import sqlite3
import hashlib


# =========================
# HELPER FUNCTIONS
# =========================

def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


# =========================
# CREATE CUSTOMER TABLE
# =========================

def create_customer_table():
    connection = sqlite3.connect(
        "Database/products.db"
    )
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            username TEXT PRIMARY KEY,
            email TEXT,
            password TEXT
        )
        """
    )

    connection.commit()
    connection.close()


# =========================
# REGISTER CUSTOMER
# =========================

def register_customer(username, email, password):
    create_customer_table()

    connection = sqlite3.connect(
        "Database/products.db"
    )
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO customers
            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                hash_password(password)
            )
        )

        connection.commit()
        connection.close()
        return True

    except Exception as e:
        connection.close()
        return False


# =========================
# CUSTOMER LOGIN
# =========================

def login_customer(username, password):
    create_customer_table()

    connection = sqlite3.connect(
        "Database/products.db"
    )
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM customers
        WHERE username=? AND password=?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cursor.fetchone()
    connection.close()

    if user:
        return True
    else:
        return False