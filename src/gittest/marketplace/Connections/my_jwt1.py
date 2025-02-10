from fastapi import APIRouter, Body, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from marketplace.BD.ORM import UserDB
from marketplace.BD.session import SessionMaker
from marketplace.Logger.loger import logger
from marketplace.User.repository import UserRepository
from marketplace.User.service import UserService
import jwt
from datetime import datetime, timedelta
from marketplace.Errors.dto_error import Error
from functools import wraps


jwt_page = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)


def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"exp": expiration})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except jwt.PyJWTError:
        return None


class JwtHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml", port=5001)
        self.table = UserDB
        self.repo = UserRepository(self.table, self.session_maker)
        self.service = UserService(self.repo, self.logger)

    @staticmethod
    @jwt_page.post("token")
    async def authenticate_user(data=Body()):
        user = await JwtHandler().get_service().login(data.get("email"), data.get("password"))
        if not isinstance(user, UserDB):
            return Error("User not found", 404)
        jwt_token = create_jwt_token({"email": data.get("email"), "password": data.get("password")})
        return {"access_token": jwt_token}

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)):
        decoded_data = verify_jwt_token(token)
        if not decoded_data:
            return Error("Unauthorized", 401)
        user = await JwtHandler().get_service().login(decoded_data["email"], decoded_data["password"])
        if not isinstance(user, UserDB):
            return Error("User not found", 404)
        return user

    @staticmethod
    def check_auth_roles(roles=None):
        def decorator(func):
            @wraps(func)
            async def wrapper(user, *args, **kwargs):
                try:
                    if isinstance(user, UserDB):
                        if roles and user.role not in roles:
                            return Error("Forbidden", 403).response()
                        return await func(*args, **kwargs)
                    return user.response()
                except Exception as e:
                    return Error("Internal Server Error", 500).response()
            return wrapper
        return decorator

    def get_service(self) -> UserService:
        return self.service
