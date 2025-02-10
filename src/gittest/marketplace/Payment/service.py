from __future__ import annotations

from typing import Any

from marketplace.Errors.dto_error import Error
from marketplace.Payment.model import Payment
from marketplace.Payment.repository import PaymentRepository


class PaymentService:
    def __init__(self, repo: PaymentRepository, logger: Any) -> None:
        self.repo = repo
        self.logger = logger

    async def create(self, user_id: int) -> Payment | Error:
        payment = await self.repo.create(user_id)
        self.logger.info("An attempt to create has occurred!")
        if payment is None:
            self.logger.error("Failed to create!")
            return Error("He удалось создать оплату!")
        self.logger.info("Successful create!")
        return payment

    async def delete(self, payment_id: int) -> Payment | Error:
        delete_payment = await self.repo.delete(payment_id)
        self.logger.info("An attempt to delete has occurred!")
        if delete_payment is None:
            self.logger.error("Failed to delete!")
            return Error("He удалось удалить оплату!")
        self.logger.info("Successful delete!")
        return delete_payment

    async def update(self, new_data: Payment) -> Payment | Error:
        payment = await self.repo.update(new_data)
        self.logger.info("An attempt to update has occurred!")
        if payment is None:
            self.logger.error("Failed update!")
            return Error("He удалось обновить данные!")
        self.logger.info("Successful update!")
        return payment

    async def get_payment_by_user_id(self, user_id: int) -> list[Payment] | Error:
        payment = await self.repo.get_payment_by_user_id(user_id)
        self.logger.info("An attempt to get payment by id has occurred!")
        if not payment:
            self.logger.error("Failed get payment by id!")
            return Error("He удалось найти оплаты по id!")
        self.logger.info("Successful get payment by id!")
        return payment

    async def get_all_payments(self) -> list[Payment] | Error:
        payments = await self.repo.get_all_payments()
        self.logger.info("An attempt to get all payments has occurred!")
        if not payments:
            self.logger.error("Failed get all payments!")
            return Error("He удалось найти оплаты!")
        self.logger.info("Successful get all payments!")
        return payments
