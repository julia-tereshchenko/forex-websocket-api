import pytest
import httpx

invalid_data_samples = [
    ({"stocks": "GBPUSD"}, "Field required"),
    ({"quantity": 5.0}, "Field required"),
    ({"stocks": "EURJPY", "quantity": "five"}, "Input should be a valid number, unable to parse string as a number"),
    ({"stocks": 12345, "quantity": 12345.0}, "Input should be a valid string"),
    ({"stocks": "CNY", "quantity": -5.0}, "Input should be greater than 0"),
    ({"stocks": "", "quantity": 100}, "String should have at least 1 characters")
]


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_data, reason", invalid_data_samples)
async def test_create_order_invalid_data(invalid_data, reason):
    url = "http://forexapi_container:8000/orders"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=invalid_data)

    assert response.status_code == 422, f"Expected a 422 Unprocessable Entity response for: {reason}"

    is_message_present = reason in response.json()['detail'][0]['msg']
    actual_message = response.json()['detail'][0]['msg']
    assert is_message_present == True, f"Expected '{reason}' but got '{actual_message}' in the response detail for invalid data: {invalid_data}"

