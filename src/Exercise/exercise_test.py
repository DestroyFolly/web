from __future__ import annotations

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Добавление пути поиска

from Exercise.model import Exercise

import unittest
from unittest.mock import MagicMock, patch
from Exercise.service import ExerciseService


class ExerciseBuilder:
    def __init__(self):
        self.id = 1
        self.name = "leg press"
        self.group = "legs"
        self.difficulty = "medium"

    def with_id(self, id):
        self.id = id
        return self

    def with_name(self, name):
        self.name = name
        return self

    def build(self) -> Exercise:
        return Exercise(id=self.id, name=self.name, group=self.group, difficulty=self.difficulty)


class TestExerciseServiceWithMock(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = MagicMock()
        self.service = ExerciseService(self.repo)

    def test_getbyid_success(self) -> None:

        exercise = ExerciseBuilder().with_id(1).build()
        self.repo.getexbyid.return_value = exercise


        result = self.service.getexbyid(1)


        self.repo.getexbyid.assert_called_once_with(1)
        self.assertEqual(result, exercise)

    def test_getbyid_failure(self) -> None:

        self.repo.getexbyid.side_effect = ValueError("Exercise not found")


        with self.assertRaises(ValueError) as context:
            self.service.getexbyid(-1)
        self.assertEqual(str(context.exception), "Exercise not found")

    def test_getbyname_success(self) -> None:

        exercise = ExerciseBuilder().with_name("leg press").build()
        self.repo.getexbyname.return_value = exercise


        result = self.service.getexbyname("leg press")


        self.repo.getexbyname.assert_called_once_with("leg press")
        self.assertEqual(result, exercise)

    def test_getbyname_failure(self) -> None:

        self.repo.getexbyname.side_effect = ValueError("Exercise not found")


        with self.assertRaises(ValueError) as context:
            self.service.getexbyname("rest in bed")
        self.assertEqual(str(context.exception), "Exercise not found")


class TestExerciseServiceWithoutMock(unittest.TestCase):

    def setUp(self) -> None:

        self.repo = FakeExerciseRepository()
        self.service = ExerciseService(self.repo)

    def test_getbyid_success(self) -> None:

        exercise = ExerciseBuilder().with_id(1).build()
        self.repo.addexercise(exercise)

        result = self.service.getexbyid(1)

        self.assertEqual(result, exercise)

    def test_getbyid_failure(self) -> None:



        with self.assertRaises(ValueError):
            self.service.getexbyid(-1)

    def test_getbyname_success(self) -> None:

        exercise = ExerciseBuilder().with_name("leg press").build()
        self.repo.addexercise(exercise)


        result = self.service.getexbyname("leg press")


        self.assertEqual(result, exercise)

    def test_getbyname_failure(self) -> None:


        with self.assertRaises(ValueError):
            self.service.getexbyname("rest in bed")

class FakeExerciseRepository:
    def __init__(self):
        self.data = {}

    def getexbyid(self, ex_id):
        if ex_id not in self.data:
            raise ValueError("Exercise not found")
        return self.data[ex_id]

    def getexbyname(self, name):
        for exercise in self.data.values():
            if exercise.name == name:
                return exercise
        raise ValueError("Exercise not found")

    def addexercise(self, exercise):
        self.data[exercise.id] = exercise

if __name__ == '__main__':
    unittest.main()

