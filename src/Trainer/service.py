from __future__ import annotations

from Trainer.model import Trainer


class TrainerService:
    def __init__(self, repo) -> None:
        self.repo = repo


    def gettrainerbyid(self, id: int) -> Trainer | str:
        trainer = self.repo.gettrainerbyid(id)

        if trainer is not None:
            return trainer
        else:
            return "-"

    def gettrainerbyphone(self, phone: int) -> Trainer | str:
        trainer = self.repo.gettrainerbyphone(phone)

        if trainer is not None:
            return trainer
        else:
            return "-"


    def gettrainers(self) -> Trainer | str:
        trainers = self.repo.gettrainers()

        if trainers is not None:
            return trainers
        else:
            return "Нет тренеров"

    def deletetrainerbyid(self, id: int) -> Trainer | str | None:
        trainer = self.repo.delete(id)
        if trainer is None:
            return "-"

        return trainer

    def addtrainer(self, first_name: str, surname: str, gender: str, number: int, position_id: int, gym_id: int) -> None | str | Trainer:
        trainer = self.repo.addtrainer(first_name, surname, gender,  number, position_id, gym_id)
        if trainer is not None:
            return trainer
        else:
            return "-"
