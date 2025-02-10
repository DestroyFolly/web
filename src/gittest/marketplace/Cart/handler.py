from __future__ import annotations

from flask import Blueprint
from flask import Response
from flask import make_response
from flask import request
from flask import url_for

from marketplace.BD.ORM import CartDB
from marketplace.BD.session import SessionMaker
from marketplace.Cart.dto import CODE_SUCCESS
from marketplace.Cart.dto import CartRequest
from marketplace.Cart.dto import CartResponse
from marketplace.Cart.dto import CartsResponse
from marketplace.Cart.repository import CartRepository
from marketplace.Cart.service import CartService
from marketplace.Logger.loger import logger
from marketplace.View.View import View


cart_page = Blueprint("cart_page", __name__)


class CartHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = CartDB
        self.repo = CartRepository(self.table, self.session_maker)
        self.service = CartService(self.repo, self.logger)

    @staticmethod
    @cart_page.route('/get_cart_by_id/<cart_id>', methods=['GET'])
    async def get_cart_by_id(cart_id: int) -> Response:
        result = await CartHandler().get_service().get_cart_by_id(cart_id)
        res = CartResponse(result)
        return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)

    @staticmethod
    @cart_page.route('/get_cart_by_id', methods=['GET', 'POST'])
    async def get_cart_by_id_admin() -> Response:
        if request.method == "POST":
            req = CartRequest(request.form)
            return View.redirect(url_for("cart_page.get_cart_by_id", cart_id=req.cart_id))
        return make_response(View.render_template("get_cart_by_id.html"), CODE_SUCCESS)

    @staticmethod
    @cart_page.route('/get_all_carts', methods=['GET'])
    async def get_all_carts() -> list[Response] | Response:
        result = await CartHandler().get_service().get_all_carts()
        res = CartsResponse(result)
        return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)

    def get_service(self) -> CartService:
        return self.service
