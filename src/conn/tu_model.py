from __future__ import annotations

from pydantic import BaseModel


class TU(BaseModel):
    id: int | None = None
    train_id: int | None = None
    users_id: int | None = None