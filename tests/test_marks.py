import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_teacher():
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

    return login.json()["access_token"]


def test_teacher_can_add_marks():
    token = create_teacher()

    response = client.post(
        "/api/marks/",
        json={
            "student_id": 1,
            "subject_id": 1,
            "exam_type": "Midterm",
            "marks": 85
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200