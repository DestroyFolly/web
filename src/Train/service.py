from __future__ import annotations

from Train.model import Train


class TrainService:
    def __init__(self, repo) -> None:
        self.repo = repo


    def gettrainbyid(self, id) -> str | Train:
        train = self.repo.gettrainbyid(id)

        if train is not None:
            return train
        else:
            return "-"

    def addtrain(self, title: str, time: str, date: str, trainer_id: int, gym_id: int) -> None | str | Train:
        train = self.repo.addtrain(title, time, date, trainer_id, gym_id)
        if train is not None:
            return train
        else:
            return "-"

    def getlistoftrains(self):
        trains = self.repo.getlistoftrains()

        if trains is not None:
            return trains
        else:
            return "-"

    def deletetrain(self, id: int) -> Train | str | None:
        mes = self.repo.delete(id)
        return mes

    def changetrain(self, id: int, title: str, times: str, dates: str, trainer_id: int, gym_id: int) -> str | Train:
        train =  self.repo.changetrain(id, title, times, dates, trainer_id, gym_id)
        if not train:
            return '-'
        else:
            return train


