from __future__ import annotations

from typing import Any

from marketplace.Errors.dto_error import Error
from marketplace.Product_Order.model import ProductOrder
import json
from fastapi import Response

CODE_SUCCESS = 200


class ProductOrderRequest:
    def __init__(self, product_order_data: Any) -> None:
        self.product_id = product_order_data.get("product_id")
        self.quantity = product_order_data.get("quantity")
        self.order_id = product_order_data.get("order_id")

    def get_product_order(self) -> ProductOrder:
        return ProductOrder(product_id=self.product_id, quantity=self.quantity, order_id=self.order_id)


class ProductOrderResponse:
    def __init__(self, data: ProductOrder | Error) -> None:
        if isinstance(data, Error):
            dict_data = {"error": data.error_description}
            error = data.error_code
        else:
            dict_data = {"product_id": str(data.product_id), "quantity": str(data.quantity),
                         "order_id": str(data.order_id)}
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


class ProductsOrderResponse:
    def __init__(self, data: list[ProductOrder] | Error) -> None:
        dicts_data = [{"": ""}] * 0
        if not isinstance(data, Error):
            for elem in data:
                dicts_data.append({"product_id": str(elem.product_id), "quantity": str(elem.quantity),
                                  "order_id": str(elem.order_id)})
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

