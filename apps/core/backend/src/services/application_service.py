import logging

from datetime import datetime

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
        self._logger = logging.getLogger(__name__)

    def get_all_by_user(self, user: User) -> List[Application]:
        return self._repository.get_all_by_user(user)

    def get_by_name(self, name: str, user: User) -> Application:
        application = self._repository.get_by_name(name)
        if application is None:
            raise ValueError(f"Not found or Not permission access application{name}")

        return application

    def create(self, data: dict, user: User) -> Application:
        try:
            application = Application(**data)
            self.generate_name(application)
            application.created_at = datetime.now()
            application.created_by = user.id
            application.updated_at = datetime.now()
            application.updated_by = user.id
            application.active = True
            application.add_user(user)
            self._repository.create(application)
            self._dbcontext.commit()
            self._logger.info(f"{user.email} created new application {application.name}")

            return application
        except Exception as e:
            self._logger.error(f"Error ocurred on create new application {str(e)}")
            self._dbcontext.rollback()

            raise e

    def update(self, data: dict, name: str, user: User):
        application: Application = self._repository.get_by_name(name, user)
        if application is None:
            raise ValueError(f"{name} not found, or you doens't have permission")
        application.real_name = data["real_name"]
        application.model = data["model"]
        application.description = data["description"]
        application.details = data["details"]
        application.updated_at = datetime.now()
        application.updated_by = user.id
        self._dbcontext.commit()

        self._logger.info(f"{user.email} updated application {application.name}")

        return application

    def activate(self, name: str, user: User):
        application = self._repository.get_by_name(name, user)
        if application is None:
            raise ValueError(f"{name} not found, or you doens't have permission")
        application.updated_at = datetime.now()
        application.updated_by = user.id
        application.active = True
        self._dbcontext.commit()

        self._logger.info(f"{user.email} activate application {application.name}")

        return application

    def inactive(self, name: str, user: User):
        application = self._repository.get_by_name(name, user)
        if application is None:
            raise ValueError(f"{name} not found, or you doens't have permission")
        application.updated_at = datetime.now()
        application.updated_by = user.id
        application.active = False
        self._dbcontext.commit()

        self._logger.info(f"{user.email} inactive application {application.name}")

        return application

    def delete(self, name: str, user: User):
        return self.inactive(name, user)

    def generate_name(self, application: Application) -> str:
        """
        Genarate unique name for Application
        """
        application.generate_name()
        if self._repository.name_exists(application.name):
            return self.generate_name(f"{application.real_name}_{randint(1, 100)}")
