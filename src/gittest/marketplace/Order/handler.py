from __future__ import annotations

from flask import Blueprint
from flask import Response
from flask import make_response
from flask import request
from flask import url_for

from marketplace.BD.ORM import OrderDB
from marketplace.BD.session import SessionMaker
from marketplace.Logger.loger import logger
from marketplace.Order.dto import CODE_SUCCESS
from marketplace.Order.dto import OrderRequest
from marketplace.Order.dto import OrderResponse
from marketplace.Order.dto import OrdersResponse
from marketplace.Order.repository import OrderRepository
from marketplace.Order.service import OrderService
from marketplace.View.View import View


order_page = Blueprint("order_page", __name__)


class OrderHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = OrderDB
        self.repo = OrderRepository(self.table, self.session_maker)
        self.service = OrderService(self.repo, self.logger)

    @staticmethod
    @order_page.route('/update_order/<order_id>', methods=['GET', 'POST'])
    async def update_order(order_id: int) -> Response:
        if request.method == "POST":
            req = OrderRequest(request.form)
            req.order_id = order_id
            result = await OrderHandler().get_service().update(req.get_order())
            res = OrderResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("order_update.html", order_id=order_id), CODE_SUCCESS)

    @staticmethod
    @order_page.route('/update_order', methods=['GET', 'POST'])
    async def update_order_admin() -> Response:
        if request.method == "POST":
            req = OrderRequest(request.form)
            result = await OrderHandler().get_service().update(req.get_order())
            res = OrderResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("order_update_admin.html"), CODE_SUCCESS)

    @staticmethod
    @order_page.route('/get_order_by_id/<order_id>', methods=['GET'])
    async def get_order_by_id(order_id: int) -> Response:
        result = await OrderHandler().get_service().get_order_by_id(order_id)
        res = OrderResponse(result)
        return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)

    @staticmethod
    @order_page.route('/get_order_by_id', methods=['GET', 'POST'])
    async def get_order_by_id_admin() -> Response:
        if request.method == "POST":
            req = OrderRequest(request.form)
            return View.redirect(url_for("order_page.get_order_by_id", order_id=req.order_id))
        return make_response(View.render_template("get_order_by_id.html"), CODE_SUCCESS)

    @staticmethod
    @order_page.route('/get_all_orders', methods=['GET'])
    async def get_all_orders() -> list[Response] | Response:
        result = await OrderHandler().get_service().get_all_orders()
        res = OrdersResponse(result)
        return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)

    def get_service(self) -> OrderService:
        return self.service
