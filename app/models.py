from __future__ import annotations
from uuid import UUID

from pydantic import BaseModel, Field
from typing import Literal, List, Optional, ForwardRef

class OrderInput(BaseModel):
    stocks: str = Field(..., min_length=1, description="Stock name should have at least one character.")
    quantity: float = Field(..., gt=0, description="Quantity should be greater than 0.")

OrderRef = ForwardRef('OrderOutput')

class OrderOutput(BaseModel):
    id: Optional[UUID]
    stocks: str
    quantity: float
    status: Literal["pending", "executed", "canceled"]


class OrdersList(BaseModel):
    orders: List[OrderOutput]

class Error(BaseModel):
    code: int
    message: str

