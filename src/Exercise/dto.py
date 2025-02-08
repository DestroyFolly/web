from __future__ import annotations

from typing import Any

from flask import Response
from flask import jsonify
from flask import make_response

from Exercise.model import Exercise


class ExerciseRequest:
    def __init__(self, exercise_data: Any) -> None:
        self.id = exercise_data.get("id")
        self.title = exercise_data.get("title")
        self.difficulty = exercise_data.get("difficulty")
        self.muscles_id = exercise_data.get("muscles_id")

    def get_exercise(self) -> Exercise:
        return Exercise(id=self.id, title=self.title, difficulty=self.difficulty,
                        muscles_id=self.muscles_id)


class ExerciseResponse:
    def __init__(self, data: Exercise | None) -> None:
        if not data:
            error = 1
            data_t = {"error": 'Empty Exercise'}
        else:
            data_t = []
            for i in range(len(data)):
                dict_data = {"id": data[i].id, "title": str(data[i].title), "difficulty": str(data[i].difficulty),
                         "muscles_id": data[i].muscles_id}
                temp = jsonify(dict_data)
                # print(temp)
                data_t.append(temp)
            error = 0

        # print(data_t)
        self.data = data_t
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.data, self.error)


class ExercisesResponse:
    def __init__(self, data: list[Exercise] | None) -> None:
        dict_data = [{"": ""}] * 0
        if not data:
            for elem in data:
                dict_data.append({"id": str(elem.id), "title": str(elem.title), "difficulty": str(elem.difficulty),
                                  "muscles_id": str(elem.muscles_id)})
            error = 0
        else:
            error = 1
            dict_data = {"error": 'Empty Exercise'}

        self.json_data = jsonify(dict_data[0]) if dict_data[0].get("error") else jsonify(dict_data)
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.json_data, self.error)
