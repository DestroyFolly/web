from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

from sql.bd import SessionMaker
from sql.bd import MusclesDB
from Muscles.repository import MusclesRepository
from Muscles.service import MuscleService

muscle_router = APIRouter()


# Модели для запросов и ответов
class Muscle(BaseModel):
    id: int
    title: str
    mgroup: str
    function: Optional[str]


class MuscleHandler:
    def __init__(self) -> None:
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = MusclesDB
        self.repo = MusclesRepository(self.table, self.session_maker)
        self.service = MuscleService(self.repo)

    @staticmethod
    @muscle_router.get("/muscles/{id}", response_model=Muscle, status_code=status.HTTP_200_OK)
    async def get_muscle_by_id(id: int):
        try:
            result = MuscleHandler().get_service().getmusclebyid(id)
            if result == "Тренировка не найдена":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Мышца не найдена"
                )
            return Muscle(
                id=result.id,
                title=result.title,
                mgroup=result.mgroup,
                function=result.function
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Произошла внутренняя ошибка сервера: {str(e)}"
            )



    def get_service(self) -> MuscleService:
        return self.service
