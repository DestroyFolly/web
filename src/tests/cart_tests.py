from __future__ import annotations

import unittest
import allure
from unittest.mock import MagicMock

from marketplace.Cart.service import CartService
from tests.objectsMother import ObjectsMother


@allure.epic("Marketplace")
@allure.feature("Cart Service")
class TestCartService(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.repo = MagicMock()
        self.service = CartService(self.repo, self.logger)
        self.objectsMother = ObjectsMother()

    @allure.story("Add Product")
    @allure.title("Test add product success")
    async def test_add_product_success(self) -> None:
        with allure.step("Mock repository to simulate existing user cart and successful cart creation"):
            self.repo.get_cart_by_user_id.return_value = not None
            self.repo.create.return_value = True

        with allure.step("Attempt to create a new cart"):
            result = await self.service.create(self.objectsMother.get_cart())

        with allure.step("Verify cart creation was successful"):
            self.assertEqual(result, True)

    @allure.story("Add Product")
    @allure.title("Test add product failure")
    async def test_add_product_failure(self) -> None:
        with allure.step("Mock repository to simulate non-existing user cart"):
            self.repo.get_cart_by_user_id.return_value = None

        with allure.step("Attempt to create a new cart"):
            result = await self.service.create(self.objectsMother.get_cart())

        with allure.step("Verify cart creation failed"):
            self.assertEqual(result, None)

    @allure.story("Update Product")
    @allure.title("Test update product success")
    async def test_update_product_success(self) -> None:
        with allure.step("Mock repository to simulate successful cart update"):
            self.repo.update.return_value = not None

        with allure.step("Attempt to update the cart"):
            result = await self.service.update(self.objectsMother.get_cart())

        with allure.step("Verify cart update was successful"):
            self.assertEqual(result, True)

    @allure.story("Update Product")
    @allure.title("Test update product failure")
    async def test_update_product_failure(self) -> None:
        with allure.step("Mock repository to simulate failed cart update"):
            self.repo.update.return_value = self.objectsMother.get_error()

        with allure.step("Attempt to update the cart"):
            result = await self.service.update(self.objectsMother.get_cart())

        with allure.step("Verify cart update failed"):
            self.assertEqual(result, self.objectsMother.get_error())

    @allure.story("Get Cart")
    @allure.title("Test get cart by ID success")
    async def test_get_cart_by_id_success(self) -> None:
        with allure.step("Mock repository to simulate existing cart retrieval by ID"):
            cart = self.objectsMother.get_cart()
            self.repo.get_cart_by_user_id.return_value = self.objectsMother.get_cart()

        with allure.step("Attempt to retrieve cart by ID"):
            result = await self.service.get_cart_by_id(1)

        with allure.step("Verify cart retrieval by ID was successful"):
            self.assertEqual(result, cart)

    @allure.story("Get Cart")
    @allure.title("Test get cart by ID failure")
    async def test_get_cart_by_id_failure(self) -> None:
        with allure.step("Mock repository to simulate non-existing cart retrieval by ID"):
            self.repo.get_cart_by_user_id.return_value = None

        with allure.step("Attempt to retrieve cart by ID"):
            result = await self.service.get_cart_by_id(1)

        with allure.step("Verify cart retrieval byID failed"):
            self.assertEqual(result, None)

    @allure.story("Get All Carts")
    @allure.title("Test get all carts success")
    async def test_get_all_carts_success(self) -> None:
        with allure.step("Mock repository to simulate successful retrieval of all carts"):
            self.repo.get_all_carts.return_value = not None

        with allure.step("Attempt to retrieve all carts"):
            result = await self.service.get_all_carts()

        with allure.step("Verify retrieval of all carts was successful"):
            self.assertEqual(result, True)

    @allure.story("Get All Carts")
    @allure.title("Test get all carts failure")
    async def test_get_all_carts_failure(self) -> None:
        with allure.step("Mock repository to simulate failed retrieval of all carts"):
            self.repo.get_all_carts.return_value = self.objectsMother.get_error()

        with allure.step("Attempt to retrieve all carts"):
            result = await self.service.get_all_carts()

        with allure.step("Verify retrieval of all carts failed"):
            self.assertEqual(result, self.objectsMother.get_error())


if __name__ == '__main__':
    unittest.main()
