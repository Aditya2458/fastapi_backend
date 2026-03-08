import uuid


def test_teacher_can_add_marks(client):

    # create teacher
    email = f"teacher_{uuid.uuid4()}@gmail.com"
    password = "Strong@123"

    client.post("/api/auth/signup", json={
        "name": "Teacher",
        "age": 40,
        "location": "Delhi",
        "email": email,
        "role": "teacher",
        "password": password,
        "confirm_password": password
    })

    login = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })

    token = login.json()["access_token"]

    # create subject first
    subject_code = f"SUB_{uuid.uuid4().hex[:6]}"

    subject = client.post(
        "/api/subjects/",
        json={
            "name": "Physics",
            "code": subject_code
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    subjects = client.get("/api/subjects/")
    subject_id = subjects.json()[-1]["id"]

    # create student
    student_email = f"student_{uuid.uuid4()}@gmail.com"

    client.post("/api/auth/signup", json={
        "name": "Student",
        "age": 18,
        "location": "Delhi",
        "email": student_email,
        "role": "student",
        "password": password,
        "confirm_password": password
    })

    # student record already auto-created in your system
    student_id = 1

    response = client.post(
        "/api/marks/",
        json={
            "student_id": student_id,
            "subject_id": subject_id,
            "exam_type": "Midterm",
            "marks": 90
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200