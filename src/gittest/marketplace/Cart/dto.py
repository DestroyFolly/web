from __future__ import annotations

from typing import Any

from marketplace.Cart.model import Cart
from marketplace.Errors.dto_error import Error
import json
from fastapi import Response

CODE_SUCCESS = 200


class CartRequest:
    def __init__(self, cart_data: Any) -> None:
        self.cart_id = cart_data.get("cart_id")
        self.all_price = cart_data.get("all_price")
        self.user_id = cart_data.get("user_id")

    def get_cart(self) -> Cart:
        return Cart(cart_id=self.cart_id, all_price=self.all_price, user_id=self.user_id)


class CartResponse:
    def __init__(self, data: Cart | Error) -> None:
        if isinstance(data, Error):
            dict_data = {"error": data.error_description}
            error = data.error_code
        else:
            dict_data = {"cart_id": str(data.cart_id), "all_price": str(data.all_price), "user_id": str(data.user_id)}
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


class CartsResponse:
    def __init__(self, data: list[Cart] | Error) -> None:
        dicts_data = [{"": ""}] * 0
        if not isinstance(data, Error):
            for elem in data:
                dicts_data.append({"cart_id": str(elem.cart_id), "all_price": str(elem.all_price),
                                  "user_id": str(elem.user_id)})
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
