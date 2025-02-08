from __future__ import annotations

from sql.bd import SessionMaker
from conn.tu_model import TU


class TURepository:
    def __init__(self, table: type, session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker

    # def create(self, phone: int, email: str, name: str, surname: str, password: str, role: str,
    #            gender: str) -> User | None:
    #     with self.session as session:
    #         new_user = User(id=max([user.id for user in session.query(self.table).all()]) + 1, phone=phone, email=email,
    #                         name=name, surname=surname, password=password, role=role, gender=gender)
    #         session.add(self.table(new_user))
    #         session.commit()
    #         return new_user

    def gettrainsid(self, id: int) -> TU | list | None:
        with self.session as session:
            return session.query(self.table).filter_by(users_id=id).all()

    def addconn(self,user_id: int, train_id: int) -> TU | None:
        with self.session as session:
            new_conn = TU(id=max([tu.id for tu in session.query(self.table).all()]) + 1, users_id=user_id, train_id=train_id)
            session.add(self.table(new_conn))
            session.commit()
            return new_conn