from __future__ import annotations

from sqlalchemy import select

from marketplace.BD.ORM import ProductOrderDB
from marketplace.BD.session import SessionMaker
from marketplace.Product_Order.model import ProductOrder


class ProductOrderRepository:
    def __init__(self, table: type[ProductOrderDB], session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker.get_session()

    async def create(self, new_product_order: ProductOrder) -> ProductOrder | None:
        async with self.session as session:
            already_exists = await session.execute(select(self.table).filter_by(product_id=new_product_order.product_id,
                                                                                order_id=new_product_order.order_id))
            already_exists = already_exists.scalars().first()
            if already_exists is None:
                session.add(self.table(new_product_order))
                await session.commit()
                return new_product_order
            return None

    async def delete(self, product_id: int, order_id: int) -> ProductOrder | None:
        async with self.session as session:
            product_order_exists = await session.execute(select(self.table).filter_by(product_id=int(product_id),
                                                                                      order_id=int(order_id)))
            product_order_exists = product_order_exists.scalars().first()
            if product_order_exists is not None:
                await session.delete(product_order_exists)
                await session.commit()
            return product_order_exists

    async def update(self, new_data: ProductOrder) -> ProductOrder | None:
        async with self.session as session:
            old_data = await session.execute(select(self.table).filter_by(product_id=new_data.product_id,
                                                                          order_id=new_data.order_id))
            old_data = old_data.scalars().first()
            if old_data:
                old_data.update(new_data)
                await session.commit()
            old_data = await session.execute(select(self.table).filter_by(product_id=new_data.product_id,
                                                                          order_id=new_data.order_id))
            return old_data.scalars().first()

    async def get_products_order_by_id(self, order_id: int) -> list[ProductOrder] | None:
        async with self.session as session:
            result = await session.execute(select(self.table).filter_by(order_id=int(order_id)))
            return result.scalars().all()
