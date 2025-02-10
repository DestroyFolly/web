from __future__ import annotations

from hashlib import sha256
from typing import Any

from marketplace.BD.ORM import CartDB
from marketplace.BD.ORM import OrderDB
from marketplace.BD.session import SessionMaker
from marketplace.Cart.model import Cart
from marketplace.Cart.repository import CartRepository
from marketplace.Cart.service import CartService
from marketplace.Errors.dto_error import Error
from marketplace.Order.model import Order
from marketplace.Order.repository import OrderRepository
from marketplace.Order.service import OrderService
from marketplace.User.model import User
from marketplace.User.repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository, logger: Any) -> None:
        self.repo = repo
        self.logger = logger

    async def login(self, email: str, password: str) -> User | Error:
        user = await self.repo.get_user_by_email(email)
        self.logger.info("An attempt to login has occurred!")
        if user and user.password == UserService.my_hash(password):
            self.logger.info("Successful login!")
            return user
        self.logger.error("Failed to login!")
        return Error("He удалось залогиниться!")

    async def register(self, new_user: User) -> User | Error:
        if new_user.password:
            new_user.password = UserService.my_hash(new_user.password)
        user = await self.repo.create(new_user)
        self.logger.info("An attempt to register has occurred!")
        if isinstance(user, Error):
            return user
        service_cart = CartService(CartRepository(CartDB, SessionMaker("pyproject.toml")), self.logger)
        user_cart = await service_cart.create(Cart(cart_id=user.user_id, all_price=0, user_id=new_user.user_id))
        if user_cart is not None:
            service_order = OrderService(OrderRepository(OrderDB, SessionMaker("pyproject.toml")), self.logger)
            user_order = await service_order.create(Order(order_id=user.user_id, all_price=0,
                                                    address=user.address, user_id=user.user_id))
            if user_order is not None:
                self.logger.info("Successful register!")
                return user
            self.logger.error("Database content error!")
        self.logger.error("Database content error!")
        await self.repo.delete(user)
        self.logger.error("Failed to register!")
        return Error("He удалось зарегистрироваться!")

    async def delete(self, user_id: int) -> User | Error:
        delete_user = await self.repo.delete(user_id)
        self.logger.info("An attempt to delete has occurred!")
        if delete_user is None:
            self.logger.error("Failed to delete!")
            return Error("He удалось удалить пользователя!")
        self.logger.info("Successful delete!")
        return delete_user

    async def update(self, new_data: User) -> User | Error:
        if new_data.password:
            new_data.password = await UserService.my_hash(new_data.password)
        user = await self.repo.update(new_data)
        self.logger.info("An attempt to update has occurred!")
        if user is None:
            self.logger.error("Failed update!")
            return Error("He удалось обновить данные!")
        self.logger.info("Successful update!")
        return user

    async def get_user_by_id(self, user_id: int) -> User | Error:
        user = await self.repo.get_user_by_id(user_id)
        self.logger.info("An attempt to get user by id has occurred!")
        if user is None:
            self.logger.error("Failed get user by id!")
            return Error("He удалось найти данного пользователя по id!")
        self.logger.info("Successful get user by id!")
        return user

    async def get_user_by_email(self, email: str) -> User | Error:
        user = await self.repo.get_user_by_email(email)
        self.logger.info("An attempt to get user by email user has occurred!")
        if user is None:
            self.logger.error("Failed get user by email!")
            return Error("He удалось найти данного пользователя по email!")
        self.logger.info("Successful get user by email!")
        return user

    async def get_all_users(self) -> list[User] | Error:
        users = await self.repo.get_all_users()
        self.logger.info("An attempt to get all users has occurred!")
        if not users:
            self.logger.error("Failed get all users!")
            return Error("He удалось найти пользователей!")
        self.logger.info("Successful get all users!")
        return users

    async def get_user_role(self, user_id: int) -> str:
        user = await self.repo.get_user_role(user_id)
        return user.role if user else "guest"

    @staticmethod
    def my_hash(text: str) -> str:
        return sha256(text.encode()).hexdigest()
