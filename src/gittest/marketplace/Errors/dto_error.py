from __future__ import annotations

from typing import Any
from fastapi import Response, Depends
import json
from functools import wraps


class Error:
    def __init__(self, error_description: str | None = None, error_code: int | None = 404) -> None:
        self.error_description = error_description
        self.error_code = error_code

    def __eq__(self, other: Any) -> bool:
        return self.error_description == other.error_description

    def __repr__(self) -> str:
        return f"Ошибка: {self.error_description}"

    def response(self) -> Response:
        return Response(json.dumps(self.error_description), self.error_code, media_type='application/json')

    @staticmethod
    def try_except_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except:
                return Error("Internal Server Error", 500).response()
        return wrapper
