from __future__ import annotations

from User.model import User
from User.repository import UserRepository
from conn.tu_repository import TURepository
from Train.repository import TrainRepository


class UserService:
    def __init__(self, repo: UserRepository, turepo: TURepository, trainrepo: TrainRepository) -> None:
        self.repo = repo
        self.tu_repo = turepo
        self.train_repo = trainrepo


    def login(self, password: str, email: str) -> User | str:
        user = self.repo.getuserbyemail(email)
        print(user)
        if user is None:
            return "User not found"
        elif user.password != password:
            return "User password is incorect"
        else:
            return user

    def register(self, phone: int, email: str, name: str, surname: str, password: str, role: str, gender: str) -> User | int | str:

        user = self.repo.getuserbyemail(email)

        if user is not None:
            return "User already registered"


        new_user = self.repo.create(phone, email, name, surname, password, role, gender)
        if new_user is None:
            return 'Fail to create user'
        return new_user

    def getuserbyid(self, id: int) -> User | str:
        user = self.repo.getuserbyid(id)

        if user is None:
            return "Not found"

        return user

    def getusertrains(self, id: int) -> User | str:
        user = self.tu_repo.gettrainsid(id)
        if user is None:
            return "Not found"
        res = []
        for i in range (len(user)):
            train = self.train_repo.gettrainbyid(user[i].train_id)
            res.append(train)
        print(res)

        return res

    def deleteuserbyid(self, id: int) -> User | int | str:
        user = self.repo.delete(id)
        if user is None:
            return "-"

        return user

    def getuserbyemail(self, email: str) -> User | str:
        user = self.repo.getuserbyemail(email)

        if user is None:
            return "Not found"

        return user

    def addconn(self, user_id: int, train_id :int) -> User | int | str:
        conn = self.tu_repo.addconn(user_id, train_id)
        if conn is None:
            return 'Fail'
        return conn
