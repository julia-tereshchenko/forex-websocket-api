import pytest
import httpx

invalid_id_samples = [
    # Equivalence Class: Too Short/Long UUIDs
    ("12345678-1234-1234-1234-1234567890123", {"detail": {"error": "Invalid ID", "details": "The provided ID does not match the UUID format."}}),  
    ("12345678-1234-1234-1234", {"detail": {"error": "Invalid ID", "details": "The provided ID does not match the UUID format."}}),

    # Equivalence Class: UUIDs with Invalid Characters
    ("12345678-1234-123z-1234-123456789012", {"detail": {"error": "Invalid ID", "details": "The provided ID does not match the UUID format."}}),
    ("g47ac10b-58cc-4372-a567-0e02b2c3d479", {"detail": {"error": "Invalid ID", "details": "The provided ID does not match the UUID format."}}),

    # Boundary Testing
    ("z"*32, {"detail": {"error": "Invalid ID", "details": "The provided ID does not match the UUID format."}}),
    ("1", {"detail": {"error": "Invalid ID", "details": "The provided ID does not match the UUID format."}}),
]

@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_id, expected_response", invalid_id_samples)
async def test_get_order_invalid_id(invalid_id, expected_response):
    url = f"http://forexapi_container:8000/orders/{invalid_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    response_json = response.json()

    assert expected_response["detail"]["error"] == response_json["detail"]["error"]
    assert expected_response["detail"]["details"] == response_json["detail"]["details"]
    assert response.status_code == 422, f"Expected a 422 Unprocessable Entity response for: {invalid_id}"
