from fastapi.testclient import TestClient

from app.main import app
from app.models import OrderOutput


def test_create_order():

    client = TestClient(app)

    order_payload = {
        "stocks": "EURUSD",
        "quantity": 999.685
    }

    response = client.post("/orders", json=order_payload)

    assert response.status_code == 201, "Status code does not match"

    assert response.headers["content-type"] == "application/json", "Content-Type does not match"

    order_response = OrderOutput(**response.json())

    assert order_response.stocks == order_payload["stocks"], "Traded instrument does not match"
    assert order_response.quantity == order_payload["quantity"], "Quantity does not match"

    valid_statuses = ["pending", "executed", "canceled"]
    assert order_response.status in valid_statuses, "Order status '{order_response.status}' is not valid'"

    assert len(response.content) <= 1_000_000, "The content of the response exceeds 1MB "

    assert response.elapsed.total_seconds() < 1.0, "The response time is over 1 second"

