import httpx
import unittest
import allure
from marketplace.BD.session import SessionMaker


@allure.epic("Marketplace")
@allure.feature("TestE2E")
class TestE2E(unittest.TestCase):
    def setUp(self) -> None:
        self.BASE_URL = "http://127.0.0.1:5000"
        self.session_maker = SessionMaker("pyproject.toml")
        self.session = self.session_maker.get_session()

    async def tearDown(self):
        await self.session.rollback()

    async def test(self):
        register_data = {
            "email": "admin@admin",
            "password": "admin",
            "money": "10000",
            "phone": "78923121975",
            "role": "admin"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.BASE_URL}/api/v2/users/register", json=register_data)
            assert response.status_code == 201

            login_data = {
                "username": "admin@admin",
                "password": "admin"
            }
            response = await client.post(f"{self.BASE_URL}/api/v2/users/login", json=login_data)
            assert response.status_code == 200
            token = response.json().get('token')
            user_id = order_id = cart_id = response.json().get('user_id')

            update_data = {
                "password": "adminadmin"
            }
            response = await client.patch(f"{self.BASE_URL}/api/v2/users/1", json=update_data,
                                          headers={"Authorization": f"Bearer {token}"})
            assert response.status_code == 200

            products_in_order = {
                1: {"quantity": 1},
                3: {"quantity": 3},
                5: {"quantity": 5},
                7: {"quantity": 7}
            }
            for product_id in products_in_order:
                response = await client.post(f"{self.BASE_URL}/api/v2/orders/{order_id}/products/{product_id}",
                                             json=products_in_order[order_id])
                assert response.status_code == 200

            response = await client.delete(f"{self.BASE_URL}/api/v2/orders/{order_id}/products/{7}")
            assert response.status_code == 200

            update_data = {
                "quantity": 7
            }
            response = await client.patch(f"{self.BASE_URL}/api/v2/orders/{order_id}/products/{5}",
                                          json=update_data)
            assert response.status_code == 200

            products_in_cart = {
                2: {"quantity": 2},
                4: {"quantity": 4}
            }
            for product_id in products_in_cart:
                response = await client.post(f"{self.BASE_URL}/api/v2/carts/{cart_id}/products/{product_id}")
                assert response.status_code == 200

            response = await client.delete(f"{self.BASE_URL}/api/v2/orders/{order_id}/products/{4}")
            assert response.status_code == 200

            update_data = {
                "quantity": 3
            }
            response = await client.patch(f"{self.BASE_URL}/api/v2/orders/{order_id}/products/{2}",
                                          json=update_data)
            assert response.status_code == 200

            response = await client.post(f"{self.BASE_URL}/api/v2/payments/users/{user_id}")
            assert response.status_code == 200

            response = await client.delete(f"{self.BASE_URL}/api/v2/users/{user_id}",
                                           headers={"Authorization": f"Bearer {token}"})
            assert response.status_code == 200
