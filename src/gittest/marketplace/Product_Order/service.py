from __future__ import annotations

from typing import Any

from marketplace.BD.ORM import OrderDB
from marketplace.BD.session import SessionMaker
from marketplace.Errors.dto_error import Error
from marketplace.Order.repository import OrderRepository
from marketplace.Order.service import OrderService
from marketplace.Product_Order.model import ProductOrder
from marketplace.Product_Order.repository import ProductOrderRepository


class ProductOrderService:
    def __init__(self, repo: ProductOrderRepository, logger: Any) -> None:
        self.repo = repo
        self.logger = logger

    async def create(self, new_product_order: ProductOrder) -> ProductOrder | Error:
        product_order = await self.repo.create(new_product_order)
        self.logger.info("An attempt to create has occurred!")
        if product_order is None:
            self.logger.error("Failed to create!")
            return Error("He удалось создать связь товар-заказ!")
        self.logger.info("Successful create!")
        return product_order

    async def delete(self, product_id: int, order_id: int) -> ProductOrder | Error:
        delete_product_order = await self.repo.delete(product_id, order_id)
        self.logger.info("An attempt to delete has occurred!")
        if delete_product_order is not None:
            await OrderService(OrderRepository(OrderDB, SessionMaker("pyproject.toml")), self.logger).update_orders_data()
            self.logger.info("Successful delete!")
            return delete_product_order
        self.logger.error("Failed to delete!")
        return Error("He удалось удалить связь товар-корзина!")

    async def update(self, new_data: ProductOrder) -> ProductOrder | Error:
        product_order = await self.repo.update(new_data)
        self.logger.info("An attempt to update has occurred!")
        if product_order is not None:
            await OrderService(OrderRepository(OrderDB, SessionMaker("pyproject.toml")), self.logger).update_orders_data()
            self.logger.info("Successful update!")
            return product_order
        self.logger.error("Failed update!")
        return Error("He удалось обновить данные!")

    async def get_products_order_by_id(self, order_id: int) -> list[ProductOrder] | Error:
        product_order = await self.repo.get_products_order_by_id(order_id)
        self.logger.info("An attempt to get products order by id has occurred!")
        if not product_order:
            self.logger.error("Failed get products order by id!")
            return Error("He удалось найти товары из заказа по id заказа!")
        self.logger.info("Successful get products order by id!")
        return product_order
