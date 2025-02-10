from __future__ import annotations
import unittest
from unittest.mock import MagicMock
import allure
from marketplace.Product.service import ProductService
from tests.objectsMother import ObjectsMother


@allure.epic("Marketplace")
@allure.feature("Product Service")
class TestCartService(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.repo = MagicMock()
        self.service = ProductService(self.repo, self.logger)
        self.objectsMother = ObjectsMother()

    @allure.story("Add Product")
    @allure.title("Test add product success")
    async def test_add_product_success(self) -> None:
        with allure.step("Set up mock for successful product retrieval and creation"):
            self.repo.get_product_by_user_id.return_value = not None
            self.repo.create.return_value = True

        with allure.step("Attempt to create product"):
            result = await self.service.create(self.objectsMother.get_product())

        with allure.step("Verify product creation was successful"):
            self.assertEqual(result, True)

    @allure.story("Add Product")
    @allure.title("Test add product failure")
    async def test_add_product_failure(self) -> None:
        with allure.step("Set up mock for failed product retrieval"):
            self.repo.get_product_by_user_id.return_value = None

        with allure.step("Attempt to create a product"):
            result = await self.service.create(self.objectsMother.get_product())

        with allure.step("Verify product creation failed"):
            self.assertEqual(result, None)

    @allure.story("Remove Product")
    @allure.title("Test remove product success")
    async def test_remove_product_success(self) -> None:
        with allure.step("Set up mock for successful product retrieval and deletion"):
            self.repo.get_product_by_user_id.return_value = not None
            self.repo.update.return_value = True

        with allure.step("Attempt to delete product"):
            result = await self.service.delete(1)

        with allure.step("Verify product deletion was successful"):
            self.assertEqual(result, True)

    @allure.story("Remove Product")
    @allure.title("Test remove product failure")
    async def test_remove_product_failure(self) -> None:
        with allure.step("Set up mock for failed product retrieval"):
            self.repo.get_product_by_user_id.return_value = None

        with allure.step("Attempt to delete product"):
            result = await self.service.delete(1)

        with allure.step("Verify product deletion failed"):
            self.assertEqual(result, None)

    @allure.title("Test updating product successfully")
    async def test_update_product_success(self) -> None:
        updated_product = self.objectsMother.get_payment()
        with allure.step("Setup repo mock to return updated product"):
            self.repo.update.return_value = updated_product

        with allure.step("Execute update method and verify result"):
            result = await self.service.update(updated_product)
            self.assertEqual(result, updated_product)

    @allure.title("Test failing to update product")
    async def test_update_payment_failure(self) -> None:
        with allure.step("Setup repo mock to return None on update"):
            self.repo.update.return_value = None
            product_to_update = self.objectsMother.get_product()

        with allure.step("Execute update method and verify result is None"):
            result = await self.service.update(product_to_update)
            self.assertEqual(result, None)

    @allure.story("Get Product")
    @allure.title("Test get product by ID success")
    async def test_get_product_by_id_success(self) -> None:
        with allure.step("Set up mock for successful product retrieval"):
            product = self.objectsMother.get_product()
            self.repo.get_product_by_user_id.return_value = product

        with allure.step("Attempt to retrieve product by ID"):
            result = await self.service.get_product_by_id(1)

        with allure.step("Verify product retrieval was successful"):
            self.assertEqual(result, product)

    @allure.story("Get Product")
    @allure.title("Test get product by ID failure")
    async def test_get_product_by_id_failure(self) -> None:
        with allure.step("Set up mock for failed product retrieval"):
            self.repo.get_product_by_user_id.return_value = None

            with allure.step("Attempt to retrieve product by ID"):
                result = await self.service.get_product_by_id(1)

            with allure.step("Verify product retrieval failed"):
                self.assertEqual(result, None)

    @allure.story("Get All Products")
    @allure.title("Test get all products success")
    async def test_get_all_products_success(self) -> None:
        with allure.step("Mock repository to simulate successful retrieval of all products"):
            self.repo.get_all_carts.return_value = not None

        with allure.step("Attempt to retrieve all products"):
            result = await self.service.get_all_products()

        with allure.step("Verify retrieval of all products was successful"):
            self.assertEqual(result, True)

    @allure.story("Get All Products")
    @allure.title("Test get all products failure")
    async def test_get_all_carts_failure(self) -> None:
        with allure.step("Mock repository to simulate failed retrieval of all products"):
            self.repo.get_all_carts.return_value = self.objectsMother.get_error()

        with allure.step("Attempt to retrieve all products"):
            result = await self.service.get_all_products()

        with allure.step("Verify retrieval of all products failed"):
            self.assertEqual(result, self.objectsMother.get_error())


if __name__ == 'main':
    unittest.main()
