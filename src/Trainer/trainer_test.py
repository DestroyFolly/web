from __future__ import annotations

import unittest
from unittest.mock import MagicMock
from pydantic import BaseModel


class Trainer(BaseModel):
    id: int | None = None
    first_name: str | None = None
    surname: str | None = None
    gender: str | None = None
    number: int | None = None
    position_id: int
    gym_id: int


class TrainerBuilder:
    def __init__(self):
        self.id = 1
        self.gender = "m"
        self.first_name = "Iliyasov"
        self.surname = "Khamzat"
        self.number = 9775374232
        self.position_id = 1
        self.gym_id = 2

    def with_id(self, id):
        self.id = id
        return self

    def build(self) -> Trainer:
        return Trainer(
            id=self.id,
            gender=self.gender,
            first_name=self.first_name,
            surname=self.surname,
            number=self.number,
            position_id=self.position_id,
            gym_id=self.gym_id,
        )


class FakeTrainerRepository:
    def __init__(self):
        self.data = {}

    def gettrainerbyid(self, trainer_id):
        if trainer_id not in self.data:
            raise ValueError("Trainer not found")
        return self.data[trainer_id]

    def gettrainers(self):
        trainers = list(self.data.values())
        if not trainers:
            raise ValueError("No trainers found")
        return trainers

    def addtrainer(self, trainer):
        self.data[trainer.id] = trainer


class TrainerService:
    def __init__(self, repo):
        self.repo = repo

    def gettrainerbyid(self, trainer_id):
        return self.repo.gettrainerbyid(trainer_id)

    def gettrainers(self):
        return self.repo.gettrainers()


class TestTrainerServiceWithMock(unittest.TestCase):
    def setUp(self):
        self.repo = MagicMock()
        self.service = TrainerService(self.repo)

    def test_getbyid_success(self):
        trainer = TrainerBuilder().with_id(1).build()
        self.repo.gettrainerbyid.return_value = trainer

        result = self.service.gettrainerbyid(1)

        self.repo.gettrainerbyid.assert_called_once_with(1)
        self.assertEqual(result, trainer)

    def test_getbyid_failure(self):
        self.repo.gettrainerbyid.side_effect = ValueError("Trainer not found")

        with self.assertRaises(ValueError) as context:
            self.service.gettrainerbyid(-1)
        self.assertEqual(str(context.exception), "Trainer not found")

    def test_gettrainers_success(self):
        trainer = TrainerBuilder().build()
        self.repo.gettrainers.return_value = [trainer]

        result = self.service.gettrainers()

        self.repo.gettrainers.assert_called_once()
        self.assertEqual(result, [trainer])

    def test_gettrainers_failure(self):
        self.repo.gettrainers.side_effect = ValueError("No trainers found")

        with self.assertRaises(ValueError) as context:
            self.service.gettrainers()
        self.assertEqual(str(context.exception), "No trainers found")


class TestTrainerServiceWithoutMock(unittest.TestCase):
    def setUp(self):
        self.repo = FakeTrainerRepository()
        self.service = TrainerService(self.repo)

    def test_getbyid_success(self):
        trainer = TrainerBuilder().with_id(1).build()
        self.repo.addtrainer(trainer)

        result = self.service.gettrainerbyid(1)

        self.assertEqual(result, trainer)

    def test_getbyid_failure(self):
        with self.assertRaises(ValueError):
            self.service.gettrainerbyid(-1)

    def test_gettrainers_success(self):
        trainer = TrainerBuilder().build()
        self.repo.addtrainer(trainer)

        result = self.service.gettrainers()

        self.assertEqual(result, [trainer])

    def test_gettrainers_failure(self):
        with self.assertRaises(ValueError):
            self.service.gettrainers()


if __name__ == "__main__":
    unittest.main()
