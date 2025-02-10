from __future__ import annotations

import unittest
import allure
from unittest.mock import MagicMock

from marketplace.Payment.service import PaymentService
from tests.objectsMother import ObjectsMother


@allure.epic("Marketplace")
@allure.feature("Payment Service")
class TestPaymentService(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.repo = MagicMock()
        self.service = PaymentService(self.repo, self.logger)
        self.objectsMother = ObjectsMother()

    @allure.story("Add Payment")
    @allure.title("Test add payment success")
    async def test_add_payment_success(self) -> None:
        with allure.step("Mock repository to simulate existing user payment and successful creation"):
            self.repo.get_payment_by_user_id.return_value = not None
            self.repo.create.return_value = True

        with allure.step("Attempt to create a new payment"):
            result = await self.service.create(1)

        with allure.step("Verify payment creation was successful"):
            self.assertEqual(result, True)

    @allure.story("Add Payment")
    @allure.title("Test add payment failure")
    async def test_add_payment_failure(self) -> None:
        with allure.step("Mock repository to simulate non-existing user payment"):
            self.repo.get_payment_by_user_id.return_value = None

        with allure.step("Attempt to create a new payment"):
            result = await self.service.create(1)

        with allure.step("Verify payment creation failed"):
            self.assertEqual(result, None)

    @allure.story("Remove Payment")
    @allure.title("Test remove payment success")
    async def test_remove_payment_success(self) -> None:
        with allure.step("Mock repository to simulate successful payment removal"):
            self.repo.remove.return_value = True

        with allure.step("Attempt to remove payment"):
            result = await self.service.delete(1)

        with allure.step("Verify payment removal was successful"):
            self.assertEqual(result, True)

    @allure.story("Remove Payment")
    @allure.title("Test remove payment failure")
    async def test_remove_payment_failure(self) -> None:
        with allure.step("Mock repository to simulate failed payment removal"):
            self.repo.remove.return_value = False

        with allure.step("Attempt to remove payment"):
            result = await self.service.delete(1)

        with allure.step("Verify payment removal failed"):
            self.assertEqual(result, False)

    @allure.story("Update Payment")
    @allure.title("Test update payment success")
    async def test_update_payment_success(self) ->None:
        with allure.step("Mock repository to simulate successful payment update"):
            updated_payment = self.objectsMother.get_payment()
            self.repo.update.return_value = updated_payment

        with allure.step("Attempt to update payment"):
            result = await self.service.update(updated_payment)

        with allure.step("Verify payment update was successful"):
            self.assertEqual(result, updated_payment)

    @allure.story("Update Payment")
    @allure.title("Test update payment failure")
    async def test_update_payment_failure(self) -> None:
        with allure.step("Mock repository to simulate failed payment update"):
            self.repo.update.return_value = None
            payment_to_update = self.objectsMother.get_payment()

        with allure.step("Attempt to update payment"):
            result = await self.service.update(payment_to_update)

        with allure.step("Verify payment update failed"):
            self.assertEqual(result, None)

    @allure.story("Get Payment by ID")
    @allure.title("Test get payment by ID success")
    async def test_get_payment_by_id_success(self) -> None:
        with allure.step("Mock repository to return a payment for a given user ID"):
            payment = self.objectsMother.get_payment()
            self.repo.get_payment_by_user_id.return_value = payment

        with allure.step("Attempt to retrieve payment by user ID"):
            result = await self.service.get_payment_by_user_id(1)

        with allure.step("Verify retrieved payment is correct"):
            self.assertEqual(result, payment)

    @allure.story("Get Payment by ID")
    @allure.title("Test get payment by ID failure")
    async def test_get_payment_by_id_failure(self) -> None:
        with allure.step("Mock repository to simulate no payment found for the given user ID"):
            self.repo.get_payment_by_user_id.return_value = None

        with allure.step("Attempt to retrieve payment by user ID"):
            result = await self.service.get_payment_by_user_id(1)

        with allure.step("Verify payment retrieval failed"):
            self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
