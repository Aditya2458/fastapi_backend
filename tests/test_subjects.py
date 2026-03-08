import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_admin():
    email = f"admin_{uuid.uuid4()}@gmail.com"
    password = "Strong@123"

    client.post("/api/auth/signup", json={
        "name": "Admin",
        "age": 30,
        "location": "Delhi",
        "email": email,
        "role": "admin",
        "password": password,
        "confirm_password": password
    })

    login = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })

    return login.json()["access_token"]


def test_admin_can_create_subject():
    token = create_admin()

    response = client.post(
        "/api/subjects/",
        json={
            "name": "Physics",
            "code": "PHY"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Subject created"


def test_get_subjects():
    response = client.get("/api/subjects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)