from __future__ import annotations

from typing import Any

import sqlalchemy

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


Base: Any = sqlalchemy.orm.declarative_base()


class UserDB(Base):
    def __init__(self, user: UserDB):
        self.id = user.id
        self.phone = user.phone
        self.email = user.email
        self.first_name = user.first_name
        self.surname = user.surname
        self.password = user.password
        self.role = user.role
        self.gender = user.gender

    def update(self, new_data: UserDB) -> None:
        self.first_name = new_data.name if new_data.name else self.name
        self.email = new_data.email if new_data.email else self.email
        self.password = new_data.password if new_data.password else self.password
        self.surname = new_data.surname if new_data.surname else self.surname
        self.phone = new_data.phone if new_data.phone else self.phone

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    phone = Column(Integer, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # def __eq__(self, other: Any) -> bool:
    #     return self.id == other.id

    def __repr__(self) -> str:
        return f"{self.id}; {self.first_name}; {self.surname}; {self.email}; {self.password}; {self.role}; {self.gender}; {self.phone}."


class ExerciseDB(Base):
    def __init__(self, exercise: ExerciseDB):
        self.id = exercise.id
        self.title = exercise.name
        self.difficulty = exercise.difficulty
        self.muscles_id = exercise.muscles_id

    def update(self, new_data: ExerciseDB) -> None:
        self.title = new_data.title if new_data.title else self.title
        self.difficulty = new_data.difficulty if new_data.difficulty else self.difficulty

    __tablename__ = 'exercise'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False)
    muscles_id = Column(Integer, ForeignKey('muscles.id', ondelete='CASCADE'))

    # def __eq__(self, other: Any) -> bool:
    #     return self.id == other.id

    def __repr__(self) -> str:
        return f"{self.id}; {self.title}; {self.difficulty}; {self.muscles_id}"


class GymDB(Base):
    def __init__(self, gym: GymDB):
        self.id = gym.id
        self.adress = gym.adress
        self.work_hours = gym.time
        self.phone = gym.phone

    def update(self, new_data: GymDB) -> None:
        self.work_hours = new_data.work_hours if new_data.work_hours else self.time
        self.phone = new_data.phone if new_data.phone else self.phone

    __tablename__ = 'gym'

    id = Column(Integer, primary_key=True)
    adress = Column(String, nullable=True)
    work_hours = Column(String, nullable=True)
    phone = Column(Integer, nullable=True)

    # def __eq__(self, other: Any) -> bool:
    #     return self.id == other.id

    def __repr__(self) -> str:
        return f"{self.id}; {self.adress}; {self.phone}; {self.work_hours}"


class MusclesDB(Base):
    def __init__(self, muscle: MusclesDB):
        self.id = muscle.id
        self.title = muscle.title
        self.mgroup = muscle.mgroup
        self.function = muscle.function

    def update(self, new_data: MusclesDB) -> None:
        self.title = new_data.title if new_data.title else self.title
        self.mgroup = new_data.mgroup if new_data.mgroup else self.mgroup

    __tablename__ = 'muscles'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    mgroup = Column(String, nullable=False)
    function = Column(String, nullable=False)

    # def __eq__(self, other: Any) -> bool:
    #     return self.id == other.id

    def __repr__(self) -> str:
        return f" Titile of muscles group: {self.title}; function: {self.function}."


class PositionDB(Base):
    def __init__(self, position: PositionDB):
        self.id = position.id
        self.title = position.title
        self.function = position.function
        self.experience = position.experience

    def update(self, new_data: PositionDB) -> None:
        self.title = new_data.title if new_data.title else self.title

    __tablename__ = 'position'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    function = Column(String, nullable=False)
    experience = Column(Integer, nullable=False)

    def __eq__(self, other: Any) -> bool:
        return self.id == other.id

    def __repr__(self) -> str:
        return f"Position_id={self.id}; title={self.title}; function={self.function}; experience={self.experience}."


class TrainDB(Base):
    def __init__(self, train: TrainDB):
        self.id = train.id
        self.title = train.title
        self.times = train.times
        self.dates = train.dates
        self.trainer_id = train.trainer_id
        self.gym_id = train.gym_id

    def update(self, new_data: TrainDB) -> None:
        self.title = new_data.title if new_data.title else self.title
        self.times = new_data.times if new_data.times else self.times
        self.dates = new_data.dates if new_data.dates else self.dates

    __tablename__ = 'train'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    times = Column(String, nullable=False)
    dates = Column(Integer, nullable=False)
    trainer_id = Column(Integer, ForeignKey('trainer.id', ondelete='CASCADE'))
    gym_id = Column(Integer, ForeignKey('gym.id', ondelete='CASCADE'))

    # def __eq__(self, other: Any) -> bool:
    #     return self.id == other.id

    def __repr__(self) -> str:
        return f"{self.id}; {self.title}; {self.times}; {self.dates}; {self.trainer_id}, {self.gym_id}."


class TrainerDB(Base):
    def __init__(self, trainer: TrainerDB):
        self.id = trainer.id
        self.first_name = trainer.first_name
        self.surname = trainer.surname
        self.gender = trainer.gender
        self.number = trainer.number
        self.position_id = trainer.position_id
        self.gym_id = trainer.gym_id

    def update(self, new_data: TrainerDB) -> None:
        self.number = new_data.number if new_data.number else self.number
        self.first_name = new_data.first_name if new_data.first_name else self.name
        self.surname = new_data.surname if new_data.surname else self.surname

    __tablename__ = 'trainer'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    position_id = Column(Integer, ForeignKey('position.id', ondelete='CASCADE'))
    gym_id = Column(Integer, ForeignKey('gym.id', ondelete='CASCADE'))

    # def __eq__(self, other: Any) -> bool:
    #     return self.id == other.id

    def __repr__(self) -> str:
        return f"{self.id}; {self.first_name}; {self.surname}; {self.number}; {self.gender}; {self.position_id}; {self.gym_id}."

class teDB(Base):
    def __init__(self, te: teDB):
        self.id = te.id
        self.trainer_id = te.trainer_id
        self.exercise_id = te.exercise_id


    def update(self, new_data: teDB) -> None:
        self.train_id = new_data.train_id
        self.exercise_id = new_data.exercise_id

    __tablename__ = 'te'

    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey('train.id', ondelete='CASCADE'))
    exercise_id = Column(Integer, ForeignKey('exercise.id', ondelete='CASCADE'))



    def __repr__(self) -> str:
        return f"{self.train_id}; {self.exercise_id}"


class tuDB(Base):
    def __init__(self, tu: tuDB):
        self.id = tu.id
        self.train_id = tu.train_id
        self.users_id = tu.users_id

    def update(self, new_data: teDB) -> None:
        self.train_id = new_data.train_id
        self.users_id = new_data.users_id

    __tablename__ = 'tu_conn'

    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey('train.id', ondelete='CASCADE'))
    users_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))


    def __repr__(self) -> str:
        return f"{self.train_id}; {self.users_id}"

class SessionMaker:
    def __init__(self, config_name: str) -> None:
        self.engine = create_engine(SessionMaker.get_url(config_name), echo=False, pool_pre_ping=True, pool_timeout=10)

    def __enter__(self) -> Session:
        self.session = self.get_session()
        return self.session

    def __exit__(self, exc_type: type, exc_val: type, exc_tb: type) -> None:
        if self.session:
            self.session.close()
            self.session = None

    def get_url(self) -> str:
        return 'postgresql://postgres:2508@localhost:5432/coursework'

    def get_session(self) -> Session:
        return Session(self.engine)

