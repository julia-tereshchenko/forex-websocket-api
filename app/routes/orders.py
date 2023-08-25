import asyncio
import random
import uuid

from fastapi import APIRouter, HTTPException, Path
from typing import List

from ..notifications import notify_all_clients
from ..models import OrderInput, OrderOutput

router = APIRouter()

orders_db = {}

@router.get("/orders", response_model=List[OrderOutput])
async def get_orders():
    await asyncio.sleep(random.uniform(0.1, 1))
    return list(orders_db.values())

@router.post("/orders", response_model=OrderOutput, status_code=201)
async def place_order(order: OrderInput):
    await asyncio.sleep(random.uniform(0.1, 1))
    order_id = str(uuid.uuid4())
    random_status = random.choice(["pending", "executed", "canceled"])
    new_order = OrderOutput(id=order_id, stocks=order.stocks, quantity=order.quantity, status=random_status)
    orders_db[order_id] = new_order
    await notify_all_clients(f"Order {order_id} with status {random_status} has been created.")
    return new_order

@router.get("/orders/{order_id}", response_model=OrderOutput)
async def get_order(order_id: str = Path(..., description="The UUID of the order to get")):
    try:
        uuid.UUID(order_id)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Invalid ID",
                "details": "The provided ID does not match the UUID format."
            }
        )

    await asyncio.sleep(random.uniform(0.1, 1))

    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail={"error": "Order not found", "message": "Order not found"})
    return order


@router.delete("/orders/{order_id}", status_code=204)
async def cancel_order(order_id: str):
    await asyncio.sleep(random.uniform(0.1, 1))

    try:
        uuid.UUID(order_id, version=4)
    except ValueError:
        raise HTTPException(status_code=400, detail={"code": 400, "message": "Invalid UUID format"})

    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail={"code": 404, "message": "Order not found"})
    del orders_db[order_id]

    await notify_all_clients(f"Order {order_id} status = deleted.")
    pass

