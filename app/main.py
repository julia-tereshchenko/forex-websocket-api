import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .routes.orders import router as orders_router
from .notifications import active_connections

app = FastAPI()
app.include_router(orders_router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Forex Trading API!",
        "available_endpoints": {
            "/orders": {
                "methods": ["GET", "POST"],
                "description": "Retrieve all orders or place a new order."
            },
            "/orders/{orderId}": {
                "methods": ["GET", "DELETE"],
                "description": "Retrieve a specific order by its ID or delete an order by its ID."
            },
            "/ws": {
                "methods": ["GET"],
                "description": "WebSocket connection for real-time order information."
            }
        }
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({'error': 'Invalid data format'}))
    except WebSocketDisconnect:
        active_connections.remove(websocket)