from __future__ import annotations

import json

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body, Response, Depends
from marketplace.BD.ORM import UserDB
from marketplace.BD.session import SessionMaker
from marketplace.Logger.loger import logger
from marketplace.User.dto import UserRequest
from marketplace.User.dto import UserResponse, UsersResponse
from marketplace.User.repository import UserRepository
from marketplace.User.service import UserService
from marketplace.Connections.my_jwt1 import JwtHandler
from marketplace.Errors.dto_error import Error
import yaml
from fastapi.responses import HTMLResponse, RedirectResponse
user_page = APIRouter()


class UserHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml", port=5001)
        self.table = UserDB
        self.repo = UserRepository(self.table, self.session_maker)
        self.service = UserService(self.repo, self.logger)

    @staticmethod
    @user_page.get("/api/v2/swagger.yaml", response_class=JSONResponse)
    async def get_swagger():
        with open("swagger.yaml", "r") as file:
            content = yaml.safe_load(file)
        return JSONResponse(content=content)

    @staticmethod
    @user_page.get("/api/v2/", include_in_schema=False)
    async def swagger_ui():
        return get_swagger_ui_html(
            openapi_url="/api/v2/swagger.yaml",
            title="Marketplace API",
        )

    @staticmethod
    @user_page.get("/admin/")
    async def open_admin_page():
        return RedirectResponse(url="http://127.0.0.1:54699")

    @staticmethod
    @user_page.post("/api/v2/users/login")
    async def login(data=Body()) -> Response:
        result = await JwtHandler.authenticate_user(data)
        if isinstance(result, Error):
            return result.response()
        return Response(json.dumps(result), 200, media_type='application/json')

    @staticmethod
    @user_page.post("/api/v2/users/register")
    async def register(data=Body()) -> Response:
        req = UserRequest(data)
        result = await UserHandler().get_service().register(req.get_user())
        return UserResponse(result).response()

    @staticmethod
    @user_page.delete('/api/v2/users/{user_id}')
    @JwtHandler.check_auth_roles()
    async def delete_user_by_id(user_id: int, user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await UserHandler().get_service().delete(user_id)
        return UserResponse(result).response()

    @staticmethod
    @user_page.patch('/api/v2/users/{user_id}')
    @JwtHandler.check_auth_roles()
    async def update_user_by_id(user_id: int, data=Body(), user=Depends(JwtHandler.get_current_user)) -> Response:
        req = UserRequest(data)
        req.user_id = user_id
        result = await UserHandler().get_service().update(req.get_user())
        return UserResponse(result).response()

    @staticmethod
    @user_page.get('/api/v2/users/{user_id}')
    @JwtHandler.check_auth_roles()
    async def get_user_by_id(user_id: int | str, user=Depends(JwtHandler.get_current_user)) -> Response:
        if isinstance(user_id, int):
            result = await UserHandler().get_service().get_user_by_id(user_id)
            return UserResponse(result).response()
        else:
            result = await UserHandler().get_service().get_user_by_email(user_id)
            return UserResponse(result).response()

    @staticmethod
    @user_page.get('/api/v2/users')
    @JwtHandler.check_auth_roles(roles=["admin"])
    async def get_all_users(user=Depends(JwtHandler.get_current_user)) -> Response:
        result = await UserHandler().get_service().get_all_users()
        return UsersResponse(result).response()

    def get_service(self) -> UserService:
        return self.service
