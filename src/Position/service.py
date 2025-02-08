from __future__ import annotations

from Position.model import Position


class PositionService:
    def __init__(self, repo) -> None:
        self.repo = repo

    def getpositionid(self, id) -> Position | str:
        position = self.repo.getpositionbyid(id)

        if position is not None:
            return position
        else:
            return "Должность не найдена"

    def getlistpositions(self, exp) -> Position | str:
        positions = self.repo.getlistofpositions(exp)

        if positions is not None:
            return positions
        else:
            return "-"
