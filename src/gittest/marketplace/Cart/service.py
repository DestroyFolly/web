from __future__ import annotations

from typing import Any

from marketplace.Cart.model import Cart
from marketplace.Cart.repository import CartRepository
from marketplace.Errors.dto_error import Error


class CartService:
    def __init__(self, repo: CartRepository, logger: Any) -> None:
        self.repo = repo
        self.logger = logger

    async def create(self, new_cart: Cart) -> Cart | Error:
        cart = await self.repo.create(new_cart)
        self.logger.info("An attempt to create has occurred!")
        if cart is None:
            self.logger.error("Failed to create!")
            return Error("He удалось создать корзину!")
        self.logger.info("Successful create!")
        return cart

    async def update(self, new_data: Cart) -> Cart | Error:
        cart = await self.repo.update(new_data)
        self.logger.info("An attempt to update has occurred!")
        if cart is None:
            self.logger.error("Failed update!")
            return Error("He удалось обновить данные!")
        self.logger.info("Successful update!")
        return cart

    async def get_cart_by_id(self, cart_id: int) -> Cart | Error:
        cart = await self.repo.get_cart_by_id(cart_id)
        self.logger.info("An attempt to get cart by id has occurred!")
        if cart is None:
            self.logger.error("Failed get cart by id!")
            return Error("He удалось найти корзину по id!")
        self.logger.info("Successful get cart by id!")
        return cart

    async def get_all_carts(self) -> list[Cart] | Error:
        carts = await self.repo.get_all_carts()
        self.logger.info("An attempt to get all carts has occurred!")
        if not carts:
            self.logger.error("Failed get all carts!")
            return Error("He удалось найти корзины!")
        self.logger.info("Successful get all carts!")
        return carts

    async def update_carts_data(self) -> None:
        self.logger.info("An attempt to update carts data has occurred!")
        await self.repo.update_carts_data()
        self.logger.info("Successful update carts data!")
