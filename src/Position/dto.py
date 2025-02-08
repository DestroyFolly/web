from __future__ import annotations

from typing import Any

from flask import Response
from flask import jsonify
from flask import make_response

from Position.model import Position


class PositionRequest:
    def __init__(self, position_data: Any) -> None:
        self.id = position_data.get("id")
        self.title = position_data.get("title")
        self.experience = position_data.get("experience")
        self.function = position_data.get("function")

    def get_position(self) -> Position:
        return Position(id=self.id, title=self.title, experience=self.experience, function=self.function)


class PositionResponse:
    def __init__(self, data: Position | None) -> None:
        if not data:
            error = 1
            dict_data = {"error": 'Empty Position'}
        else:
            dict_data = {"id": str(data.id), "title": str(data.title), "experience": str(data.experience),
                         "function": str(data.function)}
            error = 0


        self.json_data = jsonify(dict_data)
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.json_data, self.error)


class PositionsResponse:
    def __init__(self, data: list[Position] | None) -> None:
        dict_data = [{"": ""}] * 0
        if not data:
            for elem in data:
                dict_data.append({"id": str(elem.id), "title": str(elem.title), "experience": str(elem.experience),
                                  "function": str(elem.function)})
            error = 0
        else:
            error = 1
            dict_data = {"error": 'Empty Position'}

        self.json_data = jsonify(dict_data[0]) if dict_data[0].get("error") else jsonify(dict_data)
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.json_data, self.error)