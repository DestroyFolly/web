from __future__ import annotations

from Muscles.model import Muscle


class MuscleService:
    def __init__(self, repo) -> None:
        self.repo = repo

    def getmusclebyid(self, id: int) -> str | Muscle:
        muscle = self.repo.getmusclebyid(id)

        if muscle is not None:
            return muscle
        else:
            return "Тренировка не найдена"

    def getlistofmuscles(self, difficulty: int) -> str | Muscle:
        muscles = self.repo.getlistofmuscles(difficulty)

        if muscles is not None:
            return muscles
        else:
            return "Нет таких группы мышц"
