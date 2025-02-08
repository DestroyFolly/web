from __future__ import annotations

from Gym.model import Gym


class GymService:
    def __init__(self, repo) -> None:
        self.repo = repo

    def getgymbyid(self, id) -> Gym | str:
        gym = self.repo.getgymbyid(id)

        if gym is not None:
            return gym
        else:
            return "Тренировка не найдена"

    def getlistofgyms(self) -> Gym | str:
        gyms = self.repo.getlistofgyms()

        if gyms is not None:
            return gyms
        else:
            return "Подходящий зал не найдем"

    def deletegym(self, id: int) -> Gym | str | None:
        mes = self.repo.delete(id)
        return mes

    def addgym(self, adress: str, work_hours: str, phone: int) -> None | str | Gym:
        gym = self.repo.addgym(adress, work_hours, phone)
        if gym is not None:
            return gym
        else:
            return None

    def patchgym(self, id: int, adress: str, work_hours: str, phone: int) -> Gym | str | None:
        if adress != '':
            gym = self.repo.changegymadress(id, adress)
        if work_hours != '':
            gym = self.repo.changegymhours(id, work_hours)
        if phone != 0:
            gym = self.repo.changegymphone(id, phone)

        return gym
