from __future__ import annotations

from pydantic import BaseModel


class Product(BaseModel):
    product_id: int | None = None
    seller_id: int | None = None
    title: str | None = None
    price: float | str | None = None
    rate: float | str | None = None
