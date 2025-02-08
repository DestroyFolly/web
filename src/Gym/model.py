from __future__ import annotations

from pydantic import BaseModel


class Gym(BaseModel):
    id: int | None = None
    adress: str | None = None
    time: str | None = None
    phone: int | None = None
