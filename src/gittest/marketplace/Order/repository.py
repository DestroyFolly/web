from __future__ import annotations

from sqlalchemy import func
from sqlalchemy import select

from marketplace.BD.ORM import OrderDB
from marketplace.BD.ORM import ProductDB
from marketplace.BD.ORM import ProductOrderDB
from marketplace.BD.session import SessionMaker
from marketplace.Order.model import Order


class OrderRepository:
    def __init__(self, table: type[OrderDB], session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker.get_session()

    async def create(self, new_order: Order) -> Order | None:
        async with self.session as session:
            session.add(self.table(new_order))
            await session.commit()
            return new_order

    async def delete(self, order_id: int) -> Order | None:
        async with self.session as session:
            order_exists = await session.execute(select(self.table).filter_by(order_id=int(order_id)))
            order_exists = order_exists.scalars().first()
            if order_exists is not None:
                session.delete(order_exists)
                await session.commit()
            return order_exists

    async def update(self, new_data: Order) -> Order | None:
        async with self.session as session:
            old_data = await session.execute(select(self.table).filter_by(order_id=new_data.order_id))
            old_data = old_data.scalars().first()
            if old_data:
                old_data.update(new_data)
                await session.commit()
            old_data = await session.execute(select(self.table).filter_by(order_id=new_data.order_id))
            return old_data.scalars().first()

    async def get_order_by_id(self, order_id: int) -> Order | None:
        async with self.session as session:
            result = await session.execute(select(self.table).filter_by(order_id=int(order_id)))
            return result.scalars().first()

    async def update_orders_data(self) -> None:
        async with self.session as session:
            orders_prices = await session.execute(select(self.table.order_id,
                func.sum(ProductDB.price * ProductOrderDB.quantity)).
                join(ProductOrderDB, self.table.order_id == ProductOrderDB.order_id).
                join(ProductDB, ProductDB.product_id == ProductOrderDB.product_id).group_by(self.table.order_id))
            orders_prices = orders_prices.all()
            for order_id, all_price in orders_prices:
                data_order = await session.execute(select(self.table).filter_by(order_id=int(order_id)))
                data_order = data_order.scalars().first()
                data_order.update(Order(all_price=all_price))
            await session.commit()

    async def get_all_orders(self) -> list[Order]:
        async with self.session as session:
            result = await session.execute(select(self.table))
            return result.scalars().all()
