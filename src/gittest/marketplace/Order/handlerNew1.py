from __future__ import annotations
from fastapi import APIRouter, Body, Response, Depends

from marketplace.BD.ORM import OrderDB
from marketplace.BD.session import SessionMaker
from marketplace.Logger.loger import logger
from marketplace.Order.dto import OrderRequest
from marketplace.Order.dto import OrderResponse
from marketplace.Order.dto import OrdersResponse
from marketplace.Order.repository import OrderRepository
from marketplace.Order.service import OrderService
from marketplace.Connections.my_jwt1 import JwtHandler


order_page = APIRouter()


class OrderHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml", port=5001)
        self.table = OrderDB
        self.repo = OrderRepository(self.table, self.session_maker)
        self.service = OrderService(self.repo, self.logger)

    @staticmethod
    @order_page.patch('/api/v2/orders/{order_id}')
    @JwtHandler.check_auth_roles()
    async def update_order(order_id: int, data=Body(), user=Depends(JwtHandler.get_current_user)) -> Response:
        req = OrderRequest(data)
        req.order_id = order_id
        result = await OrderHandler().get_service().update(req.get_order())
        return OrderResponse(result).response()

    @staticmethod
    @order_page.get('/api/v2/orders/{order_id}')
    @JwtHandler.check_auth_roles()
    async def get_order_by_id(order_id: int, user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await OrderHandler().get_service().get_order_by_id(order_id)
        return OrderResponse(result).response()

    @staticmethod
    @order_page.get('/api/v2/orders')
    @JwtHandler.check_auth_roles(roles=["admin"])
    async def get_all_orders(user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await OrderHandler().get_service().get_all_orders()
        return OrdersResponse(result).response()

    def get_service(self) -> OrderService:
        return self.service
