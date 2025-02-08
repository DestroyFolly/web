from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from typing import List, Optional

from sql.bd import SessionMaker
from sql.bd import GymDB
from Gym.repository import GymRepository
from Gym.service import GymService

gym_router = APIRouter()


# Модели для запросов и ответов
class Gym(BaseModel):
    id: int
    adress: str
    work_hours: str
    phone: int

class GymInput(BaseModel):
    adress: str
    work_hours: str
    phone: int

class GymHandler:
    def __init__(self) -> None:
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = GymDB
        self.repo = GymRepository(self.table, self.session_maker)
        self.service = GymService(self.repo)

    @staticmethod
    @gym_router.get("/gym/{id}", response_model=Gym)
    async def get_gym_by_id(id: int):
        try:
            result = GymHandler().get_service().getgymbyid(id)
            if result == "Тренировка не найдена":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Зал не найден"
                )
            return Gym(
                id=result.id,
                adress=result.adress,
                work_hours=result.work_hours,
                phone=result.phone,
            )
        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Превышено время ожидания запроса",
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера",
            )

    @staticmethod
    @gym_router.get("/gym", response_model=List[Gym])
    async def gyms_page():
        try:
            result = GymHandler().get_service().getlistofgyms()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Залы не найдены",
                )
            gyms = [
                Gym(
                    id=gym.id,
                    adress=gym.adress,
                    work_hours=gym.work_hours,
                    phone=gym.phone,
                )
                for gym in result
            ]
            return gyms
        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Превышено время ожидания запроса",
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера",
            )

    @staticmethod
    @gym_router.delete("/gym/{id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_gym(id: int):
        try:
            res = GymHandler().get_service().getgymbyid(id)
            if res == "Тренировка не найдена":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Зал не найден"
                )

            result = GymHandler().get_service().deletegym(id)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Зал не найден",
                )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Некорректный запрос",
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера",
            )
        return {"message": "Зал удален"}

    @staticmethod
    @gym_router.post("/gym", status_code=status.HTTP_201_CREATED)
    async def addgym_post(gym: GymInput):
        try:

            result = GymHandler().get_service().addgym(
                gym.adress, gym.work_hours, gym.phone
            )
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось добавить зал",
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
        return Gym(
            id=result.id,
            adress=result.adress,
            work_hours=result.time,
            phone=result.phone,
        )

    # @staticmethod
    # @gym_router.patch("/gym/{id}", response_model=Gym)
    # async def patch_gym(id: int, gym: GymInput):
    #     try:
    #         result = GymHandler().get_service().getgymbyid(id)
    #         if result == "Тренировка не найдена":
    #             raise HTTPException(
    #                 status_code=status.HTTP_404_NOT_FOUND,
    #                 detail="Зал не найден",
    #             )
    #         gym_res = GymHandler().get_service().patchgym(
    #             id, gym.adress, gym.work_hours, gym.phone,
    #         )
    #         if not gym_res:
    #             raise HTTPException(
    #                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                 detail="Не удалось изменить тренировку",
    #             )
    #         if gym_res:
    #             return gym_res
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail=f"Ошибка изменения зала: {str(e)}",
    #         )

    def get_service(self) -> GymService:
        try:
            return self.service
        except Exception as e:
            print(f"Error initializing GymService: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка инициализации сервиса",
            )
