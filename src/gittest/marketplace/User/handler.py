from __future__ import annotations

from flask import Blueprint
from flask import Response
from flask import make_response
from flask import request
from flask import url_for

from marketplace.BD.ORM import UserDB
from marketplace.BD.session import SessionMaker
from marketplace.Logger.loger import logger
from marketplace.User.dto import CODE_SUCCESS
from marketplace.User.dto import UserRequest
from marketplace.User.dto import UserResponse
from marketplace.User.dto import UsersResponse
from marketplace.User.repository import UserRepository
from marketplace.User.service import UserService
from marketplace.View.View import View


user_page = Blueprint("user_page", __name__)


class UserHandler:
    def __init__(self) -> None:
        self.logger = logger
        self.session_maker = SessionMaker("pyproject.toml")
        self.table = UserDB
        self.repo = UserRepository(self.table, self.session_maker)
        self.service = UserService(self.repo, self.logger)

    @staticmethod
    @user_page.route('/', methods=['GET'])
    async def main_page() -> Response | str:
        return make_response(View.render_template("main.html"), CODE_SUCCESS)

    @staticmethod
    @user_page.route('/exit/<user_id>', methods=['GET'])
    async def exit(user_id: int) -> Response | str:
        return View.redirect(url_for('user_page.main_page'))

    @staticmethod
    @user_page.route('/route/<name_page>/<user_id>', methods=['GET'])
    async def router(name_page: str, user_id: int) -> Response | str:
        role = await UserHandler().get_service().get_user_role(user_id)
        return make_response(View.render_template(f"{role}_page_{name_page}.html", user_id=user_id), CODE_SUCCESS)

    @staticmethod
    @user_page.route('/route_rules/<name_page>/<user_id>', methods=['GET'])
    async def router_new(name_page: str, user_id: int) -> Response | str:
        return make_response(View.render_template(f"user_page_{name_page}.html", user_id=user_id), CODE_SUCCESS)

    @staticmethod
    @user_page.route('/login', methods=['GET', 'POST'])
    async def login() -> Response | str:
        if request.method == "POST":
            req = UserRequest(request.form)
            result = await UserHandler().get_service().login(req.email, req.password)
            res = UserResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
            return View.redirect('/legacy' + url_for('user_page.router', name_page="main", user_id=res.data.get("user_id")))
        return make_response(View.render_template("login.html"), CODE_SUCCESS)

    @staticmethod
    @user_page.route('/register', methods=['GET', 'POST'])
    async def register() -> Response | str:
        if request.method == "POST":
            req = UserRequest(request.form)
            result = await UserHandler().get_service().register(req.get_user())
            res = UserResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
            return View.redirect(url_for('user_page.router', name_page="main", user_id=res.data.get("user_id")))
        return make_response(View.render_template("register.html"), CODE_SUCCESS)

    @staticmethod
    @user_page.route('/create_user', methods=['GET', 'POST'])
    async def create_user() -> Response | str:
        if request.method == "POST":
            req = UserRequest(request.form)
            result = await UserHandler().get_service().register(req.get_user())
            res = UserResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
            return View.redirect(url_for('user_page.register'))
        return make_response(View.render_template("create_user.html"), CODE_SUCCESS)

    @staticmethod
    @user_page.route('/delete_user/<user_id>', methods=['GET'])
    async def delete_user_by_id(user_id: int) -> Response:
        result = await UserHandler().get_service().delete(user_id)
        res = UserResponse(result)
        if res.check_is_error():
            return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template(url_for("user_page.main_page")), CODE_SUCCESS)

    @staticmethod
    @user_page.route('/delete_user', methods=['GET', 'POST'])
    async def delete_user_by_id_admin() -> Response:
        if request.method == "POST":
            req = UserRequest(request.form)
            result = await UserHandler().get_service().delete(req.user_id)
            res = UserResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("user_delete.html"), CODE_SUCCESS)

    @staticmethod
    @user_page.route('/update_user/<user_id>', methods=['GET', 'POST'])
    async def update_user_by_id(user_id: int) -> Response:
        if request.method == "POST":
            req = UserRequest(request.form)
            req.user_id = user_id
            result = await UserHandler().get_service().update(req.get_user())
            res = UserResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("user_update.html", user_id=user_id), CODE_SUCCESS)

    @staticmethod
    @user_page.route('/update_user', methods=['GET', 'POST'])
    async def update_user_by_id_admin() -> Response:
        if request.method == "POST":
            req = UserRequest(request.form)
            result = await UserHandler().get_service().update(req.get_user())
            res = UserResponse(result)
            if res.check_is_error():
                return make_response(View.render_template("error.html", error=res.get_description_error()), res.error)
        return make_response(View.render_template("user_update_admin.html"), CODE_SUCCESS)

    @staticmethod
    @user_page.route('/get_user_by_id/<user_id>', methods=['GET'])
    async def get_user_by_id(user_id: int) -> Response:
        result = await UserHandler().get_service().get_user_by_id(user_id)
        res = UserResponse(result)
        return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)

    @staticmethod
    @user_page.route('/get_user_by_id', methods=['GET', 'POST'])
    async def get_user_by_id_admin() -> Response:
        if request.method == "POST":
            req = UserRequest(request.form)
            return View.redirect(url_for("user_page.get_user_by_id", user_id=req.user_id))
        return make_response(View.render_template("get_user_by_id.html"), CODE_SUCCESS)

    @staticmethod
    @user_page.route('/get_user_by_email', methods=['GET', 'POST'])
    async def get_user_by_email() -> Response:
        if request.method == "POST":
            req = UserRequest(request.form)
            result = await UserHandler().get_service().get_user_by_email(req.email)
            res = UserResponse(result)
            return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)
        return make_response(View.render_template("get_user_by_email.html"), CODE_SUCCESS)

    @staticmethod
    @user_page.route('/get_all_users', methods=['GET'])
    async def get_all_users() -> list[Response] | Response:
        result = await UserHandler().get_service().get_all_users()
        res = UsersResponse(result)
        return make_response(View.render_template("info.html", info=res.get_string_info()), res.error)

    def get_service(self) -> UserService:
        return self.service

