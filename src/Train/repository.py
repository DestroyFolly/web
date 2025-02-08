from __future__ import annotations

from sql.bd import SessionMaker
from Train.model import Train


class TrainRepository:
    def __init__(self, table: type, session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker

    def gettrainbyid(self, id: int) -> None:
        with self.session as session:
            return session.query(self.table).get(id)

    def getlistoftrains(self) -> None:
        with self.session as session:
            return session.query(self.table).all()

    def addtrain(self, title: str, times: str, dates: str, trainer_id: int, gym_id: int) -> None | Train:
        with self.session as session:
            new_train = Train(id=max([train.id for train in session.query(self.table).all()]) + 1, title = title, times = times, dates= dates, trainer_id = trainer_id, gym_id = gym_id)
            session.add(self.table(new_train))
            session.commit()
            return new_train

    def delete(self, id: int) -> Train | int | None:
        with self.session as session:
            trainer = session.query(self.table).get(id)
            print(trainer)
            if trainer is not None:
                session.delete(trainer)
                session.commit()
                return '+'
            return '-'

    def changetrain(self, train_id:int, title: str, times: str, dates: str, trainer_id: int, gym_id: int) -> None | Train:
        with self.session as session:
            train = session.query(self.table).filter_by(id = train_id).first()
            if train:
                train.title = title
                train.times = times
                train.dates = dates
                train.trainer_id = trainer_id
                train.gym_id = gym_id
                session.commit()
            return train


