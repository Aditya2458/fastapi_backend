import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add project root (/app) to Python path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from main import app


@pytest.fixture
def client():
    return TestClient(app)

import uuid


@pytest.fixture
def admin_token(client):

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