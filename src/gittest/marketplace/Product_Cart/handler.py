from __future__ import annotations

from flask import Blueprint
from flask import Response
from flask import make_response
from flask import request
from flask import url_for

from marketplace.BD.ORM import ProductCartDB
from marketplace.BD.session import SessionMaker
from marketplace.Logger.loger import logger
from marketplace.Product_Cart.dto import CODE_SUCCESS
from marketplace.Product_Cart.dto import ProductCartRequest
from marketplace.Product_Cart.dto import ProductCartResponse
from marketplace.Product_Cart.dto import ProductsCartResponse
from marketplace.Product_Cart.repository import ProductCartRepository
from marketplace.Product_Cart.service import ProductCartService
from marketplace.View.View import View


product_cart_page = Blueprint("product_cart_page", __name__)


class ProductCartHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = ProductCartDB
        self.repo = ProductCartRepository(self.table, self.session_maker)
        self.service = ProductCartService(self.repo, self.logger)

    @staticmethod
    @product_cart_page.route('/create_product_cart/<cart_id>', methods=['GET', 'POST'])
    async def create_product_cart(cart_id: int) -> Response:
        if request.method == "POST":
            req = ProductCartRequest(request.form)
            req.cart_id = cart_id
            result = await ProductCartHandler().get_service().create(req.get_product_cart())
            res = ProductCartResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("product_cart_create.html", cart_id=cart_id), CODE_SUCCESS)

    @staticmethod
    @product_cart_page.route('/create_product_cart', methods=['GET', 'POST'])
    async def create_product_cart_admin() -> Response:
        if request.method == "POST":
            req = ProductCartRequest(request.form)
            result = await ProductCartHandler().get_service().create(req.get_product_cart())
            res = ProductCartResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("product_cart_create_admin.html"), CODE_SUCCESS)

    @staticmethod
    @product_cart_page.route('/delete_product_cart/<cart_id>', methods=['GET', 'POST'])
    async def delete_product_cart(cart_id: int) -> Response:
        if request.method == "POST":
            req = ProductCartRequest(request.form)
            result = await ProductCartHandler().get_service().delete(req.product_id, cart_id)
            res = ProductCartResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("product_cart_delete.html", cart_id=cart_id), CODE_SUCCESS)

    @staticmethod
    @product_cart_page.route('/delete_product_cart', methods=['GET', 'POST'])
    async def delete_product_cart_admin() -> Response:
        if request.method == "POST":
            req = ProductCartRequest(request.form)
            result = await ProductCartHandler().get_service().delete(req.product_id, req.cart_id)
            res = ProductCartResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("product_cart_delete_admin.html"), CODE_SUCCESS)

    @staticmethod
    @product_cart_page.route('/update_product_cart/<cart_id>', methods=['GET', 'POST'])
    async def update_product_cart(cart_id: int) -> Response:
        if request.method == "POST":
            req = ProductCartRequest(request.form)
            req.cart_id = cart_id
            result = await ProductCartHandler().get_service().update(req.get_product_cart())
            res = ProductCartResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("product_cart_update.html", cart_id=cart_id), CODE_SUCCESS)

    @staticmethod
    @product_cart_page.route('/update_product_cart', methods=['GET', 'POST'])
    async def update_product_cart_admin() -> Response:
        if request.method == "POST":
            req = ProductCartRequest(request.form)
            result = await ProductCartHandler().get_service().update(req.get_product_cart())
            res = ProductCartResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("product_cart_update_admin.html"), CODE_SUCCESS)

    @staticmethod
    @product_cart_page.route('/get_products_cart_by_id/<cart_id>', methods=['GET'])
    async def get_products_cart_by_id(cart_id: int) -> list[Response] | Response:
        result = await ProductCartHandler().get_service().get_products_cart_by_id(cart_id)
        res = ProductsCartResponse(result)
        return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)

    @staticmethod
    @product_cart_page.route('/get_products_cart_by_id', methods=['GET', 'POST'])
    async def get_products_cart_by_id_admin() -> list[Response] | Response:
        if request.method == "POST":
            req = ProductCartRequest(request.form)
            return View.redirect(url_for("product_cart_page.get_products_cart_by_id", cart_id=req.cart_id))
        return make_response(View.render_template("get_products_cart_by_id.html"), CODE_SUCCESS)

    def get_service(self) -> ProductCartService:
        return self.service
