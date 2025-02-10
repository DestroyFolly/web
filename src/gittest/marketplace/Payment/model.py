from __future__ import annotations

from pydantic import BaseModel


class Payment(BaseModel):
    payment_id: int | None = None
    all_price: float | str | None = None
    state: str | None = None
    user_id: int | None = None
