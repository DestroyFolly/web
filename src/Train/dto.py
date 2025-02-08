from __future__ import annotations

from typing import Any

from flask import Response
from flask import jsonify
from flask import make_response

from Train.model import Train


class TrainRequest:
    def __init__(self, train_data: Any) -> None:
        self.id = train_data.get("id")
        self.title = train_data.get("title")
        self.dates = train_data.get("dates")
        self.times = train_data.get("times")
        self.trainer_id = train_data.get("trainer_id")
        self.gym_id = train_data.get("gym_id")

    def get_train(self) -> Train:
        return Train(id=self.id, title=self.title, dates=self.dates, times=self.times,
                    trainer_id=self.trainer_id, gym_id=self.gym_id)


class TrainResponse:
    def __init__(self, data: Train | None) -> None:
        if not data or data == '-':
            error = 1
            dict_data = {"error": 'Empty Train'}
        elif data == '+':
            error = 0
            dict_data = {"info": 'DELETED'}
        else:
            print(data)
            dict_data = {"id": str(data.id), "title": str(data.title), "dates": str(data.dates),
                         "times": str(data.times), "trainer_id": str(data.trainer_id), "gym_id": str(data.gym_id)}
            error = 0


        self.json_data = jsonify(dict_data)
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.json_data, self.error)


class TrainsResponse:
    def __init__(self, data: list[Train] | None) -> None:
        dict_data = [{"": ""}] * 0
        if not data:
            for elem in data:
                dict_data.append({"id": str(elem.id), "title": str(elem.title), "dates": str(elem.dates),
                                  "times": str(elem.times), "trainer_id": str(elem.trainer_id),
                                  "gym_id": str(elem.gym_id)})
            error = 0
        else:
            error = 1
            dict_data = {"error": 'Empty Train'}

        self.json_data = jsonify(dict_data[0]) if dict_data[0].get("error") else jsonify(dict_data)
        self.error = error

    def get_response(self) -> Response:
        return make_response(self.json_data, self.error)