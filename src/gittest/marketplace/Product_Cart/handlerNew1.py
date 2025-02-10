from __future__ import annotations

from fastapi import APIRouter, Body, Response, Depends
from marketplace.BD.ORM import ProductCartDB
from marketplace.BD.session import SessionMaker
from marketplace.Logger.loger import logger
from marketplace.Product_Cart.dto import ProductCartRequest
from marketplace.Product_Cart.dto import ProductCartResponse
from marketplace.Product_Cart.dto import ProductsCartResponse
from marketplace.Product_Cart.repository import ProductCartRepository
from marketplace.Product_Cart.service import ProductCartService
from marketplace.Connections.my_jwt1 import JwtHandler


product_cart_page = APIRouter()


class ProductCartHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml", port=5001)
        self.table = ProductCartDB
        self.repo = ProductCartRepository(self.table, self.session_maker)
        self.service = ProductCartService(self.repo, self.logger)

    @staticmethod
    @product_cart_page.post('/api/v2/carts/{cart_id}/products/{product_id}')
    @JwtHandler.check_auth_roles()
    async def create_product_cart(cart_id: int, product_id: int, data=Body(), user=Depends(JwtHandler.get_current_user)) -> Response:
        req = ProductCartRequest(data)
        req.cart_id = cart_id
        req.product_id = product_id
        result = await ProductCartHandler().get_service().create(req.get_product_cart())
        return ProductCartResponse(result).response()

    @staticmethod
    @product_cart_page.delete('/api/v2/carts/{cart_id}/products/{product_id}')
    @JwtHandler.check_auth_roles()
    async def delete_product_cart(cart_id: int, product_id: int, user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await ProductCartHandler().get_service().delete(product_id, cart_id)
        return ProductCartResponse(result).response()

    @staticmethod
    @product_cart_page.patch('/api/v2/carts/{cart_id}/products/{product_id}')
    @JwtHandler.check_auth_roles()
    async def update_product_cart(cart_id: int, product_id: int, data=Body(), user=Depends(JwtHandler.get_current_user)) -> Response:
        req = ProductCartRequest(data)
        req.cart_id = cart_id
        req.product_id = product_id
        result = await ProductCartHandler().get_service().update(req.get_product_cart())
        return ProductCartResponse(result).response()

    @staticmethod
    @product_cart_page.get('/api/v2/carts/{cart_id}/products')
    @JwtHandler.check_auth_roles()
    async def get_products_cart_by_id(cart_id: int, user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await ProductCartHandler().get_service().get_products_cart_by_id(cart_id)
        return ProductsCartResponse(result).response()

    def get_service(self) -> ProductCartService:
        return self.service
