from __future__ import annotations

from flask import Blueprint
from flask import Response
from flask import request
from flask import redirect
from flask import render_template
from flask import make_response
from flask import url_for

from Exercise.dto import ExerciseResponse
from Exercise.repository import ExerciseRepository
from Exercise.service import ExerciseService
from sql.bd import ExerciseDB
from sql.bd import SessionMaker
from Muscles.handler import MuscleHandler


exercise_page = Blueprint("exercise_page", __name__)


class ExerciseHandler:
    def __init__(self) -> None:
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = ExerciseDB
        self.repo = ExerciseRepository(self.table, self.session_maker)
        self.service = ExerciseService(self.repo)

    @staticmethod
    @exercise_page.route('/exercise_page', methods=['GET'])
    def exercise_page_get() -> Response:
        return render_template('exercise_page.html')

    @staticmethod
    @exercise_page.route('/exercise_page', methods=['POST'])
    def exercise_page_post() -> Response:
        difficulty = request.form['diff']
        result = []
        exs = ExerciseHandler().get_service().listexercise(difficulty)
        res = ExerciseResponse(exs)
        # print(res.data[0])
        # exercises = (res.data[0].get_json())
        # print (exercises['title'])
        # print(len(exercises))
        for i in range(len(exs)):
            exercise = (res.data[i].get_json())
            muscles_id = exercise['muscles_id']
            muscles = MuscleHandler().get_service().getmusclebyid(muscles_id)
            print(muscles)
            str = f"{exercise['title']}; Difficulty {exercise['difficulty']}; {muscles}"
            result.append(str)

        return render_template('exercise_list.html', data = result)

    @staticmethod
    @exercise_page.route('/getexercisebyid/<id>', methods=['GET'])
    def get_exercise_by_id(id: int) -> Response:
        result = ExerciseHandler().get_service().getexbyid(id)
        return ExerciseResponse(result).get_response()

    @staticmethod
    @exercise_page.route('/getexercisebyname/<title>', methods=['GET'])
    def get_exercise_by_name(title: str) -> Response:
        result = ExerciseHandler().get_service().getexbyname(title)
        return ExerciseResponse(result).get_response()

    @staticmethod
    @exercise_page.route('/listexercise/<difficulty>', methods=['GET'])
    def get_list_of_exercises(difficulty: int) -> Response:
        result = ExerciseHandler().get_service().listexercise(difficulty)
        return ExerciseResponse(result).get_response()

    def get_service(self) -> ExerciseService:
        return self.service
