import pytest
import httpx
import websockets

@pytest.mark.asyncio
async def test_websocket_order_status_events():
    URI = "ws://forexapi_container:8000/ws"
    async with websockets.connect(URI, extra_headers={"Origin": "http://forexapi_container:8000"}) as ws:

        async with httpx.AsyncClient() as client:
            response = await client.post("http://forexapi_container:8000/orders", json={
                "stocks": "USDEUR",
                "quantity": 5.0
            })
            assert response.status_code == 201
            created_order = response.json()

        message = await ws.recv()

        assert message == f"Order {created_order['id']} with status {created_order['status']} has been created."


