from fastapi import WebSocket
from typing import List

active_connections: List[WebSocket] = []

async def notify_all_clients(message: str):
    for connection in active_connections:
        await connection.send_text(message)