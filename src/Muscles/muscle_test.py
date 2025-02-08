from __future__ import annotations

import sys
import os
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Muscles.model import Muscle
from Muscles.service import MuscleService

class MuscleBuilder:
    def __init__(self):
        self.id = 1
        self.title = "Legs"
        self.difficulty = "Hard"

    def with_id(self, id):
        self.id = id
        return self

    def with_title(self, title):
        self.title = title
        return self

    def with_difficulty(self, difficulty):
        self.difficulty = difficulty
        return self

    def build(self) -> Muscle:
        return Muscle(id=self.id, title=self.title, difficulty=self.difficulty)

class TestMuscleServiceWithMock(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = MagicMock()
        self.service = MuscleService(self.repo)

    def test_getbyid_success(self) -> None:
        muscle = MuscleBuilder().with_id(1).build()
        self.repo.getmusclebyid.return_value = muscle

        result = self.service.getmusclebyid(1)

        self.repo.getmusclebyid.assert_called_once_with(1)
        self.assertEqual(result, muscle)

    def test_getbyid_failure(self) -> None:
        self.repo.getmusclebyid.side_effect = ValueError("Muscle not found")

        with self.assertRaises(ValueError) as context:
            self.service.getmusclebyid(-1)
        self.assertEqual(str(context.exception), "Muscle not found")

    def test_getlistofmuscles_success(self) -> None:
        muscle = MuscleBuilder().with_difficulty("Hard").build()
        self.repo.getlistofmuscles.return_value = [muscle]

        result = self.service.getlistofmuscles("Hard")

        self.repo.getlistofmuscles.assert_called_once_with("Hard")
        self.assertEqual(result, [muscle])

    def test_getlistofmuscles_failure(self) -> None:
        self.repo.getlistofmuscles.side_effect = ValueError("No muscles found")

        with self.assertRaises(ValueError) as context:
            self.service.getlistofmuscles("Soft")
        self.assertEqual(str(context.exception), "No muscles found")

class TestMuscleServiceWithoutMock(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = FakeMuscleRepository()
        self.service = MuscleService(self.repo)

    def test_getbyid_success(self) -> None:
        muscle = MuscleBuilder().with_id(1).build()
        self.repo.addmuscle(muscle)

        result = self.service.getmusclebyid(1)

        self.assertEqual(result, muscle)

    def test_getbyid_failure(self) -> None:

        with self.assertRaises(ValueError):
            self.service.getmusclebyid(-1)

    def test_getlistofmuscles_success(self) -> None:
        muscle = MuscleBuilder().with_difficulty("Hard").build()
        self.repo.addmuscle(muscle)

        result = self.service.getlistofmuscles("Hard")

        self.assertEqual(result, [muscle])

    def test_getlistofmuscles_failure(self) -> None:

        with self.assertRaises(ValueError):
            self.service.getlistofmuscles("Soft")

class FakeMuscleRepository:
    def __init__(self):
        self.data = {}

    def getmusclebyid(self, muscle_id):
        if muscle_id not in self.data:
            raise ValueError("Muscle not found")
        return self.data[muscle_id]

    def getlistofmuscles(self, difficulty):
        muscles = [muscle for muscle in self.data.values() if muscle.difficulty == difficulty]
        if not muscles:
            raise ValueError("No muscles found")
        return muscles

    def addmuscle(self, muscle):
        self.data[muscle.id] = muscle

if __name__ == '__main__':
    unittest.main()
