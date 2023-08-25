import asyncio
import pytest
import websockets
import json


@pytest.mark.asyncio
async def test_send_malformed_data():
    uri = "ws://forexapi_container:8000/ws"

    async with websockets.connect(uri) as websocket:

        await websocket.send("This is not a valid JSON")

        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=10)
        except websockets.exceptions.ConnectionClosed:
            pytest.fail("Server closed the connection unexpectedly.")
        except asyncio.TimeoutError:
            pytest.fail("Server did not respond in time.")

        data = json.loads(response)

        assert data['error'] == "Invalid data format"
