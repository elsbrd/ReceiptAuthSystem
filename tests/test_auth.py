from datetime import datetime


def test_successful_signup(client):
    response = client.post(
        "api/auth/signup",
        json={
            "name": "Unique User",
            "username": f"user_{datetime.now().timestamp()}",
            "password": "password123",
            "password_confirm": "password123",
        },
    )
    assert response.status_code == 201


def test_signup_with_duplicate_username(client):
    client.post(
        "api/auth/signup",
        json={
            "name": "Original User",
            "username": "duplicateuser",
            "password": "password123",
            "password_confirm": "password123",
        },
    )
    response = client.post(
        "api/auth/signup",
        json={
            "name": "Another User",
            "username": "duplicateuser",
            "password": "newpassword",
            "password_confirm": "newpassword",
        },
    )
    assert response.status_code == 409
    assert (
        response.json()["detail"] == "User with username `duplicateuser` already exists"
    )


def test_signup_with_invalid_password_confirmation(client):
    response = client.post(
        "api/auth/signup",
        json={
            "name": "Test User",
            "username": "testuser",
            "password": "password123",
            "password_confirm": "wrongpassword",
        },
    )
    assert response.status_code == 422


def test_successful_login(client):
    client.post(
        "api/auth/signup",
        json={
            "name": "Login User",
            "username": "loginuser",
            "password": "password123",
            "password_confirm": "password123",
        },
    )
    response = client.post(
        "api/auth/signin", data={"username": "loginuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_with_invalid_credentials(client):
    response = client.post(
        "api/auth/signin", data={"username": "wronguser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_refresh_token_with_invalid_token(client):
    response = client.post(
        "api/auth/refresh",
        json={"refresh_token": "invalidtoken"},
        headers={"Authorization": "Bearer invalidtoken"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
