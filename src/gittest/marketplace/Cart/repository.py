from __future__ import annotations

from sqlalchemy import func
from sqlalchemy import select

from marketplace.BD.ORM import CartDB
from marketplace.BD.ORM import ProductCartDB
from marketplace.BD.ORM import ProductDB
from marketplace.BD.session import SessionMaker
from marketplace.Cart.model import Cart


class CartRepository:
    def __init__(self, table: type[CartDB], session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker.get_session()

    async def create(self, new_cart: Cart) -> Cart | None:
        async with self.session as session:
            session.add(self.table(new_cart))
            await session.commit()
            return new_cart

    async def update(self, new_data: Cart) -> Cart | None:
        async with self.session as session:
            old_data = await session.execute(select(self.table).filter_by(cart_id=new_data.cart_id))
            old_data = old_data.scalars().first()
            if old_data:
                old_data.update(new_data)
                await session.commit()
            old_data = await session.execute(select(self.table).filter_by(cart_id=new_data.cart_id))
            return old_data.scalars().first()

    async def get_cart_by_id(self, cart_id: int) -> Cart | None:
        async with self.session as session:
            result = await session.execute(select(self.table).filter_by(cart_id=int(cart_id)))
            return result.scalars().first()

    async def update_carts_data(self) -> None:
        async with self.session as session:
            cart_prices = await session.execute(select(self.table.cart_id,
                func.sum(ProductDB.price * ProductCartDB.quantity)).
                join(ProductCartDB, self.table.cart_id == ProductCartDB.cart_id).
                join(ProductDB, ProductDB.product_id == ProductCartDB.product_id).group_by(self.table.cart_id))
            cart_prices = cart_prices.all()
            for cart_id, all_price in cart_prices:
                data_cart = await session.execute(select(self.table).filter_by(cart_id=int(cart_id)))
                data_cart = data_cart.scalars().first()
                data_cart.update(Cart(all_price=all_price))
            await session.commit()

    async def get_all_carts(self) -> list[Cart]:
        async with self.session as session:
            result = await session.execute(select(self.table))
            return result.scalars().all()
