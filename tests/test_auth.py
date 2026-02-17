import sys
import os
import uuid

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app

from fastapi.testclient import TestClient

client=TestClient(app)

def test_signup_success():
    email = f"test_{uuid.uuid4()}@gmail.com"
    response = client.post("/api/auth/signup", json={
        "name": "Test User",
        "age": 22,
        "location": "Delhi",
        "email": email,
        "password": "Strong@123",
        "confirm_password": "Strong@123"
        })
    assert response.status_code== 201
    assert response.json()["message"]=="User registered successfully"

def test_login_success():
    email=f"login_{uuid.uuid4()}@gmail.com"
    password= "Strong@123"

    #create user first 
    client.post("/api/auth/signup", json={
        "name": "Login User",
        "age": 23,
        "location": "Delhi",
        "email": email,
        "password": password,
        "confirm_password": password
    })

    #now login 
    response=client.post("/api/auth/login",json={
        "email":email,
        "password": password
    })

    assert response.status_code==200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"]== "bearer"

def test_signup_duplicate_email():
    import uuid

    email = f"duplicate_{uuid.uuid4()}@gmail.com"

    payload = {
        "name": "Duplicate User",
        "age": 25,
        "location": "Delhi",
        "email": email,
        "password": "Strong@123",
        "confirm_password": "Strong@123"
    }

    # First signup → should succeed
    first_response = client.post("/api/auth/signup", json=payload)
    assert first_response.status_code == 201

    # Second signup with same email → should return 409
    second_response = client.post("/api/auth/signup", json=payload)

    # Debug prints (temporary)
    print("STATUS:", second_response.status_code)
    print("BODY:", second_response.json())

    assert second_response.status_code == 409
    assert second_response.json()["message"] == "Email already registered"
    assert second_response.json()["success"] is False
    assert second_response.json()["status_code"] == 409

    
    
    
def test_protected_route_with_token():
    import uuid

    email = f"secure_{uuid.uuid4()}@gmail.com"
    password = "Strong@123"

    # Create user
    client.post("/api/auth/signup", json={
        "name": "Secure User",
        "age": 24,
        "location": "Delhi",
        "email": email,
        "password": password,
        "confirm_password": password
    })

    # Login
    login_response = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })

    token = login_response.json()["access_token"]

    # Access protected route
    response = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

