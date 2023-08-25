import pytest
import httpx
import uuid

non_existent_order_samples = [
    (str(uuid.uuid4()), {'detail': {"error": "Order not found", "message": "Order not found"}})
]


@pytest.mark.asyncio
@pytest.mark.parametrize("order_id, expected_response", non_existent_order_samples)
async def test_get_non_existent_order(order_id, expected_response):
    url = f"http://forexapi_container:8000/orders/{order_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    response_json = response.json()
    assert response.status_code == 404, f"Expected a 404 Not Found response for non-existent order ID: {order_id}"
    assert expected_response["detail"]["error"] == response_json["detail"]["error"]
    assert expected_response["detail"]["message"] == response_json["detail"]["message"]


