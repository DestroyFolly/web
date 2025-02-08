from __future__ import annotations

import unittest
from unittest.mock import MagicMock
from pydantic import BaseModel


class User(BaseModel):
    id: int
    phone: int
    email: str
    first_name: str
    surname: str
    password: str
    role: str
    gender: str


class UserBuilder:
    def __init__(self):
        self.id = 1
        self.phone = 100
        self.email = "user@email.com"
        self.first_name = "Pavel"
        self.surname = "Maslukov"
        self.password = "password"
        self.role = "Admin"
        self.gender = "male"

    def with_id(self, id):
        self.id = id
        return self

    def with_email(self, email):
        self.email = email
        return self

    def build(self) -> User:
        return User(
            id=self.id,
            phone=self.phone,
            email=self.email,
            first_name=self.first_name,
            surname=self.surname,
            password=self.password,
            role=self.role,
            gender=self.gender,
        )


class FakeUserRepository:
    def __init__(self):
        self.data = {}

    def getuserbyemail(self, email):
        if email not in self.data:
            return None
        return self.data[email]

    def create(self, user: User):
        if user.email in self.data:
            raise ValueError("User already exists")
        self.data[user.email] = user
        return user


class UserService:
    def __init__(self, repo: FakeUserRepository):
        self.repo = repo

    def login(self, password: str, email: str) -> str:
        user = self.repo.getuserbyemail(email)
        if not user:
            return "User not found"
        if user.password != password:
            return "Invalid password"
        return "Login successful"

    def register(self, phone: int, email: str, first_name: str, surname: str, password: str, role: str, gender: str) -> str:
        if self.repo.getuserbyemail(email):
            return "User already exists"
        user = User(
            id=len(self.repo.data) + 1,
            phone=phone,
            email=email,
            first_name=first_name,
            surname=surname,
            password=password,
            role=role,
            gender=gender,
        )
        self.repo.create(user)
        return "User registered successfully"


class TestUserServiceWithMock(unittest.TestCase):
    def setUp(self):
        self.repo = MagicMock()
        self.service = UserService(self.repo)

    def test_login_user_not_found(self):
        self.repo.getuserbyemail.return_value = None

        result = self.service.login("password", "user@email.com")

        self.repo.getuserbyemail.assert_called_once_with("user@email.com")
        self.assertEqual(result, "User not found")

    def test_login_invalid_password(self):
        user = UserBuilder().build()
        self.repo.getuserbyemail.return_value = user

        result = self.service.login("wrongpassword", "user@email.com")

        self.repo.getuserbyemail.assert_called_once_with("user@email.com")
        self.assertEqual(result, "Invalid password")

    def test_register_user_already_exists(self):
        user = UserBuilder().build()
        self.repo.getuserbyemail.return_value = user

        result = self.service.register(100, "user@email.com", "Pavel", "Maslukov", "password", "Admin", "male")

        self.repo.getuserbyemail.assert_called_once_with("user@email.com")
        self.assertEqual(result, "User already exists")


class TestUserServiceWithoutMock(unittest.TestCase):
    def setUp(self):
        self.repo = FakeUserRepository()
        self.service = UserService(self.repo)

    def test_register_success(self):
        result = self.service.register(100, "newuser@email.com", "John", "Doe", "password", "User", "male")

        self.assertEqual(result, "User registered successfully")
        self.assertIn("newuser@email.com", self.repo.data)

    def test_login_success(self):
        user = UserBuilder().build()
        self.repo.create(user)

        result = self.service.login("password", "user@email.com")

        self.assertEqual(result, "Login successful")

    def test_login_failure(self):
        result = self.service.login("password", "nonexistent@email.com")

        self.assertEqual(result, "User not found")


if __name__ == "__main__":
    unittest.main()
