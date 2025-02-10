from __future__ import annotations

from flask import Blueprint
from flask import Response
from flask import make_response
from flask import request

from marketplace.BD.ORM import ProductDB
from marketplace.BD.session import SessionMaker
from marketplace.Logger.loger import logger
from marketplace.Product.dto import CODE_SUCCESS
from marketplace.Product.dto import ProductRequest
from marketplace.Product.dto import ProductResponse
from marketplace.Product.dto import ProductsResponse
from marketplace.Product.repository import ProductRepository
from marketplace.Product.service import ProductService
from marketplace.View.View import View


product_page = Blueprint("product_page", __name__)


class ProductHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = ProductDB
        self.repo = ProductRepository(self.table, self.session_maker)
        self.service = ProductService(self.repo, self.logger)

    @staticmethod
    @product_page.route('/create_product/<seller_id>', methods=['GET', 'POST'])
    async def create_product(seller_id: int) -> Response:
        if request.method == "POST":
            req = ProductRequest(request.form)
            result = await ProductHandler().get_service().create(req.get_product(), seller_id)
            res = ProductResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template('product_create.html', seller_id=seller_id), CODE_SUCCESS)

    @staticmethod
    @product_page.route('/delete_product/<seller_id>', methods=['GET', 'POST'])
    async def delete_product(seller_id: int) -> Response:
        if request.method == "POST":
            req = ProductRequest(request.form)
            if req.product_id in (str(i.product_id) for i in
                                  await ProductHandler().get_service().get_seller_products(seller_id)
                                  if str(i.seller_id) == seller_id):
                result = await ProductHandler().get_service().delete(req.product_id)
                res = ProductResponse(result)
                if res.check_is_error():
                    return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template('product_delete.html', seller_id=seller_id), CODE_SUCCESS)

    @staticmethod
    @product_page.route('/update_product/<seller_id>', methods=['GET', 'POST'])
    async def update_product(seller_id: int) -> Response:
        if request.method == "POST":
            req = ProductRequest(request.form)
            if req.product_id in (str(i.product_id) for i in
                                  await ProductHandler().get_service().get_seller_products(seller_id)
                                  if str(i.seller_id) == seller_id):
                result = await ProductHandler().get_service().update(req.get_product())
                res = ProductResponse(result)
                if res.check_is_error():
                    return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template('product_update.html', seller_id=seller_id), CODE_SUCCESS)

    @staticmethod
    @product_page.route('/get_product_by_id', methods=['GET', 'POST'])
    async def get_product_by_id() -> Response:
        if request.method == "POST":
            req = ProductRequest(request.form)
            result = await ProductHandler().get_service().get_product_by_id(req.product_id)
            res = ProductResponse(result)
            return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)
        return make_response(View.render_template("get_product_by_id.html"), CODE_SUCCESS)

    @staticmethod
    @product_page.route('/get_product_by_title', methods=['GET', 'POST'])
    async def get_product_by_title() -> Response:
        if request.method == "POST":
            req = ProductRequest(request.form)
            result = await ProductHandler().get_service().get_product_by_title(req.title)
            res = ProductResponse(result)
            return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)
        return make_response(View.render_template("get_product_by_title.html"), CODE_SUCCESS)

    @staticmethod
    @product_page.route('/get_all_products', methods=['GET'])
    async def get_all_products() -> list[Response] | Response:
        result = await ProductHandler().get_service().get_all_products()
        res = ProductsResponse(result)
        return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)

    @staticmethod
    @product_page.route('/get_seller_products/<seller_id>', methods=['GET'])
    async def get_seller_products(seller_id: int) -> list[Response] | Response:
        result = await ProductHandler().get_service().get_seller_products(seller_id)
        res = ProductsResponse(result)
        return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)

    def get_service(self) -> ProductService:
        return self.service
