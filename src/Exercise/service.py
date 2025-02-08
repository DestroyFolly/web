from __future__ import annotations

from Exercise.model import Exercise


class ExerciseService:
    def __init__(self, repo) -> None:
        self.repo = repo

    def getexbyid(self, id) -> str | Exercise:
        ex = self.repo.getexbyid(id)
        if ex is not None:
            return ex
        else:
            return "Упражнение не было найдено"

    def getexbyname(self, name) -> str | Exercise:
        ex = self.repo.getexbyname(name)
        if ex is not None:
            return ex
        else:
            return "Упражнение не было найдено"

    def listexercise(self, difficulty) -> None | Exercise | str:
        exs = self.repo.getlistofexercises(difficulty)
        if exs is not None:
            return exs
        else:
            return "-"
