from __future__ import annotations

from flask import Blueprint
from flask import Response
from flask import make_response
from flask import request
from flask import url_for

from marketplace.BD.ORM import PaymentDB
from marketplace.BD.session import SessionMaker
from marketplace.Logger.loger import logger
from marketplace.Payment.dto import CODE_SUCCESS
from marketplace.Payment.dto import PaymentRequest
from marketplace.Payment.dto import PaymentResponse
from marketplace.Payment.dto import PaymentsResponse
from marketplace.Payment.repository import PaymentRepository
from marketplace.Payment.service import PaymentService
from marketplace.View.View import View


payment_page = Blueprint("payment_page", __name__)


class PaymentHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = PaymentDB
        self.repo = PaymentRepository(self.table, self.session_maker)
        self.service = PaymentService(self.repo, self.logger)

    @staticmethod
    @payment_page.route('/create_payment/<payment_id>', methods=['GET'])
    async def create_payment(payment_id: int) -> Response:
        result = await PaymentHandler().get_service().create(payment_id)
        res = PaymentResponse(result)
        if res.check_is_error():
            return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.redirect(url_for('payment_page.create_payment')), res.error)

    @staticmethod
    @payment_page.route('/delete_payment', methods=['GET', 'POST'])
    async def delete_payment() -> Response:
        if request.method == "POST":
            req = PaymentRequest(request.form)
            result = await PaymentHandler().get_service().delete(req.payment_id)
            res = PaymentResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template('payment_delete.html'), CODE_SUCCESS)

    @staticmethod
    @payment_page.route('/update_payment', methods=['GET', 'POST'])
    async def update_payment() -> Response:
        if request.method == "POST":
            req = PaymentRequest(request.form)
            result = await PaymentHandler().get_service().update(req.get_payment())
            res = PaymentResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template('payment_update.html'), CODE_SUCCESS)

    @staticmethod
    @payment_page.route('/get_payment_by_user_id/<user_id>', methods=['GET'])
    async def get_payment_by_user_id(user_id: int) -> Response:
        result = await PaymentHandler().get_service().get_payment_by_user_id(user_id)
        res = PaymentsResponse(result)
        return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)

    @staticmethod
    @payment_page.route('/get_payment_by_user_id', methods=['GET', 'POST'])
    async def get_payment_by_user_id_admin() -> Response:
        if request.method == "POST":
            req = PaymentRequest(request.form)
            return View.redirect(url_for("payment_page.get_payment_by_user_id", user_id=req.user_id))
        return make_response(View.render_template("get_payment_by_user_id.html"), CODE_SUCCESS)

    @staticmethod
    @payment_page.route('/get_all_payments', methods=['GET'])
    async def get_all_payments() -> list[Response] | Response:
        result = await PaymentHandler().get_service().get_all_payments()
        res = PaymentsResponse(result)
        return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)

    def get_service(self) -> PaymentService:
        return self.service
