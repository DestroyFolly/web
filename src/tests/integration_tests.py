from __future__ import annotations

import unittest
import allure

from marketplace.BD.ORM import OrderDB
from marketplace.BD.ORM import ProductDB
from marketplace.BD.ORM import UserDB
from marketplace.BD.ORM import PaymentDB
from marketplace.BD.ORM import CartDB
from marketplace.BD.ORM import ProductOrderDB
from marketplace.BD.ORM import ProductCartDB
from marketplace.BD.session import SessionMaker
from marketplace.Errors.dto_error import Error
from marketplace.Order.model import Order
from marketplace.Order.repository import OrderRepository
from marketplace.Order.service import OrderService
from marketplace.Product.model import Product
from marketplace.Product.repository import ProductRepository
from marketplace.Product.service import ProductService
from marketplace.User.model import User
from marketplace.User.repository import UserRepository
from marketplace.User.service import UserService
from marketplace.Payment.repository import PaymentRepository
from marketplace.Payment.service import PaymentService
from marketplace.Payment.model import Payment
from marketplace.Cart.repository import CartRepository
from marketplace.Cart.service import CartService
from marketplace.Cart.model import Cart
from marketplace.Product_Order.repository import ProductOrderRepository
from marketplace.Product_Order.service import ProductOrderService
from marketplace.Product_Order.model import ProductOrder
from marketplace.Product_Cart.repository import ProductCartRepository
from marketplace.Product_Cart.service import ProductCartService
from marketplace.Product_Cart.model import ProductCart

execution_failed = False


@allure.epic("Marketplace")
@allure.feature("TestUser")
class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.session_maker = SessionMaker("pyproject.toml", True)
        self.session = self.session_maker.get_session()
        self.table = UserDB
        self.repo = UserRepository(self.table, self.session_maker)
        self.service = UserService(self.repo, self.logger)
        self.user = User(user_id=None, fio="Kozhevnikov M.C.", email="matvey.1", password="1", money=10000,
                         phone="78923121975", role="admin")
        self.execution_failed = execution_failed

    async def tearDown(self):
        global execution_failed
        if self._outcome.errors:
            for test, err in self._outcome.errors:
                if test is self:
                    execution_failed = True

    def skip_if_failed(self):
        if self.execution_failed:
            self.skipTest("Previous test failed, skipping this test.")

    @allure.story("testRepository")
    async def testRepository(self) -> None:
        assert isinstance(self.user.email, str)

        already_exists = await self.repo.get_user_by_email(self.user.email)
        if isinstance(already_exists, self.table):
            await self.repo.delete(already_exists)
        else:
            assert already_exists == Error("He удалось найти данного пользователя по email!")

        user = await self.service.register(self.user)
        assert isinstance(user, User)

        self.user.user_id = user.user_id
        reg_user = await self.repo.get_user_by_id(self.user.user_id if self.user.user_id else 0)
        assert self.user == reg_user

        assert isinstance(self.user.email, str)
        assert isinstance(self.user.password, str)
        log_user_success = await self.service.login(self.user.email, self.user.password)
        log_user_failure = await self.service.login(self.user.email, "wrong password")
        assert self.user == log_user_success
        assert log_user_failure == Error("He удалось залогиниться!")

        self.user.password = "2"
        change_password_user = await self.repo.update(self.user)
        assert isinstance(change_password_user, UserDB)
        assert change_password_user.password == "2"

        assert isinstance(self.user.user_id, int)
        delete_user = await self.repo.delete(self.user.user_id)
        assert self.user == delete_user

    @allure.story("testService")
    async def testService(self) -> None:
        assert isinstance(self.user.email, str)

        already_exists = await self.service.get_user_by_email(self.user.email)
        if isinstance(already_exists, self.table):
            await self.service.delete(already_exists)
        else:
            assert already_exists == Error("He удалось найти данного пользователя по email!")

        user = await self.service.register(self.user)
        assert isinstance(user, User)

        self.user.user_id = user.user_id
        reg_user = await self.service.get_user_by_id(self.user.user_id if self.user.user_id else 0)
        assert self.user == reg_user

        assert isinstance(self.user.email, str)
        assert isinstance(self.user.password, str)
        log_user_success = await self.service.login(self.user.email, self.user.password)
        log_user_failure = await self.service.login(self.user.email, "wrong password")
        assert self.user == log_user_success
        assert log_user_failure == Error("He удалось залогиниться!")

        self.user.password = "2"
        change_password_user = await self.service.update(self.user)
        assert isinstance(change_password_user, UserDB)
        assert change_password_user.password == "2"

        assert isinstance(self.user.user_id, int)
        delete_user = await self.service.delete(self.user.user_id)
        assert self.user == delete_user


