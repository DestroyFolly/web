from __future__ import annotations

from flask import Blueprint
from flask import Response

from Position.dto import PositionResponse
from Position.repository import PositionRepository
from Position.service import PositionService
from sql.bd import PositionDB
from sql.bd import SessionMaker


position_page = Blueprint("position_page", __name__)


class PositionHandler:
    def __init__(self) -> None:
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = PositionDB
        self.repo = PositionRepository(self.table, self.session_maker)
        self.service = PositionService(self.repo)

    @staticmethod
    @position_page.route('/getpositionid/<id>', methods=['GET'])
    def get_position_by_id(id: int) -> Response:
        result = PositionHandler().get_service().getpositionbyid(id)
        return PositionResponse(result).get_response()

    @staticmethod
    @position_page.route('/getlistpositions/<exp>', methods=['GET'])
    def get_list_of_positions(exp: int) -> Response:
        result = PositionHandler().get_service().getlistpositions(exp)
        return PositionResponse(result).get_response()


    def get_service(self) -> PositionService:
        return self.service


