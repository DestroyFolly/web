from __future__ import annotations

from contextlib import asynccontextmanager

from dynaconf import Dynaconf
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


class SessionMaker:
    def __init__(self, config_name: str, port=5000, test_flag=None) -> None:
        self.settings = Dynaconf(settings_files=[config_name])
        self.port = port
        self.engine = create_async_engine(SessionMaker.get_url(self.settings, self.port, test_flag), echo=False, pool_pre_ping=True,
                                          pool_timeout=self.settings.database.pool_timeout)

    @staticmethod
    def async_session_generator(engine: create_async_engine) -> sessionmaker:
        return sessionmaker(engine, class_=AsyncSession)

    @staticmethod
    def get_url(settings: Dynaconf, port, test_flag=None) -> str:
        print(port)
        if port == 5000:
            return f"{settings.database.sybd_name}+asyncpg://{settings.database.username}:" \
                   f"{settings.database.password}@{settings.database.host}:" \
                   f"{settings.database.port}/{settings.database.test_name if test_flag else settings.database.name}"
        elif port == 8099:
            print(4848454465)
            print(f"{settings.database.sybd_name}+asyncpg://{settings.database.username2}:" \
                   f"{settings.database.password2}@{settings.database.host}:" \
                   f"{settings.database.port2}/{settings.database.test_name if test_flag else settings.database.name2}")
            return f"{settings.database.sybd_name}+asyncpg://{settings.database.username2}:" \
                   f"{settings.database.password2}@{settings.database.host}:" \
                   f"{settings.database.port2}/{settings.database.test_name if test_flag else settings.database.name2}"
        else:
            return f"{settings.database.sybd_name}+asyncpg://{settings.database.username1}:" \
                   f"{settings.database.password1}@{settings.database.host}:" \
                   f"{settings.database.port}/{settings.database.test_name if test_flag else settings.database.name}"

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        try:
            async_session = self.async_session_generator(self.engine)
            async with async_session() as session:
                yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
