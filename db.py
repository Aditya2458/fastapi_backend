import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Adi245899",
    database="api_db"
)

cursor = db.cursor(dictionary=True)