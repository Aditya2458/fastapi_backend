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

TESTING = os.getenv("TESTING") == "1"

if not TESTING:
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
else:
    db = None
    cursor = None