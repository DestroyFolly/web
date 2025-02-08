from __future__ import annotations

from sql.bd import SessionMaker
from Trainer.model import Trainer


class TrainerRepository:
    def __init__(self, table: type, session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker

    def gettrainerbyid(self, id: int) -> None:
        with self.session as session:
            return session.query(self.table).get(id)

    def gettrainerbyphone(self, number: int) -> None:
        with self.session as session:
            return session.query(self.table).filter_by(number=number).first()

    def gettrainers(self) -> None:
        with self.session as session:
            return session.query(self.table).all()

    def delete(self, id: int) -> Trainer | int | None:
        with self.session as session:
            trainer = session.query(self.table).get(id)
            if trainer is not None:
                session.delete(trainer)
                session.commit()
            return id

    def addtrainer(self, first_name: str, surname: str, gender: str, number: int, position_id: int, gym_id: int) -> None | Trainer:
        with self.session as session:
            new_trainer = Trainer(id=max([trainer.id for trainer in session.query(self.table).all()]) + 1, first_name = first_name, surname = surname, gender = gender, number = number, position_id = position_id, gym_id = gym_id)
            session.add(self.table(new_trainer))
            session.commit()
            return new_trainer


