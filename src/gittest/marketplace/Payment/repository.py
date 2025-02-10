from __future__ import annotations

from sqlalchemy import select

from marketplace.BD.ORM import OrderDB
from marketplace.BD.ORM import PaymentDB
from marketplace.BD.ORM import UserDB
from marketplace.BD.session import SessionMaker
from marketplace.Order.model import Order
from marketplace.Payment.model import Payment
from marketplace.User.model import User


class PaymentRepository:
    def __init__(self, table: type[PaymentDB], session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker.get_session()

    async def create(self, user_id: int) -> Payment | None:
        async with self.session as session:
            user = await session.execute(select(UserDB).filter_by(user_id=int(user_id)))
            user = user.scalars().first()
            if user:
                order = await session.execute(select(OrderDB).filter_by(user_id=int(user_id)))
                order = order.scalars().first()
                all_payments = await session.execute(select(self.table))
                payment_id_my = max([0] + [payment.payment_id for payment in all_payments.scalars().all()]) + 1
                new_payment = Payment(
                    payment_id=payment_id_my,
                    all_price=order.all_price, state="not_passed", user_id=user.user_id)
                if user.money - order.all_price >= 0:
                    new_payment.state = "passed"
                    user.update(User(money=user.money - order.all_price))
                    session.delete(order.order_id)
                    session.add(OrderDB(Order(order_id=user.user_id, all_price=0,
                                              address=user.address, user_id=user.user_id)))
                session.add(self.table(new_payment))
                if order.all_price > 0:
                    await session.commit()
            payment = await session.execute(select(PaymentDB).filter_by(payment_id=payment_id_my))
            return payment.scalars().first()

    async def delete(self, payment_id: int) -> Payment | None:
        async with self.session as session:
            payment_exists = await session.execute(select(self.table).filter_by(payment_id=int(payment_id)))
            payment_exists = payment_exists.scalars().first()
            if payment_exists is not None:
                await session.delete(payment_exists)
                await session.commit()
            return payment_exists

    async def update(self, new_data: Payment) -> Payment | None:
        async with self.session as session:
            old_data = await session.execute(select(self.table).filter_by(payment_id=new_data.payment_id))
            old_data = old_data.scalars().first()
            if old_data:
                old_data.update(new_data)
                await session.commit()
            old_data = await session.execute(select(self.table).filter_by(payment_id=new_data.payment_id))
            return old_data.scalars().first()

    async def get_payment_by_user_id(self, user_id: int) -> list[Payment] | None:
        async with self.session as session:
            result = await session.execute(select(self.table).filter_by(user_id=int(user_id)))
            return result.scalars().all()

    async def get_all_payments(self) -> list[Payment]:
        async with self.session as session:
            result = await session.execute(select(self.table))
            return result.scalars().all()