@allure.epic("Marketplace")
@allure.feature("TestProduct")
class TestProduct(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.session_maker = SessionMaker("pyproject.toml", True)
        self.table = ProductDB
        self.repo = ProductRepository(self.table, self.session_maker)
        self.service = ProductService(self.repo, self.logger)
        self.product = Product(product_id=None, title="Apple", price=1, rate=4.5)
        self.execution_failed = execution_failed

    async def tearDown(self):
        global execution_failed
        if self._outcome.errors:
            for test, err in self._outcome.errors:
                if test is self:
                    execution_failed = True

    def skip_if_failed(self):
        if self.execution_failed:
            self.skipTest("Previous test failed, skipping this test.")

    @allure.story("testRepository")
    async def testRepository(self) -> None:
        assert isinstance(self.product.title, str)

        already_exists = await self.repo.get_product_by_title(self.product.title)
        if isinstance(already_exists, self.table):
            await self.repo.delete(already_exists)
        else:
            assert already_exists == Error("He удалось найти товар по названию!")

        product = await self.service.create(self.product, seller_id=1)
        assert isinstance(product, Product)

        self.product.product_id = product.product_id
        assert isinstance(self.product.product_id, int)
        create_user = await self.repo.get_product_by_id(self.product.product_id)
        assert self.product == create_user

        self.product.price = 2
        change_price_product = await self.repo.update(self.product)
        assert isinstance(change_price_product, self.table)
        assert change_price_product.price == 2

        delete_product = await self.repo.delete(self.product.product_id)
        assert self.product == delete_product

    @allure.story("testService")
    async def testService(self) -> None:
        assert isinstance(self.product.title, str)

        already_exists = await self.service.get_product_by_title(self.product.title)
        if isinstance(already_exists, self.table):
            await self.service.delete(already_exists)
        else:
            assert already_exists == Error("He удалось найти товар по названию!")

        product = await self.service.create(self.product, seller_id=1)
        assert isinstance(product, Product)

        self.product.product_id = product.product_id
        assert isinstance(self.product.product_id, int)
        create_user = await self.service.get_product_by_id(self.product.product_id)
        assert self.product == create_user

        self.product.price = 2
        change_price_product = await self.service.update(self.product)
        assert isinstance(change_price_product, self.table)
        assert change_price_product.price == 2

        delete_product = await self.service.delete(self.product.product_id)
        assert self.product == delete_product


@allure.epic("Marketplace")
@allure.feature("TestOrder")
class TestOrder(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.session_maker = SessionMaker("pyproject.toml", True)
        self.table = OrderDB
        self.repo = OrderRepository(self.table, self.session_maker)
        self.service = OrderService(self.repo, self.logger)
        self.order = Order(order_id=None, all_price=1500, address='Russia', user_id=1)
        self.execution_failed = execution_failed

    async def tearDown(self):
        global execution_failed
        if self._outcome.errors:
            for test, err in self._outcome.errors:
                if test is self:
                    execution_failed = True

    def skip_if_failed(self):
        if self.execution_failed:
            self.skipTest("Previous test failed, skipping this test.")

    @allure.story("testRepository")
    async def testRepository(self) -> None:
        assert isinstance(self.order.user_id, int)

        already_exists = await self.repo.get_order_by_id(self.order.user_id)
        if isinstance(already_exists, self.table):
            await self.repo.delete(already_exists)
        else:
            assert already_exists == Error("He удалось найти заказ по id пользователя!")

        order = await self.repo.create(self.order)
        assert isinstance(order, Order)

        self.order.order_id = order.order_id
        assert isinstance(self.order.order_id, int)
        create_order = await self.repo.get_order_by_id(self.order.order_id)
        assert self.order == create_order

        self.order.all_price = 2500
        change_price_order = await self.repo.update(self.order)
        assert isinstance(change_price_order, self.table)
        assert change_price_order.all_price == 2500

        delete_order = await self.repo.delete(self.order.order_id)
        assert self.order == delete_order

    @allure.story("testService")
    async def testService(self) -> None:
        assert isinstance(self.order.user_id, int)

        already_exists = await self.service.get_order_by_id(self.order.user_id)
        if isinstance(already_exists, self.table):
            await self.service.delete(already_exists)
        else:
            assert already_exists == Error("He удалось найти заказ по id пользователя!")

        order = await self.service.create(self.order)
        assert isinstance(order, Order)

        self.order.order_id = order.order_id
        assert isinstance(self.order.order_id, int)
        create_order = await self.service.get_order_by_id(self.order.order_id)
        assert self.order == create_order

        self.order.all_price = 2500
        change_price_order = await self.service.update(self.order)
        assert isinstance(change_price_order, self.table)
        assert change_price_order.all_price == 2500

        delete_order = await self.service.delete(self.order.order_id)
        assert self.order == delete_order


@allure.epic("Marketplace")
@allure.feature("TestPayment")
class TestPayment(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.session_maker = SessionMaker("pyproject.toml", True)
        self.table = PaymentDB
        self.repo = PaymentRepository(self.table, self.session_maker)
        self.service = PaymentService(self.repo, self.logger)
        self.payment = Payment(payment_id=None, all_price=1000, state="passed", user_id=1)
        self.execution_failed = execution_failed

    async def tearDown(self):
        global execution_failed
        if self._outcome.errors:
            for test, err in self._outcome.errors:
                if test is self:
                    execution_failed = True

    def skip_if_failed(self):
        if self.execution_failed:
            self.skipTest("Previous test failed, skipping this test.")

    @allure.story("testRepository")
    async def testRepository(self) -> None:
        assert isinstance(self.payment.user_id, int)

        already_exists = await self.service.get_payment_by_user_id(self.payment.user_id)
        if isinstance(already_exists, self.table):
            await self.repo.delete(already_exists)
        else:
            assert already_exists == Error("He удалось найти оплату по id пользователя!")

        payment = await self.repo.create(1)
        assert isinstance(payment, Payment)

        self.payment.payment_id = payment.payment_id
        assert isinstance(self.payment.payment_id, int)
        create_order = await self.repo.get_payment_by_user_id(self.payment.user_id)
        assert self.payment == create_order

        self.payment.all_price = 2500
        change_price_payment = await self.repo.update(self.payment)
        assert isinstance(change_price_payment, self.table)
        assert change_price_payment.all_price == 2500

        delete_payment = await self.repo.delete(self.payment.payment_id)
        assert self.payment == delete_payment

    @allure.story("testService")
    async def testService(self) -> None:
        assert isinstance(self.payment.user_id, int)

        already_exists = await self.service.get_payment_by_user_id(self.payment.user_id)
        if isinstance(already_exists, self.table):
            await self.service.delete(already_exists)
        else:
            assert already_exists == Error("He удалось найти оплату по id пользователя!")

        payment = await self.service.create(1)
        assert isinstance(payment, Payment)

        self.payment.payment_id = payment.payment_id
        assert isinstance(self.payment.payment_id, int)
        create_order = await self.service.get_payment_by_user_id(self.payment.user_id)
        assert self.payment == create_order

        self.payment.all_price = 2500
        change_price_payment = await self.service.update(self.payment)
        assert isinstance(change_price_payment, self.table)
        assert change_price_payment.all_price == 2500

        delete_payment = await self.service.delete(self.payment.payment_id)
        assert self.payment == delete_payment


@allure.epic("Marketplace")
@allure.feature("TestCart")
class TestCart(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.session_maker = SessionMaker("pyproject.toml", True)
        self.table = CartDB
        self.repo = CartRepository(self.table, self.session_maker)
        self.service = CartService(self.repo, self.logger)
        self.cart = Cart(Cart_id=None, all_price=1000, user_id=1)
        self.execution_failed = execution_failed

    async def tearDown(self):
        global execution_failed
        if self._outcome.errors:
            for test, err in self._outcome.errors:
                if test is self:
                    execution_failed = True

    def skip_if_failed(self):
        if self.execution_failed:
            self.skipTest("Previous test failed, skipping this test.")

    @allure.story("testRepository")
    async def testRepository(self) -> None:
        assert isinstance(self.cart.user_id, int)

        cart = await self.repo.create(self.cart)
        assert isinstance(cart, Cart)

        self.cart.cart_id = cart.cart_id
        assert isinstance(self.cart.cart_id, int)
        create_order = await self.repo.get_cart_by_id(self.cart.user_id)
        assert self.cart == create_order

        self.cart.all_price = 2500
        change_price_cart = await self.repo.update(self.cart)
        assert isinstance(change_price_cart, self.table)
        assert change_price_cart.all_price == 2500

    @allure.story("testService")
    async def testService(self) -> None:
        assert isinstance(self.cart.user_id, int)

        cart = await self.service.create(self.cart)
        assert isinstance(cart, Cart)

        self.cart.cart_id = cart.cart_id
        assert isinstance(self.cart.cart_id, int)
        create_order = await self.service.get_cart_by_id(self.cart.user_id)
        assert self.cart == create_order

        self.cart.all_price = 2500
        change_price_cart = await self.service.update(self.cart)
        assert isinstance(change_price_cart, self.table)
        assert change_price_cart.all_price == 2500


@allure.epic("Marketplace")
@allure.feature("TestProductCart")
class TestProductCart(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.session_maker = SessionMaker("pyproject.toml", True)
        self.table = ProductCartDB
        self.repo = ProductCartRepository(self.table, self.session_maker)
        self.service = ProductCartService(self.repo, self.logger)
        self.product_cart = ProductCart(product_id=1, cart_id=1, quantity=1)
        self.execution_failed = execution_failed

    async def tearDown(self):
        global execution_failed
        if self._outcome.errors:
            for test, err in self._outcome.errors:
                if test is self:
                    execution_failed = True

    def skip_if_failed(self):
        if self.execution_failed:
            self.skipTest("Previous test failed, skipping this test.")

    @allure.story("testRepository")
    async def testRepository(self) -> None:
        assert isinstance(self.product_cart.product_id, int)
        assert isinstance(self.product_cart.cart_id, int)

        already_exists = await self.repo.get_products_cart_by_id(self.product_cart.cart_id)
        if isinstance(already_exists, self.table):
            await self.repo.delete(already_exists.product_id, already_exists.cart_id)
        else:
            assert already_exists == Error("He удалось найти товар в корзине!")

        product_cart = await self.repo.create(self.product_cart)
        assert isinstance(product_cart, ProductCart)

        self.product_cart.cart_id = product_cart.cart_id
        self.product_cart.product_id = product_cart.product_id
        assert isinstance(self.product_cart.cart_id, int)
        assert isinstance(self.product_cart.product_id, int)
        create_order = await self.repo.get_products_cart_by_id(self.product_cart.cart_id)
        assert self.product_cart == create_order

        self.product_cart.quantity = 10
        change_price_product_cart = await self.repo.update(self.product_cart)
        assert isinstance(change_price_product_cart, self.table)
        assert change_price_product_cart.all_price == 10

        delete_order = await self.repo.delete(self.product_cart.product_id, self.product_cart.cart_id)
        assert self.product_cart == delete_order

    @allure.story("testService")
    async def testService(self) -> None:
        assert isinstance(self.product_cart.product_id, int)
        assert isinstance(self.product_cart.cart_id, int)

        already_exists = await self.service.get_products_cart_by_id(self.product_cart.cart_id)
        if isinstance(already_exists, self.table):
            await self.service.delete(already_exists.product_id, already_exists.cart_id)
        else:
            assert already_exists == Error("He удалось найти товар в корзине!")

        product_cart = await self.service.create(self.product_cart)
        assert isinstance(product_cart, ProductCart)

        self.product_cart.cart_id = product_cart.cart_id
        self.product_cart.product_id = product_cart.product_id
        assert isinstance(self.product_cart.cart_id, int)
        assert isinstance(self.product_cart.product_id, int)
        create_order = await self.service.get_products_cart_by_id(self.product_cart.cart_id)
        assert self.product_cart == create_order

        self.product_cart.quantity = 10
        change_price_product_cart = await self.service.update(self.product_cart)
        assert isinstance(change_price_product_cart, self.table)
        assert change_price_product_cart.all_price == 10

        delete_order = await self.service.delete(self.product_cart.product_id, self.product_cart.cart_id)
        assert self.product_cart == delete_order


@allure.epic("Marketplace")
@allure.feature("TestProductOrder")
class TestProductOrder(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.session_maker = SessionMaker("pyproject.toml", True)
        self.table = ProductOrderDB
        self.repo = ProductOrderRepository(self.table, self.session_maker)
        self.service = ProductOrderService(self.repo, self.logger)
        self.product_order = ProductOrder(product_id=1, order_id=1, quantity=1)
        self.execution_failed = execution_failed

    async def tearDown(self):
        global execution_failed
        if self._outcome.errors:
            for test, err in self._outcome.errors:
                if test is self:
                    execution_failed = True

    def skip_if_failed(self):
        if self.execution_failed:
            self.skipTest("Previous test failed, skipping this test.")

    @allure.story("testRepository")
    async def testRepository(self) -> None:
        assert isinstance(self.product_order.product_id, int)
        assert isinstance(self.product_order.order_id, int)

        already_exists = await self.repo.get_products_order_by_id(self.product_order.order_id)
        if isinstance(already_exists, self.table):
            await self.repo.delete(already_exists.product_id, already_exists.order_id)
        else:
            assert already_exists == Error("He удалось найти товар в корзине!")

        product_order = await self.repo.create(self.product_order)
        assert isinstance(product_order, ProductOrder)

        self.product_order.order_id = product_order.order_id
        self.product_order.product_id = product_order.product_id
        assert isinstance(self.product_order.order_id, int)
        assert isinstance(self.product_order.product_id, int)
        create_order = await self.repo.get_products_order_by_id(self.product_order.order_id)
        assert self.product_order == create_order

        self.product_order.quantity = 10
        change_price_product_order = await self.repo.update(self.product_order)
        assert isinstance(change_price_product_order, self.table)
        assert change_price_product_order.quantity == 10

        delete_order = await self.repo.delete(self.product_order.product_id, self.product_order.order_id)
        assert self.product_order == delete_order

    @allure.story("testService")
    async def testService(self) -> None:
        assert isinstance(self.product_order.product_id, int)
        assert isinstance(self.product_order.order_id, int)

        already_exists = await self.service.get_products_order_by_id(self.product_order.order_id)
        if isinstance(already_exists, self.table):
            await self.service.delete(already_exists.product_id, already_exists.order_id)
        else:
            assert already_exists == Error("He удалось найти товар в корзине!")

        product_order = await self.service.create(self.product_order)
        assert isinstance(product_order, ProductOrder)

        self.product_order.order_id = product_order.order_id
        self.product_order.product_id = product_order.product_id
        assert isinstance(self.product_order.order_id, int)
        assert isinstance(self.product_order.product_id, int)
        create_order = await self.service.get_products_order_by_id(self.product_order.order_id)
        assert self.product_order == create_order

        self.product_order.quantity = 10
        change_price_product_order = await self.service.update(self.product_order)
        assert isinstance(change_price_product_order, self.table)
        assert change_price_product_order.quantity == 10

        delete_order = await self.service.delete(self.product_order.product_id, self.product_order.order_id)
        assert self.product_order == delete_order


if __name__ == '__main__':
    unittest.main()
