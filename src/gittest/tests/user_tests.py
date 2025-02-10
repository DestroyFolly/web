from __future__ import annotations

import unittest
import allure
from unittest.mock import MagicMock

from marketplace.User.service import UserService
from tests.objectsMother import ObjectsMother


@allure.epic("Marketplace")
@allure.feature("User Service")
class TestUserService(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = None
        self.repo = MagicMock()
        self.service = UserService(self.repo, self.logger)
        self.objectsMother = ObjectsMother()

    @allure.story("Login")
    @allure.title("Test login success")
    async def test_login_success(self) -> None:
        user = self.objectsMother.get_user()

        with allure.step("Mock repository to return an existing user"):
            self.repo.get_user_by_email.return_value = user

        with allure.step("Attempt to login with valid credentials"):
            result = await self.service.login(user.email, user.password)

        with allure.step("Verify login was successful"):
            self.assertEqual(result, user)

    @allure.story("Login")
    @allure.title("Test login failure")
    async def test_login_failure(self) -> None:
        with allure.step("Mock repository to simulate no matching user found"):
            self.repo.get_user_by_email.return_value = None

        with allure.step("Attempt to login with invalid credentials"):
            result = await self.service.login(self.objectsMother.get_user().email,
                                              self.objectsMother.get_user().password)

        with allure.step("Verify login failed"):
            self.assertEqual(result, None)

    @allure.story("Register")
    @allure.title("Test register success")
    async def test_register_success(self) -> None:
        user = self.objectsMother.get_user()

        with allure.step("Mock repository to simulate no existing user and create a new one"):
            self.repo.get_user_by_email.return_value = None
            self.repo.create.return_value = user

        with allure.step("Attempt to register a new user"):
            result = await self.service.register(user)

        with allure.step("Verify registration was successful"):
            self.assertEqual(result, user)

    @allure.story("Register")
    @allure.title("Test register failure")
    async def test_register_failure(self) -> None:
        user = self.objectsMother.get_user()

        with allure.step("Mock repository to simulate existing user found by email"):
            self.repo.get_user_by_email.return_value = user

        with allure.step("Attempt to register a user that already exists"):
            result = await self.service.register(user)

        with allure.step("Verify registration failed"):
            self.assertEqual(result, None)

    @allure.story("Get User by ID")
    @allure.title("Test get user by ID success")
    async def test_get_user_by_id_success(self) -> None:
        user = self.objectsMother.get_user()

        with allure.step("Mock repository to return a user for a given ID"):
            self.repo.get_user_by_id.return_value = user

        with allure.step("Attempt to retrieve user by ID"):
            result = await self.service.get_user_by_id(1)

        with allure.step("Verify retrieved user is correct"):
            self.assertEqual(result, user)

    @allure.story("Get User by ID")
    @allure.title("Test get user by ID failure")
    async def test_get_user_by_id_failure(self) -> None:
        with allure.step("Mock repository to simulate no user found with the given ID"):
            self.repo.get_user_by_id.return_value = None

        with allure.step("Attempt to retrieve user by an invalid ID"):
            result = await self.service.get_user_by_id(1)

        with allure.step("Verify user retrieval failed"):
            self.assertEqual(result,None)

    @allure.story("Get User by Email")
    @allure.title("Test get user by email success")
    async def test_get_user_by_email_success(self) -> None:
        user = self.objectsMother.get_user()

        with allure.step("Mock repository to return a user for a given email"):
            self.repo.get_user_by_email.return_value = user

        with allure.step("Attempt to retrieve user by email"):
            result = await self.service.get_user_by_email(user.email)

        with allure.step("Verify retrieved user is correct"):
            self.assertEqual(result, user)

    @allure.story("Get User by Email")
    @allure.title("Test get user by email failure")
    async def test_get_user_by_email_failure(self) -> None:

        with allure.step("Mock repository to simulate no user found with the given email"):
            self.repo.get_user_by_email.return_value = None

        with allure.step("Attempt to retrieve user by a non-existent email"):
            result = await self.service.get_user_by_email(self.objectsMother.get_user().email)

        with allure.step("Verify user retrieval failed"):
            self.assertEqual(result, None)

    @allure.story("Get All Users")
    @allure.title("Test get all users success")
    async def test_get_all_users_success(self) -> None:

        with allure.step("Mock repository to return a non-empty list of users"):
            self.repo.get_all_users.return_value = not None

        with allure.step("Attempt to get all users"):
            result = await self.service.get_all_users()

        with allure.step("Verify get all users was successful"):
            self.assertEqual(result, True)

    @allure.story("Get All Users")
    @allure.title("Test get all users failure")
    async def test_get_all_users_failure(self) -> None:

        with allure.step("Mock repository to simulate failure or empty list of users"):
            self.repo.get_all_users.return_value = self.objectsMother.get_error()

        with allure.step("Attempt to get all users"):
            result = await self.service.get_all_users()

        with allure.step("Verify get all users failed"):
            self.assertEqual(result, self.objectsMother.get_error())


if __name__ == '__main__':
    unittest.main()
