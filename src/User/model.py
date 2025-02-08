from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class Userrole(Enum):
    Admin = "admin"
    Customer = "trainer"
    Seller = "client"

class User(BaseModel):
    id: int
    phone: int
    email: str
    first_name: str
    surname: str
    password: str
    role: str
    gender: str



