from __future__ import annotations

import unittest
import allure
from unittest.mock import MagicMock

from marketplace.Product_Order.service import ProductOrderService
from tests.objectsMother import ObjectsMother


@allure.epic("Marketplace")
@allure.feature("Product Order Service")
class TestProductOrderService(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.repo = MagicMock()
        self.service = ProductOrderService(self.repo, self.logger)
        self.objectsMother = ObjectsMother()

    @allure.story("Add ProductOrder")
    @allure.title("Test add product Order success")
    async def test_add_product_Order_success(self) -> None:
        with allure.step("Mock repository to simulate existing user product Order and successful creation"):
            self.repo.get_product_Order_by_user_id.return_value = not None
            self.repo.create.return_value = True

        with allure.step("Attempt to create a new product Order"):
            result = await self.service.create(1)

        with allure.step("Verify product Order creation was successful"):
            self.assertEqual(result, True)

    @allure.story("Add ProductOrder")
    @allure.title("Test add product Order failure")
    async def test_add_product_Order_failure(self) -> None:
        with allure.step("Mock repository to simulate non-existing user product Order"):
            self.repo.get_product_Order_by_user_id.return_value = None

        with allure.step("Attempt to create a new product Order"):
            result = await self.service.create(1)

        with allure.step("Verify product Order creation failed"):
            self.assertEqual(result, None)

    @allure.story("Remove ProductOrder")
    @allure.title("Test remove product Order success")
    async def test_remove_product_Order_success(self) -> None:
        with allure.step("Mock repository to simulate successful product Order removal"):
            self.repo.remove.return_value = True

        with allure.step("Attempt to remove product Order"):
            result = await self.service.delete(1)

        with allure.step("Verify product Order removal was successful"):
            self.assertEqual(result, True)

    @allure.story("Remove ProductOrder")
    @allure.title("Test remove product Order failure")
    async def test_remove_product_Order_failure(self) -> None:
        with allure.step("Mock repository to simulate failed product Order removal"):
            self.repo.remove.return_value = False

        with allure.step("Attempt to remove product Order"):
            result = await self.service.delete(1)

        with allure.step("Verify product Order removal failed"):
            self.assertEqual(result, False)

    @allure.story("Update ProductOrder")
    @allure.title("Test update product Order success")
    async def test_update_product_Order_success(self) -> None:
        with allure.step("Mock repository to simulate successful product Order update"):
            updated_product_Order = self.objectsMother.get_product_order()
            self.repo.update.return_value = updated_product_Order

        with allure.step("Attempt to update product Order"):
            result = await self.service.update(updated_product_Order)

        with allure.step("Verify product Order update was successful"):
            self.assertEqual(result, updated_product_Order)

    @allure.story("Update ProductOrder")
    @allure.title("Test update product Order failure")
    async def test_update_product_Order_failure(self) -> None:
        with allure.step("Mock repository to simulate failed product Order update"):
            self.repo.update.return_value = None
            product_order_to_update = self.objectsMother.get_product_order()

        with allure.step("Attempt to update product Order"):
            result = await self.service.update(product_order_to_update)

        with allure.step("Verify product Order update failed"):
            self.assertEqual(result, None)

    @allure.story("Get ProductOrder by ID")
    @allure.title("Test get product Order by ID success")
    async def test_get_product_Order_by_id_success(self) -> None:
        with allure.step("Mock repository to return a product Order for a given user ID"):
            product_order = self.objectsMother.get_product_order()
            self.repo.get_product_Order_by_user_id.return_value = product_order

        with allure.step("Attempt to retrieve product Order by user ID"):
            result = await self.service.get_product_order_by_user_id(1)

        with allure.step("Verify retrieved product Order is correct"):
            self.assertEqual(result, product_order)

    @allure.story("Get ProductOrder by ID")
    @allure.title("Test get product Order by ID failure")
    async def test_get_product_Order_by_id_failure(self) -> None:
        with allure.step("Mock repository to simulate no product Order found for the given user ID"):
            self.repo.get_product_Order_by_user_id.return_value = None

        with allure.step("Attempt to retrieve product Order by user ID"):
            result = await self.service.get_product_order_by_user_id(1)

        with allure.step("Verify product Order retrieval failed"):
            self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
