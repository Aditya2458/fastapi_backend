from db import db, cursor
from mysql.connector import IntegrityError, Error
from fastapi import HTTPException


def create_user(user, hashed_password):
    query = """
    INSERT INTO users (name, age, location, email, password, role)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        user.name,
        user.age,
        user.location,
        user.email,
        hashed_password,
        user.role
    )

    try:
        cursor.execute(query, values)
        db.commit()

        user_id = cursor.lastrowid

        # Only create student record if role is student
        if user.role == "student":
            create_student_query = """
            INSERT INTO students (user_id)
            VALUES (%s)
            """
            cursor.execute(create_student_query, (user_id,))
            db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    except Error as e:
        db.rollback()
        print("DB ERROR:", e)  # Temporary debug
        raise HTTPException(
            status_code=503,
            detail="Database temporarily unavailable"
        )


def get_users():
    cursor.execute("SELECT id, name, age, location, email FROM users")
    return cursor.fetchall()


def update_user(user_id, user):
    query = """
    UPDATE users
    SET name=%s, age=%s, location=%s
    WHERE id=%s
    """
    values = (user.name, user.age, user.location, user_id)
    cursor.execute(query, values)
    db.commit()


def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()

def get_user_by_email(email):
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )
    return cursor.fetchone()

def update_user_password(user_id:int , hashed_password:int):
    query="UPDATE users SET password= %s WHERE id =%s"
    cursor.execute(query,(hashed_password,user_id))
    db.commit()