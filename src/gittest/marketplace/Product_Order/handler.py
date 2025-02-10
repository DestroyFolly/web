from __future__ import annotations

from flask import Blueprint
from flask import Response
from flask import make_response
from flask import request
from flask import url_for

from marketplace.BD.ORM import ProductOrderDB
from marketplace.BD.session import SessionMaker
from marketplace.Logger.loger import logger
from marketplace.Product_Order.dto import CODE_SUCCESS
from marketplace.Product_Order.dto import ProductOrderRequest
from marketplace.Product_Order.dto import ProductOrderResponse
from marketplace.Product_Order.dto import ProductsOrderResponse
from marketplace.Product_Order.repository import ProductOrderRepository
from marketplace.Product_Order.service import ProductOrderService
from marketplace.View.View import View


product_order_page = Blueprint("product_order_page", __name__)


class ProductOrderHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = ProductOrderDB
        self.repo = ProductOrderRepository(self.table, self.session_maker)
        self.service = ProductOrderService(self.repo, self.logger)

    @staticmethod
    @product_order_page.route('/create_product_order/<order_id>', methods=['GET', 'POST'])
    async def create_product_order(order_id: int) -> Response:
        if request.method == "POST":
            req = ProductOrderRequest(request.form)
            req.order_id = order_id
            result = await ProductOrderHandler().get_service().create(req.get_product_order())
            res = ProductOrderResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("product_order_create.html", order_id=order_id), CODE_SUCCESS)

    @staticmethod
    @product_order_page.route('/create_product_order', methods=['GET', 'POST'])
    async def create_product_order_admin() -> Response:
        if request.method == "POST":
            req = ProductOrderRequest(request.form)
            result = await ProductOrderHandler().get_service().create(req.get_product_order())
            res = ProductOrderResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("product_order_create_admin.html"), CODE_SUCCESS)

    @staticmethod
    @product_order_page.route('/delete_product_order/<order_id>', methods=['GET', 'POST'])
    async def delete_product_order(order_id: int) -> Response:
        if request.method == "POST":
            req = ProductOrderRequest(request.form)
            result = await ProductOrderHandler().get_service().delete(req.product_id, order_id)
            res = ProductOrderResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("product_order_delete.html", order_id=order_id), CODE_SUCCESS)

    @staticmethod
    @product_order_page.route('/delete_product_order', methods=['GET', 'POST'])
    async def delete_product_order_admin() -> Response:
        if request.method == "POST":
            req = ProductOrderRequest(request.form)
            result = await ProductOrderHandler().get_service().delete(req.product_id, req.order_id)
            res = ProductOrderResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("product_order_delete_admin.html"), CODE_SUCCESS)

    @staticmethod
    @product_order_page.route('/update_product_order/<order_id>', methods=['GET', 'POST'])
    async def update_product_order(order_id: int) -> Response:
        if request.method == "POST":
            req = ProductOrderRequest(request.form)
            req.order_id = order_id
            result = await ProductOrderHandler().get_service().update(req.get_product_order())
            res = ProductOrderResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("product_order_update.html", order_id=order_id), CODE_SUCCESS)

    @staticmethod
    @product_order_page.route('/update_product_order', methods=['GET', 'POST'])
    async def update_product_order_admin() -> Response:
        if request.method == "POST":
            req = ProductOrderRequest(request.form)
            result = await ProductOrderHandler().get_service().update(req.get_product_order())
            res = ProductOrderResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("product_order_update_admin.html"), CODE_SUCCESS)

    @staticmethod
    @product_order_page.route('/get_products_order_by_id/<order_id>', methods=['GET'])
    async def get_products_order_by_id(order_id: int) -> list[Response] | Response:
        result = await ProductOrderHandler().get_service().get_products_order_by_id(order_id)
        res = ProductsOrderResponse(result)
        return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)

    @staticmethod
    @product_order_page.route('/get_products_order_by_id', methods=['GET', 'POST'])
    async def get_products_order_by_id_admin() -> list[Response] | Response:
        if request.method == "POST":
            req = ProductOrderRequest(request.form)
            return View.redirect(url_for("product_order_page.get_products_order_by_id", order_id=req.order_id))
        return make_response(View.render_template("get_products_order_by_id.html"), CODE_SUCCESS)

    def get_service(self) -> ProductOrderService:
        return self.service
