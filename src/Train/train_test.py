from __future__ import annotations

import sys
import os
import unittest
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Train.model import Train
from Train.service import TrainService

class TrainBuilder:
    def __init__(self):
        self.id = 1
        self.title = "legs"
        self.time = "10:00"
        self.date = "10.04.24"
        self.trainer_id = 1
        self.gym_id = 2

    def with_id(self, id):
        self.id = id
        return self

    def with_title(self, title):
        self.title = title
        return self

    def build(self) -> Train:
        return Train(id=self.id, title=self.title, time=self.time, date=self.date, trainer_id=self.trainer_id, gym_id=self.gym_id)

class TestTrainServiceWithMock(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = MagicMock()
        self.service = TrainService(self.repo)

    def test_getbyid_success(self) -> None:
        train = TrainBuilder().with_id(1).build()
        self.repo.gettrainbyid.return_value = train

        result = self.service.gettrainbyid(1)

        self.repo.gettrainbyid.assert_called_once_with(1)
        self.assertEqual(result, train)

    def test_getbyid_failure(self) -> None:
        self.repo.gettrainbyid.side_effect = ValueError("Train not found")

        with self.assertRaises(ValueError) as context:
            self.service.gettrainbyid(-1)
        self.assertEqual(str(context.exception), "Train not found")

    def test_getlistoftrains_success(self) -> None:
        train = TrainBuilder().with_id(1).build()
        self.repo.getlistoftrains.return_value = [train]

        result = self.service.getlistoftrains()

        self.repo.getlistoftrains.assert_called_once()
        self.assertEqual(result, [train])

    def test_getlistoftrains_failure(self) -> None:
        self.repo.getlistoftrains.side_effect = ValueError("No trains found")

        with self.assertRaises(ValueError) as context:
            self.service.getlistoftrains()
        self.assertEqual(str(context.exception), "No trains found")

class TestTrainServiceWithoutMock(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = FakeTrainRepository()
        self.service = TrainService(self.repo)

    def test_getbyid_success(self) -> None:
        train = TrainBuilder().with_id(1).build()
        self.repo.addtrain(train)

        result = self.service.gettrainbyid(1)

        self.assertEqual(result, train)

    def test_getbyid_failure(self) -> None:

        with self.assertRaises(ValueError):
            self.service.gettrainbyid(-1)

    def test_getlistoftrains_success(self) -> None:
        train = TrainBuilder().build()
        self.repo.addtrain(train)

        result = self.service.getlistoftrains()

        self.assertEqual(result, [train])

    def test_getlistoftrains_failure(self) -> None:

        with self.assertRaises(ValueError):
            self.service.getlistoftrains()

class FakeTrainRepository:
    def __init__(self):
        self.data = {}

    def gettrainbyid(self, train_id):
        if train_id not in self.data:
            raise ValueError("Train not found")
        return self.data[train_id]

    def getlistoftrains(self):
        trains = list(self.data.values())
        if not trains:
            raise ValueError("No trains found")
        return trains

    def addtrain(self, train):
        self.data[train.id] = train

if __name__ == '__main__':
    unittest.main()
