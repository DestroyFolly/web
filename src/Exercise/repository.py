from __future__ import annotations

from sql.bd import SessionMaker


class ExerciseRepository:
    def __init__(self, table: type, session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker

    def getexbyid(self, id):
        with self.session as session:
            return session.query(self.table).get(id)

    def getexbyname(self, name):
        with self.session as session:
            return session.query(self.table).get(name)

    def getlistofexercises(self, difficulty):
        with self.session as session:
            return session.query(self.table).filter_by(difficulty=difficulty).all()
