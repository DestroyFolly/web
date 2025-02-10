from __future__ import annotations

from pydantic import BaseModel


class Cart(BaseModel):
    cart_id: int | None = None
    all_price: float | str | None = None
    user_id: int | None = None
