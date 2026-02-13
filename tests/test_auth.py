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
