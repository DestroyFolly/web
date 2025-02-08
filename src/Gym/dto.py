from __future__ import annotations

from typing import Any

from flask import Response
from flask import jsonify
from flask import make_response

from Gym.model import Gym


class GymRequest:
    def __init__(self, gym_data: Any) -> None:
        self.id = gym_data.get("id")
        self.adress = gym_data.get("adress")
        self.phone = gym_data.get("phone")
        self.work_hours = gym_data.get("work_hours")

    def get_gym(self) -> Gym:
        return Gym(id=self.id, adress=self.adress, phone=self.phone, work_hours=self.work_hours)


class GymResponse:
    def __init__(self, data: Gym | None) -> None:
        print (data[0])
        dict_data = []
        if not data:
            error = 1
            dict_data = {"error": 'Empty Gym'}
        else:
            for i in range(len(data)):
                new_data = {"address": str(data[i].adress), "phone": str(data[i].phone),
                         "work_hours": str(data[i].work_hours)}
                dict_data.append(new_data)
            error = 0


        self.data = jsonify(dict_data)
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.data, self.error)


class GymsResponse:
    def __init__(self, data: list[Gym] | None) -> None:
        dict_data = [{"": ""}] * 0
        if not data:
            for elem in data:
                dict_data.append({"id": str(elem.id), "address": str(elem.adress), "phone": str(elem.phone),
                                  "work_hours": str(elem.work_hours)})
            error = 0
        else:
            error = 1
            dict_data = {"error": 'Empty Gym'}

        self.data = jsonify(dict_data[0]) if dict_data[0].get("error") else jsonify(dict_data)
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.json_data, self.error)