import sqlite3

def verify_product(unique_id, username="Anonymous"):
    connection = sqlite3.connect(
        "Database/products.db"
    )
    cursor = connection.cursor()
    
    cursor.execute(
        """
        SELECT * FROM products
        WHERE unique_id = ?
        """,
        (unique_id,)
    )
    product = cursor.fetchone()

    # Product does not exist (Counterfeit)
    if product is None:
        cursor.execute(
            """
            INSERT INTO audit_logs (username, product_id, product_name, status)
            VALUES (?, ?, ?, ?)
            """,
            (username, unique_id, "Unknown Product", "Counterfeit")
        )
        connection.commit()
        connection.close()
        return (
            "Counterfeit",
            None
        )

    # Check scan count
    scan_count = product[7]
    
    if scan_count == 0:
        # First scan (Authentic)
        cursor.execute(
            """
            UPDATE products
            SET scan_count = 1,
                verification_status = 'Verified'
            WHERE unique_id = ?
            """,
            (unique_id,)
        )
        cursor.execute(
            """
            INSERT INTO audit_logs (username, product_id, product_name, status)
            VALUES (?, ?, ?, ?)
            """,
            (username, unique_id, product[1], "Authentic")
        )
        connection.commit()
        
        product_details = {
            "Unique ID": product[0],
            "Product Name": product[1],
            "Manufacturer": product[2],
            "Batch No": product[3],
            "Manufacture Date": product[4],
            "Expiry Date": product[5],
            "Status": product[8]
        }
        connection.close()
        return (
            "Authentic",
            product_details
        )
    else:
        # Subsequent scans (Duplicate)
        cursor.execute(
            """
            UPDATE products
            SET scan_count = scan_count + 1
            WHERE unique_id = ?
            """,
            (unique_id,)
        )
        cursor.execute(
            """
            INSERT INTO audit_logs (username, product_id, product_name, status)
            VALUES (?, ?, ?, ?)
            """,
            (username, unique_id, product[1], "Duplicate")
        )
        connection.commit()
        
        product_details = {
            "Unique ID": product[0],
            "Product Name": product[1],
            "Manufacturer": product[2],
            "Previous Scans": scan_count
        }
        connection.close()
        return (
            "Duplicate",
            product_details
        )