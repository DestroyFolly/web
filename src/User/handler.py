from fastapi import APIRouter, HTTPException, status, Response, Query
from pydantic import BaseModel
from typing import Optional, List
from User.dto import UserResponse
import time
from Train.handler import TrainHandler
from User.service import UserService
from User.repository import UserRepository
from Train.repository import TrainRepository
from conn.tu_repository import TURepository
from sql.bd import SessionMaker, UserDB, TrainDB, tuDB

user_router = APIRouter()

# Модели для запросов и ответов
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    surname: str
    phone: int
    gender: str

class UserResponse(BaseModel):
    id: int
    role: str

class UserResponseFull(BaseModel):
    id: int
    email: str
    first_name: str
    surname: str
    phone: int

class TrainResponse(BaseModel):
    train_id: int
    title: str


class UserHandler:
    import time

    @staticmethod
    @user_router.post("/login", response_model=UserResponse,
                      status_code=status.HTTP_200_OK)
    async def login(data: LoginRequest):
        # Засекаем время начала выполнения
        start_time = time.time()

        try:
            # Проверяем, если отсутствуют данные в запросе
            if not data.email or not data.password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email and password are required")

            # Вызываем сервис для входа
            result = UserHandler.get_service().login(data.password,
                                                     data.email)

            # Проверяем, если пользователь не найден
            if result == "User not found":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found")

            if result == "User password is incorrect":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Incorrect password")

            # Засекаем время окончания выполнения и проверяем, не превышает ли лимит
            elapsed_time = time.time() - start_time
            if elapsed_time > 5:  # Лимит времени выполнения: 5 секунд
                raise HTTPException(
                    status_code=status.HTTP_408_REQUEST_TIMEOUT,
                    detail="Request timed out")

            # Возвращаем успешный результат
            return UserResponse(
                id=result.id,
                role=result.role
            )

        except HTTPException as e:
            raise e
        except Exception as e:
            # Логируем исключение для отладки
            print(f"Error during login: {e}")
            # Универсальная ошибка 400 для любых других проблем
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An error occurred during login")

    @staticmethod
    @user_router.post("/register", response_model=UserResponse,
                      status_code=status.HTTP_201_CREATED)
    async def register(data: RegisterRequest):
        # Засекаем время начала выполнения
        start_time = time.time()

        try:
            # Проверка на наличие всех необходимых данных
            if not all([data.phone, data.email, data.first_name,
                        data.surname, data.password, data.gender]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="All fields are required")

            # Проверка формата email
            if "@" not in data.email or "." not in \
                    data.email.split("@")[-1]:
                print("Полученные данные:", data.email)
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid email format")

            # Проверка длины пароля
            if len(data.password) < 2:
                print("Полученные данные:", data.password)
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Password must be at least 2 character long")

            # Проверка номера телефона
            if  not str(data.phone).isdigit():
                print("Полученные данные:", data.phone)
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid phone number format")

            print("Регистрация началась")
            # Выполнение логики регистрации
            result = UserHandler.get_service().register(
                data.phone, data.email, data.first_name, data.surname,
                data.password, 'u', data.gender
            )
            print("Регистрация прошла", result )

            # Проверка, если пользователь уже зарегистрирован
            if result == "User already registered":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User already registered")

            # Засекаем время окончания выполнения и проверяем, не превышает ли лимит
            elapsed_time = time.time() - start_time
            if elapsed_time > 5:  # Лимит времени выполнения: 5 секунд
                raise HTTPException(
                    status_code=status.HTTP_408_REQUEST_TIMEOUT,
                    detail="Request timed out")

            # Возвращаем успешный результат
            return UserResponse(
                id=result.id,
                role=result.role
            )

        except HTTPException as e:
            raise e
        except Exception as e:
            # Логируем исключение для отладки
            print(f"Error during registration: {e}")
            # Универсальная ошибка 400 для любых других проблем
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An error occurred during registration")



    @staticmethod
    @user_router.get("/user/{id}/trains", response_model=List[TrainResponse], status_code=status.HTTP_200_OK)
    async def show_trains_for_user(id: int):
        result = UserHandler.get_service().getuserbyid(id)
        if result == "User not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Not found")

        train_handler = TrainHandler()
        result = train_handler.get_service().getlistoftrains()
        trains = [
            TrainResponse(
                train_id=train.id,
                title=train.title
            )
            for train in result
        ]
        return trains

    @staticmethod
    @user_router.post("/user/{id}/trains/{train_id}",
                      status_code=status.HTTP_200_OK)
    async def choose_train_post(id: int, train_id: int):
        # Создаем экземпляры TrainHandler и UserHandler
        train_handler = TrainHandler()

        # Получаем информацию о тренировке
        train = train_handler.get_service().gettrainbyid(train_id)
        if train == "-":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Train not found")

        user = UserHandler.get_service().getuserbyid(id)
        if user == "Not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        # Добавляем связь между пользователем и тренировкой
        service = UserHandler.get_service()  # Вызов статического метода
        service.addconn(id, train_id)

        # Получаем тренировки пользователя
        result = service.getusertrains(id)
        user_trains = [
            TrainResponse(
                train_id=train.id,
                title=train.title
            )
            for train in result
        ]
        return user_trains

    @staticmethod
    @user_router.get("/users/{id}", response_model=UserResponseFull)
    async def get_user_by_id(id: int):

            result = UserHandler().get_service().getuserbyid(id)
            if result == "Not found":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден",
                )
            return UserResponseFull(
                id=result.id,
                first_name=result.first_name,
                surname=result.surname,
                email=result.email,
                phone=result.phone,
            )


    @staticmethod
    def get_service() -> UserService:
        # Создаем зависимости для UserService
        session_maker = SessionMaker("pyproject.toml")
        user_repo = UserRepository(UserDB, session_maker)
        tu_repo = TURepository(tuDB, session_maker)  # для связей
        train_repo = TrainRepository(TrainDB, session_maker)
        return UserService(repo=user_repo, turepo=tu_repo, trainrepo=train_repo)
