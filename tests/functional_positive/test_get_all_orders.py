from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import app
from app.models import OrdersList


def test_get_all_orders():

    client = TestClient(app)

    response = client.get("/orders")

    assert response.status_code == 200, "Status code does not match"

    assert response.headers["content-type"] == "application/json", "Content-Type does not match"

    try:
        _ = OrdersList(orders=response.json())
    except ValidationError as e:
        assert False, f"Response schema validation failed with error: {e}"

    assert len(response.content) <= 1_000_000, "The content of the response exceeds 1MB"

    assert response.elapsed.total_seconds() < 1.0, "The response time is over 1 second"

