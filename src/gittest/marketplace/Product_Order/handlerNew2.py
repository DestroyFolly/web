from __future__ import annotations

from fastapi import APIRouter, Body, Response, Depends
from marketplace.BD.ORM import ProductOrderDB
from marketplace.BD.session import SessionMaker
from marketplace.Logger.loger import logger
from marketplace.Product_Order.dto import ProductOrderRequest
from marketplace.Product_Order.dto import ProductOrderResponse
from marketplace.Product_Order.dto import ProductsOrderResponse
from marketplace.Product_Order.repository import ProductOrderRepository
from marketplace.Product_Order.service import ProductOrderService
from marketplace.Connections.my_jwt2 import JwtHandler


product_order_page = APIRouter()


class ProductOrderHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml", port=8099)
        self.table = ProductOrderDB
        self.repo = ProductOrderRepository(self.table, self.session_maker)
        self.service = ProductOrderService(self.repo, self.logger)

    @staticmethod
    @product_order_page.post('/api/v2/orders/{order_id}/products/{product_id}')
    @JwtHandler.check_auth_roles()
    async def create_product_order(order_id: int, product_id: int, data=Body(), user=Depends(JwtHandler.get_current_user)) -> Response:
        req = ProductOrderRequest(data)
        req.order_id = order_id
        req.product_id = product_id
        result = await ProductOrderHandler().get_service().create(req.get_product_order())
        return ProductOrderResponse(result).response()

    @staticmethod
    @product_order_page.delete('/api/v2/orders/{order_id}/products/{product_id}')
    @JwtHandler.check_auth_roles()
    async def delete_product_order(order_id: int, product_id: int, user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await ProductOrderHandler().get_service().delete(product_id, order_id)
        return ProductOrderResponse(result).response()

    @staticmethod
    @product_order_page.patch('/api/v2/orders/{order_id}/products/{product_id}')
    @JwtHandler.check_auth_roles()
    async def update_product_order(order_id: int, product_id: int, data=Body(), user=Depends(JwtHandler.get_current_user)) -> Response:
        req = ProductOrderRequest(data)
        req.order_id = order_id
        req.product_id = product_id
        result = await ProductOrderHandler().get_service().update(req.get_product_order())
        return ProductOrderResponse(result).response()

    @staticmethod
    @product_order_page.get('/api/v2/orders/{order_id}/products')
    @JwtHandler.check_auth_roles()
    async def get_products_order_by_id(order_id: int, user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await ProductOrderHandler().get_service().get_products_order_by_id(order_id)
        return ProductsOrderResponse(result).response()

    def get_service(self) -> ProductOrderService:
        return self.service
