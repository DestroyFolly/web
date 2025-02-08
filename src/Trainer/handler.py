from fastapi import APIRouter, HTTPException, status, Response
from pydantic import BaseModel
from typing import List
from sql.bd import SessionMaker
from sql.bd import TrainerDB
from Trainer.dto import TrainerResponse
from Trainer.repository import TrainerRepository
from Trainer.service import TrainerService

trainer_router = APIRouter()

class Trainer(BaseModel):
    id: int
    first_name: str
    surname: str
    number: str  # Изменено на str для соответствия коду

class TrainerHandler:
    def __init__(self) -> None:
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = TrainerDB
        self.repo = TrainerRepository(self.table, self.session_maker)
        self.service = TrainerService(self.repo)

    @staticmethod
    @trainer_router.get("/trainers", response_model=List[Trainer])
    async def trainers_page():
        try:
            print('Fetching trainers')
            result = TrainerHandler().get_service().gettrainers()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Тренеры не найдены"
                )
            trainers = [
                Trainer(
                    id=trainer.id,
                    first_name=trainer.first_name,
                    surname=trainer.surname,
                    number=str(trainer.number)
                )
                for trainer in result
            ]
            return trainers
        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Превышено время ожидания ответа от сервера"
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Произошла внутренняя ошибка сервера: {str(e)}"
            )

    @staticmethod
    @trainer_router.get("/trainers/{id}", response_model=Trainer)
    async def get_trainer_by_id(id: int):
        # try:
            trainer = TrainerHandler().get_service().gettrainerbyid(id)
            if trainer == '-':
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Тренер не найден"
                )
            return Trainer(
                id=trainer.id,
                first_name=trainer.first_name,
                surname=trainer.surname,
                number=str(trainer.number)
            )
        # except TimeoutError:
        #     raise HTTPException(
        #         status_code=status.HTTP_408_REQUEST_TIMEOUT,
        #         detail="Превышено время ожидания ответа от сервера"
        #     )
        # except HTTPException as e:
        #     # Обработка исключений HTTPException должна возвращать оригинальный статус код
        #     raise e
        # except Exception as e:
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         detail=f"Произошла внутренняя ошибка сервера: {str(e)}"
        #     )

    def get_service(self) -> TrainerService:
        try:
            return self.service
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка инициализации TrainerService: {str(e)}"
            )
