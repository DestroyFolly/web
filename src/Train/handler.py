from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from typing import List, Optional

from sql.bd import SessionMaker
from sql.bd import TrainDB
from Train.dto import TrainRequest
from Train.dto import TrainResponse
from Train.repository import TrainRepository
from Train.service import TrainService
from Trainer.service import TrainerService
from Trainer.handler import TrainerHandler
from Gym.service import GymService
from Gym.handler import GymHandler

train_router = APIRouter()


# Модели для запросов и ответов
class Train(BaseModel):
    id: int
    title: str
    dates: str
    times: str
    trainer_id: int
    gym_id: int


class TrainInput(BaseModel):
    title: str
    dates: str
    times: str
    trainer_id: int
    gym_id: int


class TrainHandler:
    def __init__(self) -> None:
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = TrainDB
        self.repo = TrainRepository(self.table, self.session_maker)
        self.service = TrainService(self.repo)

    @staticmethod
    @train_router.post("/trains", status_code=status.HTTP_201_CREATED)
    async def addtrain_post(train: TrainInput):
        try:
            trainer = TrainerHandler().get_service().gettrainerbyid(train.trainer_id)
            if trainer == '-':
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Trainer not found")

            gym = GymHandler().get_service().getgymbyid(
                train.gym_id)
            if gym == "Тренировка не найдена":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Gym not found")

            result = TrainHandler().get_service().addtrain(
                train.title, train.times, train.dates, train.trainer_id, train.gym_id
            )
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить тренировку",
                )
        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Превышено время ожидания добавления тренировки",
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка добавления тренировки: {str(e)}",
            )
        return Train(
            id=result.id,
            title=result.title,
            dates=result.dates,
            times=result.times,
            trainer_id=result.trainer_id,
            gym_id=result.gym_id,
        )

    @staticmethod
    @train_router.get("/trains/{id}", response_model=Train)
    async def get_train_by_id(id: int):
        try:
            result = TrainHandler().get_service().gettrainbyid(id)
            if result == '-':
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Тренировка не найдена"
                )
            return Train(
                id=result.id,
                title=result.title,
                dates=result.dates,
                times=result.times,
                trainer_id=result.trainer_id,
                gym_id=result.gym_id,
            )
        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Превышено время ожидания ответа",
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Внутренняя ошибка: {str(e)}",
            )

    @staticmethod
    @train_router.get("/trains", response_model=List[Train])
    async def get_list_of_trains():
        try:
            result = TrainHandler().get_service().getlistoftrains()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Тренировки не найдены"
                )
            trains = [
                Train(
                    id=train.id,
                    title=train.title,
                    dates=train.dates,
                    times=train.times,
                    trainer_id=train.trainer_id,
                    gym_id=train.gym_id,
                )
                for train in result
            ]
            return trains
        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Превышено время ожидания ответа",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Внутренняя ошибка: {str(e)}",
            )

    @staticmethod
    @train_router.put("/trains/{id}", response_model=Train)
    async def change_train(id: int, train: TrainInput):
        try:
            result = TrainHandler().get_service().changetrain(
                id, train.title, train.times, train.dates, train.trainer_id, train.gym_id
            )
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось изменить тренировку",
                )
            if result == "-":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Тренировка не найдена",
                )
        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Превышено время ожидания изменения тренировки",
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка изменения тренировки: {str(e)}",
            )
        return Train(
            id=result.id,
            title=result.title,
            dates=result.dates,
            times=result.times,
            trainer_id=result.trainer_id,
            gym_id=result.gym_id,
        )


    def get_service(self) -> TrainService:
        try:
            return self.service
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка инициализации TrainService: {str(e)}",
            )
    def get_trainer_service(self) -> TrainerService:
        try:
            return self.service
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка инициализации TrainerService: {str(e)}",
            )
    def get_gym_service(self) -> GymService:
        try:
            return self.service
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка инициализации GymService: {str(e)}",
            )
