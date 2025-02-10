from __future__ import annotations

from typing import Any

from marketplace.Errors.dto_error import Error
from marketplace.Payment.model import Payment
import json
from fastapi import Response

CODE_SUCCESS = 200


class PaymentRequest:
    def __init__(self, payment_data: Any) -> None:
        self.payment_id = payment_data.get("payment_id")
        self.all_price = payment_data.get("all_price")
        self.state = payment_data.get("state")
        self.user_id = payment_data.get("user_id")

    def get_payment(self) -> Payment:
        return Payment(payment_id=self.payment_id, all_price=self.all_price, state=self.state, user_id=self.user_id)


class PaymentResponse:
    def __init__(self, data: Payment | Error) -> None:
        if isinstance(data, Error):
            dict_data = {"error": data.error_description}
            error = data.error_code
        else:
            dict_data = {"payment_id": str(data.payment_id), "all_price": str(data.all_price),
                         "state": str(data.state), "user_id": str(data.user_id)}
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


class PaymentsResponse:
    def __init__(self, data: list[Payment] | Error) -> None:
        dicts_data = [{"": ""}] * 0
        if not isinstance(data, Error):
            for elem in data:
                dicts_data.append({"payment_id": str(elem.payment_id), "all_price": str(elem.all_price),
                                  "state": str(elem.state), "user_id": str(elem.user_id)})
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
