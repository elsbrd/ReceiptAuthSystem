from datetime import datetime
from uuid import uuid4


def test_create_receipt(client, access_token):
    # Data for creating a receipt
    receipt_data = {
        "products": [
            {"name": "Item 1", "price": 10.5, "quantity": 2},
            {"name": "Item 2", "price": 5.75, "quantity": 3},
        ],
        "payment": {"amount": 50, "type": "cash"},
    }

    # Make the request to create a receipt
    response = client.post(
        "/api/receipts",
        json=receipt_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["total"] == 38.25
    assert response_data["rest"] == 11.75
    assert len(response_data["products"]) == 2


def test_create_receipt_invalid_data(client, access_token):
    # Invalid receipt data (missing payment amount)
    receipt_data = {
        "products": [
            {"name": "Item 1", "price": 10.5, "quantity": 2},
        ],
        "payment": {"type": "cash"},
    }

    response = client.post(
        "/api/receipts",
        json=receipt_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 422  # Unprocessable Entity


def test_get_receipt_by_id(client, access_token, receipt_id):
    response = client.get(
        f"/api/receipts/{receipt_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["id"] == receipt_id


def test_view_receipt_by_public_id(client, access_token, receipt_public_id):
    response = client.get(
        f"/api/receipts/{receipt_public_id}/view",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.text, str)  # Response is plain text


def test_get_non_existent_receipt_by_id(client, access_token):
    non_existent_receipt_id = 999999

    response = client.get(
        f"/api/receipts/{non_existent_receipt_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Receipt not found"


def test_list_receipts(client, access_token):
    response = client.get(
        "/api/receipts?limit=5&offset=0",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data["receipts"], list)
    assert "total_count" in response_data


def test_list_receipts_with_filters(client, access_token):
    # Listing receipts with a minimum total filter
    response = client.get(
        "/api/receipts?minimum_total=30.00",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    response_data = response.json()
    assert all(receipt["total"] >= 30 for receipt in response_data["receipts"])


def test_view_non_existent_receipt_by_public_id(client, access_token):
    non_existent_public_id = str(uuid4())

    response = client.get(
        f"/api/receipts/{non_existent_public_id}/view",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Receipt not found"
