from __future__ import annotations

from typing import Any

from flask import Response
from flask import jsonify
from flask import make_response

from User.model import User


class UserRequest:
    def __init__(self, user_data: Any) -> None:
        self.id = user_data.get("id")
        self.gender = user_data.get("gender")
        self.email = user_data.get("email")
        self.password = user_data.get("password")
        self.first_name = user_data.get("first_name")
        self.surname = user_data.get("surname")
        self.phone = user_data.get("phone")
        self.role = user_data.get("role")

    def get_user(self) -> User:
        return User(id=self.id, gender=self.gender, email=self.email, password=self.password,
                    first_name=self.first_name, surname=self.surname, phone=self.phone, role=self.role)


class UserResponse:
    def __init__(self, data: User | None) -> None:
        print(data)
        if data == 'User not found':
            error = 1
            print("Error")
            dict_data = {"error": 'Empty user data'}
        elif data == 'User already registered':
            error = 1
            print("Error")
            dict_data = {"error": 'Already registered'}
        else:
            dict_data = {"id": data.id, "gender": str(data.gender), "email": str(data.email),
                         "password": str(data.password), "first_name": str(data.first_name), "surname": str(data.surname),
                         "phone": data.phone, "role": str(data.role)}
            error = 0


        self.data = jsonify(dict_data)
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.data, self.error)


class UsersResponse:
    def __init__(self, data: list[User] | None) -> None:
        dict_data = [{"": ""}] * 0
        if not data:
            for elem in data:
                dict_data.append({"id": str(elem.id), "gender": str(elem.gender), "email": str(elem.email),
                                  "password": str(elem.password), "first_name": str(elem.first_name),
                                  "surname": str(elem.surname), "phone": str(elem.phone), "role": str(elem.role)})
            error = 0
        else:
            error = 1
            dict_data = {"error": 'Empty user data'}

        self.data = jsonify(dict_data[0]) if dict_data[0].get("error") else jsonify(dict_data)
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.json_data, self.error)