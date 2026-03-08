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