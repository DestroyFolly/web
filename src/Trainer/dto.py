from __future__ import annotations

from typing import Any

from flask import Response
from flask import jsonify
from flask import make_response

from Trainer.model import Trainer


class TrainerRequest:
    def __init__(self, trainer_data: Any) -> None:
        self.id = trainer_data.get("id")
        self.gender = trainer_data.get("gender")
        self.position_id = trainer_data.get("position_id")
        self.gym_id = trainer_data.get("gym_id")
        self.first_name = trainer_data.get("first_name")
        self.surname = trainer_data.get("surname")
        self.number = trainer_data.get("number")
        self.role = trainer_data.get("role")

    def get_trainer(self) -> Trainer:
        return Trainer(id=self.id, gender=self.gender, position_id=self.position_id, gym_id=self.gym_id,
                    first_name=self.first_name, surname=self.surname, number=self.number, role=self.role)


class TrainerResponse:
    def __init__(self, data: Trainer | None) -> None:
        print (data[0])
        dict_data = []
        if not data:
            error = 1
            dict_data = {"error": 'Empty Gym'}
        else:
            for i in range(len(data)):
                new_data = {"id": str(data[i].id), "gender": str(data[i].gender), "position_id": str(data[i].position_id),
                         "gym_id": str(data[i].gym_id), "first_name": str(data[i].first_name), "surname": str(data[i].surname),
                         "number": str(data[i].number)}
                dict_data.append(new_data)
            error = 0


        self.data = jsonify(dict_data)
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.data, self.error)


class TrainersResponse:
    def __init__(self, data: list[Trainer] | None) -> None:
        dict_data = [{"": ""}] * 0
        if not data:
            for elem in data:
                dict_data.append({"id": str(elem.id), "gender": str(elem.gender), "position_id": str(elem.position_id),
                                  "gym_id": str(elem.gym_id), "first_name": str(elem.first_name),
                                  "surname": str(elem.surname), "number": str(elem.number)})
            error = 0
        else:
            error = 1
            dict_data = {"error": 'Empty Trainer'}

        self.json_data = jsonify(dict_data[0]) if dict_data[0].get("error") else jsonify(dict_data)
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.json_data, self.error)