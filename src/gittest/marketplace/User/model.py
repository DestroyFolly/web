from __future__ import annotations

from pydantic import BaseModel


class User(BaseModel):
    user_id: int | None = None
    fio: str | None = None
    email: str | None = None
    password: str | None = None
    money: float | str | None = None
    address: str | None = None
    phone: str | None = None
    role: str | None = None
