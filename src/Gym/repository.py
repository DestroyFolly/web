from __future__ import annotations

from sql.bd import SessionMaker
from Gym.model import Gym


class GymRepository:
    def __init__(self, table: type, session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker

    def getgymbyid(self, id: int) -> None:
        with self.session as session:
            return session.query(self.table).get(id)

    def getlistofgyms(self) -> None:
        with self.session as session:
            return session.query(self.table).all()

    def delete(self, id: int) -> Gym | int | None:
        with self.session as session:
            gym = session.query(self.table).get(id)
            print(gym)
            if gym is not None:
                session.delete(gym)
                session.commit()
                return '+'
            return '-'
    def changegymadress(self, gym_id: int, adress: str) -> None | Gym:
        with self.session as session:
            gym = session.query(self.table).filter_by(id = gym_id).first()
            if gym:
                gym.adress = adress
                session.commit()
            return gym
    def changegymhours(self, gym_id: int, work_hours: str) -> None | Gym:
        with self.session as session:
            gym = session.query(self.table).filter_by(id = gym_id).first()
            if gym:
                gym.work_hours = work_hours
                session.commit()
            return gym

    def addgym(self, adress: str, work_hours: str, phone: int) -> None | str | Gym:
        with self.session as session:
            new_gym = Gym(id=max([gym.id for gym in session.query(self.table).all()]) + 1, adress = adress, phone = phone, work_hours = "9:00 - 18:00")
            new_gym.time = work_hours
            session.add(self.table(new_gym))
            session.commit()
            return new_gym

    def changegymphone(self, gym_id: int, phone: int) -> None | Gym:
        with self.session as session:
            gym = session.query(self.table).filter_by(id = gym_id).first()
            if gym:
                gym.phone = phone
                session.commit()
            return gym


