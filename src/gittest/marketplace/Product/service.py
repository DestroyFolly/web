from __future__ import annotations

from typing import Any

from marketplace.BD.ORM import CartDB
from marketplace.BD.ORM import OrderDB
from marketplace.BD.session import SessionMaker
from marketplace.Cart.repository import CartRepository
from marketplace.Cart.service import CartService
from marketplace.Errors.dto_error import Error
from marketplace.Order.repository import OrderRepository
from marketplace.Order.service import OrderService
from marketplace.Product.model import Product
from marketplace.Product.repository import ProductRepository


class ProductService:
    def __init__(self, repo: ProductRepository, logger: Any) -> None:
        self.repo = repo
        self.logger = logger

    async def create(self, new_product: Product, seller_id: int) -> Product | Error:
        new_product.seller_id = seller_id
        product = await self.repo.create(new_product)
        self.logger.info("An attempt to create has occurred!")
        if product is None:
            self.logger.error("Failed to create!")
            return Error("He удалось создать товар!")
        self.logger.info("Successful create!")
        return product

    async def delete(self, product_id: int) -> Product | Error:
        delete_product = await self.repo.delete(product_id)
        self.logger.info("An attempt to delete has occurred!")
        if delete_product is not None:
            await OrderService(OrderRepository(OrderDB, SessionMaker("pyproject.toml")), self.logger).update_orders_data()
            await CartService(CartRepository(CartDB, SessionMaker("pyproject.toml")), self.logger).update_carts_data()
            self.logger.info("Successful delete!")
            return delete_product
        self.logger.error("Failed to delete!")
        return Error("He удалось удалить товар!")

    async def update(self, new_data: Product) -> Product | Error:
        user = await self.repo.update(new_data)
        self.logger.info("An attempt to update has occurred!")
        if user is not None:
            await OrderService(OrderRepository(OrderDB, SessionMaker("pyproject.toml")), self.logger).update_orders_data()
            await CartService(CartRepository(CartDB, SessionMaker("pyproject.toml")), self.logger).update_carts_data()
            self.logger.info("Successful update!")
            return user
        self.logger.error("Failed update!")
        return Error("He удалось обновить данные!")

    async def get_product_by_id(self, product_id: int) -> Product | Error:
        product = await self.repo.get_product_by_id(product_id)
        self.logger.info("An attempt to get product by id has occurred!")
        if product is None:
            self.logger.error("Failed get product by id!")
            return Error("He удалось найти товар по id!")
        self.logger.info("Successful get product by id!")
        return product

    async def get_product_by_title(self, title: str) -> Product | Error:
        product = await self.repo.get_product_by_title(title)
        self.logger.info("An attempt to get product by title has occurred!")
        if product is None:
            self.logger.error("Failed get product by title!")
            return Error("He удалось найти товар по названию!")
        self.logger.info("Successful get product by title!")
        return product

    async def get_all_products(self) -> list[Product] | Error:
        products = await self.repo.get_all_products()
        self.logger.info("An attempt to get all products has occurred!")
        if not products:
            self.logger.error("Failed get all products!")
            return Error("He удалось найти товары!")
        self.logger.info("Successful get all products!")
        return products

    async def get_seller_products(self, seller_id: int) -> list[Product] | Error:
        products = await self.repo.get_seller_products(seller_id)
        self.logger.info("An attempt to get all seller's products has occurred!")
        if not products:
            self.logger.error("Failed get all seller's products!")
            return Error("He удалось найти товары!")
        self.logger.info("Successful get all seller's products!")
        return products
