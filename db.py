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
# classes table first domain table 

cursor.execute(create_table_query)
db.commit()
print("✅ Users table ready")


create_classes_table = """
CREATE TABLE IF NOT EXISTS classes(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50),
section VARCHAR (10)
)"""

cursor.execute(create_classes_table)
db.commit()



create_students_table = """
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    class_id INT,
    roll_no INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE SET NULL
)
"""
cursor.execute(create_students_table)
db.commit()
print("✅ Students table ready")


create_subjects_table = """
CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE
)
"""

cursor.execute(create_subjects_table)
db.commit()
print("✅ Subjects table ready")


create_marks_table = """
CREATE TABLE IF NOT EXISTS marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    subject_id INT,
    exam_type VARCHAR(50),
    marks INT,

    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
)
"""

cursor.execute(create_marks_table)
db.commit()
print("✅ Marks table ready")



create_teacher_subjects_table = """
CREATE TABLE IF NOT EXISTS teacher_subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT,
    subject_id INT,

    FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,

    UNIQUE (teacher_id, subject_id)
)
"""

    

cursor.execute(create_teacher_subjects_table)
db.commit()
print("✅ Teacher-Subjects table ready")
