from __future__ import annotations

import unittest
import allure
from unittest.mock import MagicMock

from marketplace.Order.service import OrderService
from tests.objectsMother import ObjectsMother


@allure.epic("Marketplace")
@allure.feature("Cart Service")
class TestCartService(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.repo = MagicMock()
        self.service = OrderService(self.repo, self.logger)
        self.objectsMother = ObjectsMother()

    @allure.title("Test adding payment successfully")
    async def test_add_payment_success(self) -> None:
        with allure.step("Setup repo mock and call create"):
            self.repo.get_payment_by_user_id.return_value = self.objectsMother.get_order()
            self.repo.create.return_value = True

        with allure.step("Execute create method and verify result"):
            result = await self.service.create(self.objectsMother.get_order())
            self.assertEqual(result, True)

    @allure.title("Test failing to add payment")
    async def test_add_payment_failure(self) -> None:
        with allure.step("Setup repo mock to return None"):
            self.repo.get_payment_by_user_id.return_value = None

        with allure.step("Execute create method and verify result is None"):
            result = await self.service.create(self.objectsMother.get_order())
            self.assertEqual(result, None)

    @allure.title("Test removing payment successfully")
    async def test_remove_payment_success(self) -> None:
        with allure.step("Setup repo mock to allow deletion"):
            self.repo.remove.return_value = True

        with allure.step("Execute delete method and verify result"):
            result = await self.service.delete(1)
            self.assertEqual(result, True)

    @allure.title("Test failing to remove payment")
    async def test_remove_payment_failure(self) -> None:
        with allure.step("Setup repo mock to prevent deletion"):
            self.repo.remove.return_value = False

        with allure.step("Execute delete method and verify result is False"):
            result = await self.service.delete(1)
            self.assertEqual(result, False)

    @allure.title("Test updating payment successfully")
    async def test_update_payment_success(self) -> None:
        updated_payment = self.objectsMother.get_payment()
        with allure.step("Setup repo mock to return updated payment"):
            self.repo.update.return_value = updated_payment

        with allure.step("Execute update method and verify result"):
            result = await self.service.update(updated_payment)
            self.assertEqual(result, updated_payment)

    @allure.title("Test failing to update payment")
    async def test_update_payment_failure(self) -> None:
        with allure.step("Setup repo mock to return None on update"):
            self.repo.update.return_value = None
            payment_to_update = self.objectsMother.get_payment()

        with allure.step("Execute update method and verify result is None"):
            result = await self.service.update(payment_to_update)
            self.assertEqual(result, None)

    @allure.title("Test getting payment by ID successfully")
    async def test_get_payment_by_id_success(self) -> None:
        payment = self.objectsMother.get_payment()
        with allure.step("Setup repo mock to return a payment"):
            self.repo.get_payment_by_user_id.return_value = payment

        with allure.step("Execute get_payment_by_user_id method and verify result"):
            result = await self.service.get_order_by_id(1)
            self.assertEqual(result, payment)

    @allure.title("Test failing to get payment by ID")
    async def test_get_payment_by_id_failure(self) -> None:
        with allure.step("Setup repo mock to return None"):
            self.repo.get_payment_by_user_id.return_value = None

        with allure.step("Execute get_payment_by_user_id method and verify result is None"):
            result = await self.service.get_order_by_id(1)
            self.assertEqual(result, None)

    @allure.story("Get All Orders")
    @allure.title("Test get all orders success")
    async def test_get_all_orders_success(self) -> None:
        with allure.step("Mock repository to simulate successful retrieval of all orders"):
            self.repo.get_all_orders.return_value = not None

        with allure.step("Attempt to retrieve all carts"):
            result = await self.service.get_all_orders()

        with allure.step("Verify retrieval of all orders was successful"):
            self.assertEqual(result, True)

    @allure.story("Get All Orders")
    @allure.title("Test get all orders failure")
    async def test_get_all_orders_failure(self) -> None:
        with allure.step("Mock repository to simulate failed retrieval of all orders"):
            self.repo.get_all_carts.return_value = self.objectsMother.get_error()

        with allure.step("Attempt to retrieve all carts"):
            result = await self.service.get_all_orders()

        with allure.step("Verify retrieval of all orders failed"):
            self.assertEqual(result, self.objectsMother.get_error())

    @allure.story("Get All Orders Error")
    @allure.title("Test get all orders failure due to database error")
    async def test_get_all_orders_failure_due_to_db_error(self) -> None:
        error_message = "Database connection error"

        with allure.step("Mock repository to simulate database connection error"):
            # Предполагается, что self.repo.get_all_carts является асинхронным методом
            self.repo.get_all_carts = Exception(error_message)

        with allure.step("Attempt to retrieve all carts"):
            try:
                result = await self.service.get_all_orders()
            except Exception as e:
                result = str(e)

        with allure.step("Verify database connection error was handled properly"):
            self.assertEqual(result, error_message)


if __name__ == '__main__':
    unittest.main()
