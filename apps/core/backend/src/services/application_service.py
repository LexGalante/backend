import re
from textwrap import shorten
from random import randint
from typing import List

from models.application import Application
from models.user import User
from repositories.application_repository import ApplicationRepository
from resources.dbcontext import DbContext


class ApplicationService():
    def __init__(self, dbcontext: DbContext):
        self._dbcontext = dbcontext
        self._repository: ApplicationRepository = ApplicationRepository(dbcontext)

    def get_all_by_user(self, user: User) -> List[Application]:
        return self._repository.get_all_by_user(user)

    def get_by_name(self, name: str, user: User) -> Application:
        application = self._repository.get_by_name(name)
        if application is None:
            raise ValueError(f"Not found or Not permission access application{name}")

        return application

    def create(self, data: dict, user: User) -> Application:
        application = Application(**data)
        application.name = self.generate_name(application.real_name)
        self._repository.create(application)
        self._dbcontext.commit()

        return application

    def update(self, data: dict, name: str):
        pass

    def delete(self, name: str):
        pass

    def generate_name(self, real_name: str) -> str:
        name = real_name.lower().replace(" ", "_")
        name = re.sub(r"[^a-zA-Z0-9]", "", name)
        name = shorten(name, width=30, placeholder="_")
        if self._repository.name_exists(name):
            return self.generate_name(f"{real_name}_{randint(1, 100)}")

        return name
