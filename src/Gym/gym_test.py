from __future__ import annotations

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Gym.model import Gym

import unittest
from unittest.mock import MagicMock, patch
from Gym.service import GymService

class GymBuilder:
    def __init__(self):
        self.id = 1
        self.adress = "1000"
        self.time = "10:00"
        self.phone = 111

    def with_id(self, id):
        self.id = id
        return self

    def with_adress(self, adress):
        self.adress = adress
        return self

    def build(self) -> Gym:
        return Gym(id=self.id, adress=self.adress, time=self.time, phone=self.phone)

class TestGymServiceWithMock(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = MagicMock()
        self.service = GymService(self.repo)

    def test_getbyid_success(self) -> None:
        gym = GymBuilder().with_id(1).build()
        self.repo.getgymbyid.return_value = gym

        result = self.service.getgymbyid(1)

        self.repo.getgymbyid.assert_called_once_with(1)
        self.assertEqual(result, gym)

    def test_getbyid_failure(self) -> None:
        self.repo.getgymbyid.side_effect = ValueError("Gym not found")

        with self.assertRaises(ValueError) as context:
            self.service.getgymbyid(-1)
        self.assertEqual(str(context.exception), "Gym not found")

    def test_list_success(self) -> None:
        gym = GymBuilder().build()
        self.repo.getlistofgyms.return_value = [gym]

        result = self.service.getlistofgyms()

        self.repo.getlistofgyms.assert_called_once_with()
        self.assertEqual(result, [gym])

    def test_list_failure(self) -> None:
        self.repo.getlistofgyms.side_effect = ValueError("No gyms found")

        with self.assertRaises(ValueError) as context:
            self.service.getlistofgyms()
        self.assertEqual(str(context.exception), "No gyms found")

class TestGymServiceWithoutMock(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = FakeGymRepository()
        self.service = GymService(self.repo)

    def test_getbyid_success(self) -> None:
        gym = GymBuilder().with_id(1).build()
        self.repo.addgym(gym)

        result = self.service.getgymbyid(1)

        self.assertEqual(result, gym)

    def test_getbyid_failure(self) -> None:

        with self.assertRaises(ValueError):
            self.service.getgymbyid(-1)

    def test_list_success(self) -> None:
        gym = GymBuilder().build()
        self.repo.addgym(gym)

        result = self.service.getlistofgyms()

        self.assertEqual(result, [gym])

    def test_list_failure(self) -> None:

        with self.assertRaises(ValueError):
            self.service.getlistofgyms()

class FakeGymRepository:
    def __init__(self):
        self.data = {}

    def getgymbyid(self, gym_id):
        if gym_id not in self.data:
            raise ValueError("Gym not found")
        return self.data[gym_id]

    def getlistofgyms(self):
        gyms = list(self.data.values())
        if not gyms:
            raise ValueError("No gyms found")
        return gyms

    def addgym(self, gym):
        self.data[gym.id] = gym

if __name__ == '__main__':
    unittest.main()
