from __future__ import annotations

from sqlalchemy import select

from marketplace.BD.ORM import ProductDB
from marketplace.BD.session import SessionMaker
from marketplace.Product.model import Product


class ProductRepository:
    def __init__(self, table: type[ProductDB], session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker.get_session()

    async def create(self, new_product: Product) -> Product | None:
        async with self.session as session:
            already_exists = await session.execute(select(self.table).filter_by(title=new_product.title))
            already_exists = already_exists.scalars().first()
            if already_exists is None:
                all_products = await session.execute(select(self.table))
                new_product.product_id = max([0] + [product.product_id for product in all_products.scalars().all()]) + 1
                session.add(self.table(new_product))
                await session.commit()
                return new_product
            return None

    async def delete(self, product_id: int) -> Product | None:
        async with self.session as session:
            product_exists = await session.execute(select(self.table).filter_by(product_id=int(product_id)))
            product_exists = product_exists.scalars().first()
            if product_exists is not None:
                await session.delete(product_exists)
                await session.commit()
            return product_exists

    async def update(self, new_data: Product) -> Product | None:
        async with self.session as session:
            old_data = await session.execute(select(self.table).filter_by(product_id=new_data.product_id))
            old_data = old_data.scalars().first()
            if old_data:
                old_data.update(new_data)
                await session.commit()
            old_data = await session.execute(select(self.table).filter_by(product_id=new_data.product_id))
            return old_data.scalars().first()

    async def get_product_by_id(self, product_id: int) -> Product | None:
        async with self.session as session:
            result = await session.execute(select(self.table).filter_by(product_id=int(product_id)))
            return result.scalars().first()

    async def get_product_by_title(self, title: str) -> Product | None:
        async with self.session as session:
            result = await session.execute(select(self.table).filter_by(title=title))
            return result.scalars().first()

    async def get_all_products(self) -> list[Product]:
        async with self.session as session:
            result = await session.execute(select(self.table))
            return result.scalars().all()

    async def get_seller_products(self, seller_id: int) -> list[Product]:
        async with self.session as session:
            result = await session.execute(select(self.table).filter_by(seller_id=int(seller_id)))
            return result.scalars().all()
