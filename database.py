import sqlite3

DB_FILE = "listings.db"

def init_db():
    """Create the SQLite database and listings table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT,
            price INTEGER,
            sqft INTEGER
        )
    """)

    conn.commit()
    conn.close()


def insert_listing(address, price, sqft):
    """Insert a single listing into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO listings (address, price, sqft)
        VALUES (?, ?, ?)
    """, (address, price, sqft))

    conn.commit()
    conn.close()


def get_all_listings():
    """Return all listings from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM listings")
    rows = cursor.fetchall()

    conn.close()
    return rows

