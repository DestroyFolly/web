from __future__ import annotations

from Position.model import Position
from sql.bd import SessionMaker


class PositionRepository:
    def __init__(self, table: type, session_maker: SessionMaker) -> None:
        self.table = table
        self.session = session_maker

    def getpositionbyid(self, id: int) -> Position | None:
        with self.session as session:
            return session.query(self.table).get(id)

    def getlistofpositions(self, exp: int) -> None:
        with self.session as session:
            return session.query(self.table).filter(self.table.experience <= exp).all()


