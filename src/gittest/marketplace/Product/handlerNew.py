from __future__ import annotations
from fastapi import APIRouter, Body, Response, Depends

from marketplace.BD.ORM import ProductDB
from marketplace.BD.session import SessionMaker
from marketplace.Logger.loger import logger
from marketplace.Product.dto import ProductRequest
from marketplace.Product.dto import ProductResponse
from marketplace.Product.dto import ProductsResponse
from marketplace.Product.repository import ProductRepository
from marketplace.Product.service import ProductService
from marketplace.Errors.dto_error import Error
from marketplace.Connections.my_jwt import JwtHandler


product_page = APIRouter()


class ProductHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = ProductDB
        self.repo = ProductRepository(self.table, self.session_maker)
        self.service = ProductService(self.repo, self.logger)

    @staticmethod
    @product_page.post('/api/v2/products')
    @JwtHandler.check_auth_roles(roles=["seller", "admin"])
    async def create_product(data=Body(), user=Depends(JwtHandler.get_current_user)) -> Response:
        req = ProductRequest(data)
        result = await ProductHandler().get_service().create(req.get_product(), req.seller_id)
        return ProductResponse(result).response()

    @staticmethod
    @product_page.delete('/api/v2/products/{product_id}')
    @JwtHandler.check_auth_roles(roles=["seller", "admin"])
    async def delete_product(product_id: int, user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await ProductHandler().get_service().delete(product_id)
        return ProductResponse(result).response()

    @staticmethod
    @product_page.patch('/api/v2/products/{product_id}')
    @JwtHandler.check_auth_roles(roles=["seller", "admin"])
    async def update_product(product_id: int, data=Body(), user=Depends(JwtHandler.get_current_user)) -> Response:
        req = ProductRequest(data)
        req.product_id = product_id
        result = await ProductHandler().get_service().update(req.get_product())
        return ProductResponse(result).response()

    @staticmethod
    @product_page.get('/api/v2/products/id/{product_id}')
    @JwtHandler.check_auth_roles()
    async def get_product_by_id(product_id: int, user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await ProductHandler().get_service().get_product_by_id(product_id)
        return ProductResponse(result).response()

    @staticmethod
    @product_page.get('/api/v2/products/title/{title}')
    @JwtHandler.check_auth_roles()
    async def get_product_by_title(title: str, user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await ProductHandler().get_service().get_product_by_title(title)
        return ProductResponse(result).response()

    @staticmethod
    @product_page.get('/api/v2/products')
    @JwtHandler.check_auth_roles()
    async def get_all_products(user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await ProductHandler().get_service().get_all_products()
        return ProductsResponse(result).response()

    def get_service(self) -> ProductService:
        return self.service
