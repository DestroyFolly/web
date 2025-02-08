from __future__ import annotations

from pydantic import BaseModel


class Exercise(BaseModel):
    id: int | None = None
    name: str | None = None
    group: str | None = None
    difficulty: str | None = None
    muscles_id: int | None = None

