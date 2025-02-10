from __future__ import annotations

import unittest
import allure
from unittest.mock import MagicMock

from marketplace.Product_Cart.service import ProductCartService
from tests.objectsMother import ObjectsMother


@allure.epic("Marketplace")
@allure.feature("Product Cart Service")
class TestProductCartService(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.repo = MagicMock()
        self.service = ProductCartService(self.repo, self.logger)
        self.objectsMother = ObjectsMother()

    @allure.story("Add ProductCart")
    @allure.title("Test add product cart success")
    async def test_add_product_cart_success(self) -> None:
        with allure.step("Mock repository to simulate existing user product cart and successful creation"):
            self.repo.get_product_cart_by_user_id.return_value = not None
            self.repo.create.return_value = True

        with allure.step("Attempt to create a new product cart"):
            result = await self.service.create(1)

        with allure.step("Verify product cart creation was successful"):
            self.assertEqual(result, True)

    @allure.story("Add ProductCart")
    @allure.title("Test add product cart failure")
    async def test_add_product_cart_failure(self) -> None:
        with allure.step("Mock repository to simulate non-existing user product cart"):
            self.repo.get_product_cart_by_user_id.return_value = None

        with allure.step("Attempt to create a new product cart"):
            result = await self.service.create(1)

        with allure.step("Verify product cart creation failed"):
            self.assertEqual(result, None)

    @allure.story("Remove ProductCart")
    @allure.title("Test remove product cart success")
    async def test_remove_product_cart_success(self) -> None:
        with allure.step("Mock repository to simulate successful product cart removal"):
            self.repo.remove.return_value = True

        with allure.step("Attempt to remove product cart"):
            result = await self.service.delete(1)

        with allure.step("Verify product cart removal was successful"):
            self.assertEqual(result, True)

    @allure.story("Remove ProductCart")
    @allure.title("Test remove product cart failure")
    async def test_remove_product_cart_failure(self) -> None:
        with allure.step("Mock repository to simulate failed product cart removal"):
            self.repo.remove.return_value = False

        with allure.step("Attempt to remove product cart"):
            result = await self.service.delete(1)

        with allure.step("Verify product cart removal failed"):
            self.assertEqual(result, False)

    @allure.story("Update ProductCart")
    @allure.title("Test update product cart success")
    async def test_update_product_cart_success(self) -> None:
        with allure.step("Mock repository to simulate successful product cart update"):
            updated_product_cart = self.objectsMother.get_product_cart()
            self.repo.update.return_value = updated_product_cart

        with allure.step("Attempt to update product cart"):
            result = await self.service.update(updated_product_cart)

        with allure.step("Verify product cart update was successful"):
            self.assertEqual(result, updated_product_cart)

    @allure.story("Update ProductCart")
    @allure.title("Test update product cart failure")
    async def test_update_product_cart_failure(self) -> None:
        with allure.step("Mock repository to simulate failed product cart update"):
            self.repo.update.return_value = None
            product_cart_to_update = self.objectsMother.get_product_cart()

        with allure.step("Attempt to update product cart"):
            result = await self.service.update(product_cart_to_update)

        with allure.step("Verify product cart update failed"):
            self.assertEqual(result, None)

    @allure.story("Get ProductCart by ID")
    @allure.title("Test get product cart by ID success")
    async def test_get_product_cart_by_id_success(self) -> None:
        with allure.step("Mock repository to return a product cart for a given user ID"):
            product_cart = self.objectsMother.get_product_cart()
            self.repo.get_product_cart_by_user_id.return_value = product_cart

        with allure.step("Attempt to retrieve product cart by user ID"):
            result = await self.service.get_product_cart_by_user_id(1)

        with allure.step("Verify retrieved product cart is correct"):
            self.assertEqual(result, product_cart)

    @allure.story("Get ProductCart by ID")
    @allure.title("Test get product cart by ID failure")
    async def test_get_product_cart_by_id_failure(self) -> None:
        with allure.step("Mock repository to simulate no product cart found for the given user ID"):
            self.repo.get_product_cart_by_user_id.return_value = None

        with allure.step("Attempt to retrieve product cart by user ID"):
            result = await self.service.get_product_cart_by_user_id(1)

        with allure.step("Verify product cart retrieval failed"):
            self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
