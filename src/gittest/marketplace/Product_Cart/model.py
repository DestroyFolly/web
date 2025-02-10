from __future__ import annotations

from pydantic import BaseModel


class ProductCart(BaseModel):
    product_id: int | None = None
    cart_id: int | None = None
    quantity: int | str | None = None
