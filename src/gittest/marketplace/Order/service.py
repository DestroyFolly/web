from __future__ import annotations

from typing import Any

from marketplace.Errors.dto_error import Error
from marketplace.Order.model import Order
from marketplace.Order.repository import OrderRepository


class OrderService:
    def __init__(self, repo: OrderRepository, logger: Any) -> None:
        self.repo = repo
        self.logger = logger

    async def create(self, new_order: Order) -> Order | Error:
        order = await self.repo.create(new_order)
        self.logger.info("An attempt to create has occurred!")
        if order is None:
            self.logger.error("Failed to create!")
            return Error("He удалось создать заказ!")
        self.logger.info("Successful create!")
        return order

    async def delete(self, order_id: int) -> Order | Error:
        delete_order = await self.repo.delete(order_id)
        self.logger.info("An attempt to delete has occurred!")
        if delete_order is None:
            self.logger.error("Failed to delete!")
            return Error("He удалось удалить заказ!")
        self.logger.info("Successful delete!")
        return delete_order

    async def update(self, new_data: Order) -> Order | Error:
        order = await self.repo.update(new_data)
        self.logger.info("An attempt to update has occurred!")
        if order is None:
            self.logger.error("Failed update!")
            return Error("He удалось обновить данные!")
        self.logger.info("Successful update!")
        return order

    async def get_order_by_id(self, order_id: int) -> Order | Error:
        order = await self.repo.get_order_by_id(order_id)
        self.logger.info("An attempt to get order by id has occurred!")
        if order is None:
            self.logger.error("Failed get order by id!")
            return Error("He удалось найти заказ по id!")
        self.logger.info("Successful get order by id!")
        return order

    async def get_all_orders(self) -> list[Order] | Error:
        orders = await self.repo.get_all_orders()
        self.logger.info("An attempt to get all orders has occurred!")
        if not orders:
            self.logger.error("Failed get all orders!")
            return Error("He удалось найти заказы!")
        self.logger.info("Successful get all orders!")
        return orders

    async def update_orders_data(self) -> None:
        self.logger.info("An attempt to update orders data has occurred!")
        await self.repo.update_orders_data()
        self.logger.info("Successful update orders data!")
