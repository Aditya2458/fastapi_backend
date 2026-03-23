import uuid


def test_teacher_can_add_marks(client):

    password = "Strong@123"

    # create admin
    admin_email = f"admin_{uuid.uuid4()}@gmail.com"

    client.post("/api/auth/signup", json={
        "name": "Admin",
        "age": 30,
        "location": "Delhi",
        "email": admin_email,
        "role": "admin",
        "password": password,
        "confirm_password": password
    })

    admin_login = client.post("/api/auth/login", json={
        "email": admin_email,
        "password": password
    })

    admin_token = admin_login.json()["access_token"]

    # create subject
    subject_code = f"SUB_{uuid.uuid4().hex[:6]}"

    client.post(
        "/api/subjects/",
        json={
            "name": "Physics",
            "code": subject_code
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    subjects = client.get("/api/subjects/")
    subject_id = subjects.json()[0]["id"]

    # create teacher
    teacher_email = f"teacher_{uuid.uuid4()}@gmail.com"

    client.post("/api/auth/signup", json={
        "name": "Teacher",
        "age": 40,
        "location": "Delhi",
        "email": teacher_email,
        "role": "teacher",
        "password": password,
        "confirm_password": password
    })

    teacher_login = client.post("/api/auth/login", json={
        "email": teacher_email,
        "password": password
    })

    teacher_token = teacher_login.json()["access_token"]

    # 🔥 get teacher_id from /me
    me = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    teacher_id = me.json()["data"]["id"]

    # ✅ assign teacher to subject (ADMIN ONLY)
    client.post(
        "/api/teacher-subjects/",
        json={
            "teacher_id": teacher_id,
            "subject_id": subject_id
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

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

    student_id = 1

    # now teacher can add marks ✅
    response = client.post(
        "/api/marks/",
        json={
            "student_id": student_id,
            "subject_id": subject_id,
            "exam_type": "Midterm",
            "marks": 90
        },
        headers={"Authorization": f"Bearer {teacher_token}"}
    )

    assert response.status_code == 200


def test_teacher_cannot_add_marks_without_assignment(client):
    import uuid

    password = "Strong@123"

    # create teacher
    teacher_email = f"teacher_{uuid.uuid4()}@gmail.com"

    client.post("/api/auth/signup", json={
        "name": "Teacher",
        "age": 40,
        "location": "Delhi",
        "email": teacher_email,
        "role": "teacher",
        "password": password,
        "confirm_password": password
    })

    login = client.post("/api/auth/login", json={
        "email": teacher_email,
        "password": password
    })

    teacher_token = login.json()["access_token"]

    # ❌ no subject assignment here

    response = client.post(
        "/api/marks/",
        json={
            "student_id": 1,
            "subject_id": 1,
            "exam_type": "Midterm",
            "marks": 90
        },
        headers={"Authorization": f"Bearer {teacher_token}"}
    )

    assert response.status_code == 403