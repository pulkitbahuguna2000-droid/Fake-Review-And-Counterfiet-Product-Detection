import sqlite3
import uuid
import qrcode
import os
import hashlib


# =========================
# HELPER FUNCTIONS
# =========================

def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


# =========================
# ADMIN ACCESS KEY
# =========================

ADMIN_SECRET_KEY = "COMPANY2026"


# =========================
# ADD PRODUCT
# =========================

def add_product(
        product_name,
        manufacturer,
        batch_no,
        manufacture_date,
        expiry_date
):
    unique_id = str(uuid.uuid4())[:8]

    connection = sqlite3.connect(
        "Database/products.db"
    )
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO products
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            unique_id,
            product_name,
            manufacturer,
            batch_no,
            manufacture_date,
            expiry_date,
            "Not Verified",
            0,
            "Authentic"
        )
    )

    connection.commit()
    connection.close()

    # Create QR folder
    os.makedirs(
        "qr_codes",
        exist_ok=True
    )

    qr = qrcode.make(
        unique_id
    )

    qr.save(
        f"qr_codes/{unique_id}.png"
    )

    return unique_id


# =========================
# FETCH PRODUCTS
# =========================

def get_all_products():
    connection = sqlite3.connect(
        "Database/products.db"
    )
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        """
    )

    products = cursor.fetchall()
    connection.close()

    return products


# =========================
# CREATE ADMIN TABLE
# =========================

def create_admin_table():
    connection = sqlite3.connect(
        "Database/products.db"
    )
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS admins (
            username TEXT PRIMARY KEY,
            email TEXT,
            password TEXT
        )
        """
    )

    connection.commit()
    connection.close()


# =========================
# REGISTER ADMIN
# =========================

def register_admin(
        username,
        email,
        password,
        access_key
):
    create_admin_table()

    if access_key != ADMIN_SECRET_KEY:
        return "Unauthorized"

    connection = sqlite3.connect(
        "Database/products.db"
    )
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO admins
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
        return "Success"

    except Exception as e:
        connection.close()
        return "Exists"


# =========================
# LOGIN ADMIN
# =========================

def login_admin(
        username,
        password
):
    create_admin_table()

    connection = sqlite3.connect(
        "Database/products.db"
    )
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM admins
        WHERE username=? AND password=?
        """,
        (
            username,
            hash_password(password)
        )
    )

    result = cursor.fetchone()
    connection.close()

    if result:
        return True
    else:
        return False


# =========================
# GET AUDIT LOGS
# =========================

def get_audit_logs():
    connection = sqlite3.connect(
        "Database/products.db"
    )
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM audit_logs
            ORDER BY timestamp DESC
            """
        )
        logs = cursor.fetchall()
    except sqlite3.OperationalError:
        # Return empty list if table doesn't exist yet
        logs = []
    connection.close()
    return logs