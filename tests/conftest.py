import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.session import Base
from src.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the testing database
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def get_db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db_session] = get_db_session


@pytest.fixture(scope="function")
def client():
    """Fixture for test client"""
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def access_token(client):
    """Fixture for getting access token"""
    client.post(
        "api/auth/signup",
        json={
            "name": "John Doe",
            "username": "johndoe",
            "password": "password123",
            "password_confirm": "password123",
        },
    )
    response = client.post(
        "api/auth/signin", data={"username": "johndoe", "password": "password123"}
    )
    return response.json()["access_token"]


def create_receipt(client, access_token):
    """Helper function to create a receipt and return the response"""
    receipt_data = {
        "products": [
            {"name": "Item 1", "price": 10.5, "quantity": 2},
            {"name": "Item 2", "price": 5.75, "quantity": 3},
        ],
        "payment": {"amount": 50, "type": "cash"},
    }
    response = client.post(
        "/api/receipts",
        json=receipt_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="function")
def receipt_id(client, access_token):
    """Fixture for creating a receipt and returning its ID"""
    receipt = create_receipt(client, access_token)
    return receipt["id"]


@pytest.fixture(scope="function")
def receipt_public_id(client, access_token):
    """Fixture for creating a receipt and returning its public ID"""
    receipt = create_receipt(client, access_token)
    return receipt["public_id"]
