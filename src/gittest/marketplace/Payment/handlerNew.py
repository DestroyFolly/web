from __future__ import annotations


from fastapi import APIRouter, Body, Response, Depends, Query
from marketplace.BD.ORM import PaymentDB
from marketplace.BD.session import SessionMaker
from marketplace.Logger.loger import logger
from marketplace.Payment.dto import PaymentRequest
from marketplace.Payment.dto import PaymentResponse
from marketplace.Payment.dto import PaymentsResponse
from marketplace.Payment.repository import PaymentRepository
from marketplace.Payment.service import PaymentService
from marketplace.Connections.my_jwt import JwtHandler

payment_page = APIRouter()


class PaymentHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = PaymentDB
        self.repo = PaymentRepository(self.table, self.session_maker)
        self.service = PaymentService(self.repo, self.logger)

    @staticmethod
    @payment_page.post('/api/v2/payments/users')
    @JwtHandler.check_auth_roles()
    async def create_payment(user_id: int = Query(...), user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await PaymentHandler().get_service().create(user_id)
        return PaymentResponse(result).response()

    @staticmethod
    @payment_page.delete('/api/v2/payments/{payment_id}')
    @JwtHandler.check_auth_roles()
    async def delete_payment(payment_id: int, user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await PaymentHandler().get_service().delete(payment_id)
        return PaymentResponse(result).response()

    @staticmethod
    @payment_page.patch('/api/v2/payments/{payment_id}')
    @JwtHandler.check_auth_roles()
    async def update_payment(payment_id: int, data=Body(), user=Depends(JwtHandler.get_current_user)) -> Response:
        req = PaymentRequest(data)
        req.payment_id = payment_id
        result = await PaymentHandler().get_service().update(req.get_payment())
        return PaymentResponse(result).response()

    # @staticmethod
    # @payment_page.get('/api/v2/payments/users')
    # @JwtHandler.check_auth_roles()
    # async def get_payment_by_user_id(user_id: int = Query(...), user=Depends(JwtHandler.get_current_user)) -> Response:
    #     result = await PaymentHandler().get_service().get_payment_by_user_id(user_id)
    #     return PaymentsResponse(result).response()

    @staticmethod
    @payment_page.get('/api/v2/payments')
    @JwtHandler.check_auth_roles(roles=["admin"])
    async def get_all_payments(user_id: int = Query(None), user=Depends(JwtHandler.get_current_user)) -> Response:
        if user_id:
            result = await PaymentHandler().get_service().get_payment_by_user_id(user_id)
        else:
            result = await PaymentHandler().get_service().get_all_payments()
        return PaymentsResponse(result).response()

    def get_service(self) -> PaymentService:
        return self.service
