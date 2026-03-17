import uuid


def test_admin_can_create_subject(client, admin_token):

    code = f"SUB_{uuid.uuid4().hex[:6]}"

    response = client.post(
        "/api/subjects/",
        json={
            "name": "Physics",
            "code": code
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Subject created"


def test_duplicate_subject_code(client, admin_token):

    code = f"DUP_{uuid.uuid4().hex[:6]}"

    client.post(
        "/api/subjects/",
        json={
            "name": "Chemistry",
            "code": code
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.post(
        "/api/subjects/",
        json={
            "name": "Chemistry",
            "code": code
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 409


def test_get_subjects(client):

    response = client.get("/api/subjects/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    import uuid


def test_non_admin_cannot_create_subject(client):

    email = f"user_{uuid.uuid4()}@gmail.com"
    password = "Strong@123"

    # create student user
    client.post("/api/auth/signup", json={
        "name": "Student User",
        "age": 20,
        "location": "Delhi",
        "email": email,
        "role": "student",
        "password": password,
        "confirm_password": password
    })

    # login
    login = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })

    token = login.json()["access_token"]

    code = f"SUB_{uuid.uuid4().hex[:6]}"

    response = client.post(
        "/api/subjects/",
        json={
            "name": "Biology",
            "code": code
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403





import uuid


def test_create_subject_missing_code(client, admin_token):

    response = client.post(
        "/api/subjects/",
        json={
            "name": "Mathematics"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 422



