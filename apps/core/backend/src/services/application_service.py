import logging

from datetime import datetime

from random import randint
from typing import List

from models.application import Application
from models.user import User
from repositories.application_repository import ApplicationRepository
from repositories.environment_repository import EnvironmentRepository
from resources.dbcontext import DbContext


class ApplicationService():
    def __init__(self, dbcontext: DbContext):
        self._dbcontext = dbcontext
        self._repository: ApplicationRepository = ApplicationRepository(dbcontext)
        self._environment_repository: EnvironmentRepository = EnvironmentRepository(dbcontext)
        self._logger = logging.getLogger(__name__)

    def get_all_by_user(self, user: User) -> List[Application]:
        return self._repository.get_all_by_user(user)

    def get_by_name(self, name: str, user: User) -> Application:
        application = self._repository.get_by_name(name, user)
        if application is None:
            raise ValueError(f"Not found or Not permission access application {name}")

        return application

    def create(self, data: dict, user: User) -> Application:
        try:
            application = Application()
            application.real_name = data["real_name"]
            application.model = data["model"]
            application.description = data["description"]
            application.details = data["details"] if "details" in data.keys() else None
            self.generate_name(application)
            application.created_at = datetime.now()
            application.created_by = user.id
            application.updated_at = datetime.now()
            application.updated_by = user.id
            application.activate = True
            application.add_user(user.id)
            self._repository.create(application)
            self._dbcontext.commit()
            self._logger.info(
                f"{user.email} created new application {application.name}")

            return application
        except Exception as e:
            self._logger.error(f"Error ocurred on create new application {str(e)}")
            self._dbcontext.rollback()

            raise e

    def update(self, data: dict, name: str, user: User):
        application = self.get_by_name(name, user)
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
        application = self.get_by_name(name, user)
        application.updated_at = datetime.now()
        application.updated_by = user.id
        application.activate = True
        self._dbcontext.commit()

        self._logger.info(f"{user.email} activate application {application.name}")

        return application

    def inactivate(self, name: str, user: User):
        application = self.get_by_name(name, user)
        application.updated_at = datetime.now()
        application.updated_by = user.id
        application.activate = False
        self._dbcontext.commit()

        self._logger.info(f"{user.email} inactivate application {application.name}")

        return application

    def delete(self, name: str, user: User):
        return self.inactivate(name, user)

    def generate_name(self, application: Application) -> str:
        """
        Genarate unique name for Application
        """
        application.generate_name()
        while self._repository.name_exists(application.name):
            application.generate_name(f"{application.real_name}_{randint(1, 100)}")

    def add_user(self, name: str, user_id: int, user: User) -> Application:
        application = self.get_by_name(name, user)
        application.add_user(user_id)
        application.updated_at = datetime.now()
        application.updated_by = user.id
        self._dbcontext.commit()

        self._logger.info(
            f"{user.email} add new user into application {application.name}")

        return application

    def remove_user(self, name: str, user_id: int, user: User) -> Application:
        application = self.get_by_name(name, user)
        self._dbcontext.execute(
            "DELETE FROM application_users WHERE application_id = :application_id AND user_id = :user_id",
            {"application_id": application.id, "user_id": user_id})
        self._dbcontext.commit()

        self._logger.info(
            f"{user.email} remove user({user_id}) on application {application.name}")

        return application

    def add_feature(self, name: str, data: dict, user: User) -> Application:
        application = self.get_by_name(name, user)
        application.add_feature(
            environment_id=data["environment_id"],
            name=data["name"],
            enable=data["enable"],
            user=user
        )
        self._dbcontext.commit()

        self._logger.info(
            f"{user.email} add new feature into application({application.name})")

        return application

    def add_feature_all_environments(self, name: str, data: dict, user: User) -> Application:
        try:
            application = self.get_by_name(name, user)
            for environment in self._environment_repository.get_all():
                application.add_feature(
                    environment_id=environment.id,
                    name=data["name"],
                    enable=data["enable"],
                    user=user
                )

            self._dbcontext.commit()

            self._logger.info(
                f"{user.email} add new features into application({application.name})")

            return application
        except Exception as e:
            self._dbcontext.rollback()
            self._logger.error(f"Error occurred when {user.email} tryng to add new features {str(e)}")
            raise

    def remove_feature(self, name: str, feature_name: str, environment_id: int, user: User) -> Application:
        application = self.get_by_name(name, user)
        for key, feature in enumerate(application.features):
            if feature.name == feature_name and feature.environment_id == environment_id:
                del application.features[key]
        self._dbcontext.commit()

        self._logger.info(
            f"{user.email} remove feature({feature_name}) from applicarion({application.name})")

        return application

    def remove_feature_all_environments(self, name: str, feature_name: str, user: User) -> Application:
        application = self.get_by_name(name, user)
        for key, feature in enumerate(application.features):
            if feature.name == feature_name:
                del application.features[key]
        self._dbcontext.commit()

        self._logger.info(
            f"{user.email} remove features for all environments from applicarion({application.name})")

        return application

    def activate_feature(self, name: str, environment_id: int, feature_name: str, user: User) -> Application:
        return self.toggle_feature(name, environment_id, feature_name, True, user)

    def inactivate_feature(self, name: str, environment_id: int, feature_name: str, user: User) -> Application:
        return self.toggle_feature(name, environment_id, feature_name, False, user)

    def toggle_feature(self, name: str, env: int, feature_name: str, status: bool, user: User) -> Application:
        application = self.get_by_name(name, user)
        for feature in application.features:
            if feature.name == feature_name and feature.environment_id == env:
                feature.enable = status
                feature.updated_at = datetime.now()
                feature.updated_by = user.id
        self._dbcontext.commit()

        self._logger.info(
            f"{user.email} toggle({feature_name}) for({status}) into application({application.name}) in env({env})")

        return application

    def activate_all_feature(self, name: str, user: User) -> Application:
        return self.toggle_all_features(name, True, user)

    def inactivate_all_feature(self, name: str, user: User) -> Application:
        return self.toggle_all_features(name, False, user)

    def toggle_all_features(self, name: str, status: bool, user: User) -> Application:
        try:
            application = self.get_by_name(name, user)
            for feature in application.features:
                feature.enable = status
                feature.updated_at = datetime.now()
                feature.updated_by = user.id
            self._dbcontext.commit()

            self._logger.info(
                f"{user.email} toggle all features for({status}) into application({name})")

            return application
        except Exception as e:
            self._dbcontext.rollback()
            self._logger.error(
                f"Error occurred when {user.email} tryng to toggle({status}) features into {name}, {str(e)}")
            raise
