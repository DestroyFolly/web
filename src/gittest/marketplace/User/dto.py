from __future__ import annotations

from typing import Any
import json
from marketplace.Errors.dto_error import Error
from marketplace.User.model import User
from fastapi import Response

CODE_SUCCESS = 200


class UserRequest:
    def __init__(self, user_data: Any) -> None:
        self.user_id = user_data.get("user_id")
        self.fio = user_data.get("fio")
        self.email = user_data.get("email")
        self.password = user_data.get("password")
        self.money = user_data.get("money", 0.0)
        self.address = user_data.get("address")
        self.phone = user_data.get("phone")
        self.role = user_data.get("role", "user")

    def get_user(self) -> User:
        return User(user_id=self.user_id, fio=self.fio, email=self.email, password=self.password,
                    money=self.money, address=self.address, phone=self.phone, role=self.role)


class UserResponse:
    def __init__(self, data: User | Error) -> None:
        if isinstance(data, Error):
            dict_data = {"error": data.error_description}
            error = data.error_code
        else:
            dict_data = {"user_id": str(data.user_id), "fio": str(data.fio), "email": str(data.email),
                         "password": str(data.password), "money": str(data.money), "address": str(data.address),
                         "phone": str(data.phone), "role": str(data.role)}
            error = CODE_SUCCESS

        self.data = dict_data
        self.error = error

    def check_is_error(self) -> bool:
        return self.error != CODE_SUCCESS

    def get_description_error(self) -> str | None:
        return json.dumps(self.data.get("error"))

    def get_string_info(self) -> str:
        str_result = ""
        for key in self.data:
            str_result += f"{key}: {self.data[key]} <br />"
        return str_result

    def get_data(self) -> str | None:
        return json.dumps(self.data)

    def response(self):
        if self.check_is_error():
            return Response(self.get_description_error(), self.error, media_type='application/json')
        return Response(self.get_data(), self.error, media_type='application/json')


class UsersResponse:
    def __init__(self, data: list[User] | Error) -> None:
        dicts_data = [{"": ""}] * 0
        if not isinstance(data, Error):
            for elem in data:
                dicts_data.append({"user_id": str(elem.user_id), "fio": str(elem.fio), "email": str(elem.email),
                                   "password": str(elem.password), "money": str(elem.money),
                                   "address": str(elem.address), "phone": str(elem.phone), "role": str(elem.role)})
            error = CODE_SUCCESS
        else:
            dicts_data.append({"error": data.error_description})
            error = data.error_code

        self.data = dicts_data
        self.error = error

    def check_is_error(self) -> bool:
        return self.error != CODE_SUCCESS

    def get_description_error(self) -> str | None:
        return json.dumps(self.data[0].get("error"))

    def get_string_info(self) -> str:
        str_result = ""
        elem = 1
        for data in self.data:
            str_result += f"№{elem}<br />"
            for key in data:
                str_result += f"{key}: {data[key]} <br />"
            str_result += "<br />"
            elem += 1
        return str_result

    def get_data(self) -> str | None:
        return json.dumps(self.data)

    def response(self):
        if self.check_is_error():
            return Response(self.get_description_error(), self.error, media_type='application/json')
        return Response(self.get_data(), self.error, media_type='application/json')

