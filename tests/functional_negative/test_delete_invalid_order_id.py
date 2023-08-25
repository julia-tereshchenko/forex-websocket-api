import pytest
import httpx

invalid_ids = [
    ("12345", "Invalid UUID format"),
    ("not-a-uuid", "Invalid UUID format"),
    ("abcd-efgh-ijkl-mnop", "Invalid UUID format")
]

@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_id, reason", invalid_ids)
async def test_delete_order_invalid_id_format(invalid_id, reason):

    url = f"http://forexapi_container:8000/orders/{invalid_id}"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url)

    assert response.status_code == 400, f"Expected a 400 Bad Request response for: {reason}"

    is_message_present = reason in response.json()['detail']['message']
    actual_message = response.json()['detail']['message']
    assert is_message_present == True, f"Expected '{reason}' but got '{actual_message}' for invalid ID: {invalid_id}"

