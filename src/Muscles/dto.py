from __future__ import annotations

from typing import Any

from flask import Response
from flask import jsonify
from flask import make_response

from Muscles.model import Muscle


class MuscleRequest:
    def __init__(self, muscle_data: Any) -> None:
        self.id = muscle_data.get("id")
        self.title = muscle_data.get("title")
        self.mgroup = muscle_data.get("mgroup")
        self.function = muscle_data.get("function")

    def get_muscle(self) -> Muscle:
        return Muscle(id=self.id, title=self.title, mgroup=self.mgroup, function=self.function)


class MuscleResponse:
    def __init__(self, data: Muscle | None) -> None:
        if not data:
            error = 1
            dict_data = {"error": 'Empty Muscle'}
        else:
            dict_data = {"id": str(data.id), "title": str(data.title), "mgroup": str(data.mgroup),
                         "function": str(data.function)}
            error = 0


        self.json_data = jsonify(dict_data)
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.json_data, self.error)


class MusclesResponse:
    def __init__(self, data: list[Muscle] | None) -> None:
        dict_data = [{"": ""}] * 0
        if not data:
            for elem in data:
                dict_data.append({"id": str(elem.id), "title": str(elem.title), "mgroup": str(elem.mgroup),
                                  "function": str(elem.function)})
            error = 0
        else:
            error = 1
            dict_data = {"error": 'Empty Muscle'}

        self.json_data = jsonify(dict_data[0]) if dict_data[0].get("error") else jsonify(dict_data)
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.json_data, self.error)