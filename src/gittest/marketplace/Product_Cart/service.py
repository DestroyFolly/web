from __future__ import annotations

from typing import Any

from marketplace.BD.ORM import CartDB
from marketplace.BD.session import SessionMaker
from marketplace.Cart.repository import CartRepository
from marketplace.Cart.service import CartService
from marketplace.Errors.dto_error import Error
from marketplace.Product_Cart.model import ProductCart
from marketplace.Product_Cart.repository import ProductCartRepository


class ProductCartService:
    def __init__(self, repo: ProductCartRepository, logger: Any) -> None:
        self.repo = repo
        self.logger = logger

    async def create(self, new_product_cart: ProductCart) -> ProductCart | Error:
        product_cart = await self.repo.create(new_product_cart)
        self.logger.info("An attempt to create has occurred!")
        if product_cart is None:
            self.logger.error("Failed to create!")
            return Error("He удалось создать связь товар-корзина!")
        self.logger.info("Successful create!")
        return product_cart

    async def delete(self, product_id: int, cart_id: int) -> ProductCart | Error:
        delete_product_cart = await self.repo.delete(product_id, cart_id)
        self.logger.info("An attempt to delete has occurred!")
        if delete_product_cart is not None:
            await CartService(CartRepository(CartDB, SessionMaker("pyproject.toml")), self.logger).update_carts_data()
            self.logger.info("Successful delete!")
            return delete_product_cart
        self.logger.error("Failed to delete!")
        return Error("He удалось удалить связь товар-корзина!")

    async def update(self, new_data: ProductCart) -> ProductCart | Error:
        product_cart = await self.repo.update(new_data)
        self.logger.info("An attempt to update has occurred!")
        if product_cart is not None:
            await CartService(CartRepository(CartDB, SessionMaker("pyproject.toml")), self.logger).update_carts_data()
            self.logger.info("Successful update!")
            return product_cart
        self.logger.error("Failed update!")
        return Error("He удалось обновить данные!")

    async def get_products_cart_by_id(self, cart_id: int) -> list[ProductCart] | Error:
        product_cart = await self.repo.get_products_cart_by_id(cart_id)
        self.logger.info("An attempt to get products cart by id has occurred!")
        if not product_cart:
            self.logger.error("Failed get products cart by id!")
            return Error("He удалось найти товары из корзины по id корзины!")
        self.logger.info("Successful get products cart by id!")
        return product_cart
