from __future__ import annotations

from pydantic import BaseModel


class Trainer(BaseModel):
    id: int | None = None
    first_name: str | None = None
    surname: str | None = None
    gender: str | None = None
    number: int | None = None
    position_id: int
    gym_id: int
