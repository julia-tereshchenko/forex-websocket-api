from fastapi.testclient import TestClient
from app.main import app

def test_delete_order():

    client = TestClient(app)

    order_payload = {
        "stocks": "EURUSD",
        "quantity": 100.5
    }
    create_response = client.post("/orders", json=order_payload)
    assert create_response.status_code == 201, "Failed to create the order."

    order_id = create_response.json().get("id")

    response = client.delete(f"/orders/{order_id}")

    assert response.status_code == 204, "Status code does not match for DELETE operation"

    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 404, "Order still exists after deletion"

    second_delete_response = client.delete(f"/orders/{order_id}")
    assert second_delete_response.status_code in [204, 404], "Second DELETE operation for the same order is not idempotent"


    if response.content:
        assert response.headers["content-type"] == "application/json", "Content-Type does not match for DELETE operation"


    assert response.elapsed.total_seconds() < 1, "The response time for DELETE operation is over 1 second"
