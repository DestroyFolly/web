from __future__ import annotations

from sql.bd import SessionMaker
from User.model import User


class UserRepository:
    def __init__(self, table: type, session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker

    def create(self, phone: int, email: str, name: str, surname: str, password: str, role: str,
               gender: str) -> User | None:
        with self.session as session:
            new_user = User(id=max([user.id for user in session.query(self.table).all()]) + 1, phone=phone, email=email,
                            first_name=name, surname=surname, password=password, role=role, gender=gender)
            session.add(self.table(new_user))
            session.commit()
            return new_user

    def getuserbyid(self, id: int) -> User | None:
        with self.session as session:
            return session.query(self.table).get(id)

    def delete(self, id: int) -> User | int | None:
        with self.session as session:
            user = session.query(self.table).get(id)
            if user is not None:
                session.delete(user)
                session.commit()
            return id

    def getuserbyemail(self, email: str) -> User | None:
        with self.session as session:
            print(email)
            print(session.query(self.table).filter_by(email=email).first())
            return session.query(self.table).filter_by(email=email).first()



