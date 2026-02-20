import mysql.connector
import os
import time

def connect_to_db():
    while True:
        try:
            db = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
            )
            print("✅ Connected to MySQL")
            return db
        except mysql.connector.Error:
            print("⏳ Waiting for MySQL...")
            time.sleep(3)

db = connect_to_db()
cursor = db.cursor(dictionary=True)



create_table_query = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    location VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(20) NOT NULL
)
"""

cursor.execute(create_table_query)
db.commit()
print("✅ Users table ready")