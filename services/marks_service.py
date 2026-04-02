import json
from crud import create_mark, get_marks
from redis_client import redis_client
from db import db, cursor
from crud import is_teacher_assigned 


def add_mark_service(mark, teacher_id):

    assigned = is_teacher_assigned(teacher_id, mark.subject_id)

    if not assigned:
        return False

    query = """
    INSERT INTO marks (student_id, subject_id, exam_type, marks)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        mark.student_id,
        mark.subject_id,
        mark.exam_type,
        mark.marks
    )

    cursor.execute(query, values)
    db.commit()


    # 🔥 CLEAR CACHE (CRITICAL)
    redis_client.delete("marks:all")

    return True


def list_marks_service():
    cache_key = "marks:all"

    cached = redis_client.get(cache_key)
    if cached:
        print("CACHE HIT")
        return json.loads(cached)

    print("CACHE MISS")

    marks = get_marks()

    result = marks  # ✅ FIX HERE

    redis_client.setex(cache_key, 60, json.dumps(result))

    print("SAVED TO REDIS")

    return result