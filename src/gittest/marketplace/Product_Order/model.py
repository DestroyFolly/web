from __future__ import annotations

from pydantic import BaseModel


class ProductOrder(BaseModel):
    product_id: int | None = None
    order_id: int | None = None
    quantity: int | str | None = None
