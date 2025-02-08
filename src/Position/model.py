from __future__ import annotations

from pydantic import BaseModel


class Position(BaseModel):
    id: int | None = None
    title: str | None = None
    function: str | None = None
    experience: int | None = None
