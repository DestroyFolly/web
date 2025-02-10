from __future__ import annotations
import sqlalchemy.exc
from sqlalchemy import select

from marketplace.BD.ORM import UserDB
from marketplace.BD.session import SessionMaker
from marketplace.User.model import User
from marketplace.Errors.dto_error import Error

class UserRepository:
    def __init__(self, table: type[UserDB], session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker.get_session()

    async def create(self, new_user: User) -> User | None:
        async with self.session as session:
            try:
                already_exists = await session.execute(select(self.table).filter_by(email=new_user.email))
                already_exists = already_exists.scalars().first()
                if already_exists is None:
                    all_users = await session.execute(select(self.table))
                    new_user.user_id = max([0] + [user.user_id for user in all_users.scalars().all()]) + 1
                    session.add(self.table(new_user))
                    await session.commit()
                    return new_user
                return None
            except sqlalchemy.exc.ProgrammingError as e:
                return Error("Нет доступа к таблице!", 403)

    async def delete(self, user_id: int) -> User | None:
        async with self.session as session:
            user_exists = await session.execute(select(self.table).filter_by(user_id=int(user_id)))
            user_exists = user_exists.scalars().first()
            if user_exists is not None:
                await session.delete(user_exists)
                await session.commit()
            return user_exists

    async def update(self, new_data: User) -> User | None:
        async with self.session as session:
            old_data = await session.execute(select(self.table).filter_by(user_id=new_data.user_id))
            old_data = old_data.scalars().first()
            if old_data:
                old_data.update(new_data)
                await session.commit()
            old_data = await session.execute(select(self.table).filter_by(user_id=new_data.user_id))
            return old_data.scalars().first()

    async def get_user_by_id(self, user_id: int) -> User | None:
        async with self.session as session:
            result = await session.execute(select(self.table).filter_by(user_id=int(user_id)))
            return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        async with self.session as session:
            result = await session.execute(select(self.table).filter_by(email=email))
            return result.scalars().first()

    async def get_all_users(self) -> list[User]:
        async with self.session as session:
            result = await session.execute(select(self.table))
            return result.scalars().all()

    async def get_user_role(self, user_id) -> User | None:
        async with self.session as session:
            result = await session.execute(select(self.table).filter_by(user_id=int(user_id)))
            return result.scalars().first()
