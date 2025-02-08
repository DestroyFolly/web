from __future__ import annotations

from pydantic import BaseModel


class Train(BaseModel):
    id: int | None = None
    title: str | None = None
    times: str | None = None
    dates: str | None = None
    trainer_id: int
    gym_id: int
