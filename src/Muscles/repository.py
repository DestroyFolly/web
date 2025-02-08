from __future__ import annotations

from sql.bd import SessionMaker


class MusclesRepository:
    def __init__(self, table: type, session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker

    def getmusclebyid(self, id: int) -> None:
        with self.session as session:
            return session.query(self.table).get(id)

    def getlistofmuscles(self, mg: str) -> None:
        with self.session as session:
            return session.query(self.table).filter_by(mgroup=mg).all()

