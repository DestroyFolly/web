from __future__ import annotations

from pydantic import BaseModel


class Order(BaseModel):
    order_id: int | None = None
    all_price: float | str | None = None
    address: str | None = None
    user_id: int | None = None
