from __future__ import annotations

from sqlalchemy import select

from marketplace.BD.ORM import ProductCartDB
from marketplace.BD.session import SessionMaker
from marketplace.Product_Cart.model import ProductCart


class ProductCartRepository:
    def __init__(self, table: type[ProductCartDB], session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker.get_session()

    async def create(self, new_product_cart: ProductCart) -> ProductCart | None:
        async with self.session as session:
            already_exists = await session.execute(select(self.table).filter_by(product_id=new_product_cart.product_id,
                                                                                cart_id=new_product_cart.cart_id))
            already_exists = already_exists.scalars().first()
            if already_exists is None:
                session.add(self.table(new_product_cart))
                await session.commit()
                return new_product_cart
            return None

    async def delete(self, product_id: int, cart_id: int) -> ProductCart | None:
        async with self.session as session:
            product_cart_exists = await session.execute(select(self.table).filter_by(product_id=int(product_id),
                                                                                     cart_id=int(cart_id)))
            product_cart_exists = product_cart_exists.scalars().first()
            if product_cart_exists is not None:
                await session.delete(product_cart_exists)
                await session.commit()
            return product_cart_exists

    async def update(self, new_data: ProductCart) -> ProductCart | None:
        async with self.session as session:
            old_data = await session.execute(select(self.table).filter_by(product_id=new_data.product_id,
                                                                          cart_id=new_data.cart_id))
            old_data = old_data.scalars().first()
            if old_data:
                old_data.update(new_data)
                await session.commit()
            old_data = await session.execute(select(self.table).filter_by(product_id=new_data.product_id,
                                                                          cart_id=new_data.cart_id))
            return old_data.scalars().first()

    async def get_products_cart_by_id(self, cart_id: int) -> list[ProductCart] | None:
        async with self.session as session:
            result = await session.execute(select(self.table).filter_by(cart_id=int(cart_id)))
            return result.scalars().all()
