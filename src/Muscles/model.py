from __future__ import annotations

from pydantic import BaseModel


class Muscle(BaseModel):
    id: int | None = None
    title: str | None = None
    difficulty: str | None = None
    function: str | None = None
