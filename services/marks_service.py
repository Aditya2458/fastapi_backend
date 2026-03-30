import json
from crud import create_mark, get_marks
from redis_client import redis_client


def add_mark_service(mark, teacher_id, is_assigned):
    if not is_assigned:
        return None

    try:
        create_mark(mark.student_id, mark.subject_id, mark.exam_type, mark.marks)

        # invalidate cache
        redis_client.delete("marks:all")
        print("CACHE INVALIDATED")

        return True

    except Exception as e:
        print(f"ERROR in add_mark_service: {e}")
        return False


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