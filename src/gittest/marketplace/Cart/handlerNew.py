from __future__ import annotations

from fastapi import APIRouter, Body, Response, Depends

from marketplace.BD.ORM import CartDB
from marketplace.BD.session import SessionMaker
from marketplace.Cart.dto import CartResponse
from marketplace.Cart.dto import CartsResponse
from marketplace.Cart.repository import CartRepository
from marketplace.Cart.service import CartService
from marketplace.Logger.loger import logger
from marketplace.Connections.my_jwt import JwtHandler

cart_page = APIRouter()


class CartHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = CartDB
        self.repo = CartRepository(self.table, self.session_maker)
        self.service = CartService(self.repo, self.logger)

    @staticmethod
    @cart_page.get('/api/v2/carts/{cart_id}')
    @JwtHandler.check_auth_roles()
    async def get_cart_by_id(cart_id: int, user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await CartHandler().get_service().get_cart_by_id(cart_id)
        return CartResponse(result).response()

    @staticmethod
    @cart_page.get('/api/v2/carts')
    @JwtHandler.check_auth_roles(roles=["admin"])
    async def get_all_carts(user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await CartHandler().get_service().get_all_carts()
        return CartsResponse(result).response()

    def get_service(self) -> CartService:
        return self.service
