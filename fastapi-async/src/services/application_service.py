import re
import logging
from datetime import datetime
from typing import List
from textwrap import shorten
from random import randint

from databases import Database
from databases.core import Transaction

from services.user_service import UserService
from services.environment_service import EnvironmentService
from resources.database import (application_features, application_users,
                                applications)


class ApplicationService():
    def __init__(self, database: Database):
        self._database = database
        self._user_service: UserService = UserService(database)
        self._environment_service: EnvironmentService = EnvironmentService(database)
        self._logger = logging.getLogger(__name__)

    async def get_all_by_user(self, user: dict) -> List[dict]:
        sql = """
        SELECT a.*
        FROM applications a
        LEFT JOIN application_users au ON a.id = au.application_id
        WHERE au.user["id"] = :user["id"]
        """
        parameters = {"user_id": user["id"]}
        applications = await self._database.fetch_all(query=sql, values=parameters)

        return applications

    async def get_by_name(self, name: str, user: dict) -> dict:
        sql = """
        SELECT a.*
        FROM applications a
        LEFT JOIN application_users au ON a.id = au.application_id
        WHERE au.user["id"] = :user["id"]
        AND a.name = :name
        """
        parameters = {"user_id": user["id"], "name": name}
        application = await self._database.fetch_one(query=sql, values=parameters)
        if application is None:
            raise ValueError(f"Not found or Not permission access application {name}")

        return application

    async def get_id_by_name(self, name: str) -> int:
        sql = "SELECT id FROM applications WHERE name = :name"
        parameters = {"name": name}

        return int(await self._database.fetch_val(query=sql, values=parameters))

    async def create(self, application: dict, user: dict):
        transaction: Transaction = await self._database.transaction()
        try:
            name = self.generate_name(application["name"])
            sql = applications.insert().vales(
                name=name,
                real_name=application["real_name"],
                model=application["model"],
                description=application["description"],
                details=application["details"],
                active=application["active"],
                created_at=datetime.now(),
                created_by=user["id"],
                updated_at=datetime.now(),
                updated_by=user["id"]
            )
            id = await self._database.execute(sql)
            sql = application_users.insert().values(
                application_id=id,
                user_id=user["id"]
            )
            await self._database.execute(query=sql)
            transaction.commit()

            self._logger.info(
                user["email"] + f" created new application {application.name}")
        except Exception as e:
            transaction.rollback()
            self._logger.error(f"Error ocurred on create new application {str(e)}")

            raise e

    async def update(self, data: dict, name: str, user: dict):
        sql = applications.update().where(applications.c.name == name).values(
            real_name=data["real_name"],
            model=data["model"],
            description=data["description"],
            details=data["details"],
            updated_at=datetime.now(),
            updated_by=user["id"]
        )
        await self._database.execute(query=sql)
        self._logger.info(user["email"] + f" updated application {name}")

    async def activate(self, name: str, user: dict):
        await self.toggle_active(name, True, user)

    async def inactivate(self, name: str, user: dict):
        await self.toggle_active(name, True, user)

    async def toggle_active(self, name: str, active: bool, user):
        sql = applications.update().where(applications.c.name == name).values(
            updated_at=datetime.now(),
            updated_by=user["id"],
            active=True
        )
        await self._database.execute(query=sql)
        self._logger.info(user["email"] + f" activate application {name}")

    async def delete(self, name: str, user: dict):
        await self.toggle_active(name, False, user)

    async def generate_name(self, application_name: str) -> str:
        """
        Genarate unique name for dict
        """
        application_name = application_name.lower().replace(" ", "_")
        application_name = re.sub(r"[^a-zA-Z0-9]", "", application_name)
        application_name = shorten(application_name, width=30, placeholder="_")
        sql = "SELECT COUNT(*) FROM applications WHERE name = :name"
        while await self._database.fetch_val(query=sql, values={"name": application_name}) != 0:
            application_name = f"{application_name}_{randint(1, 100)}"

        return application_name

    async def add_user(self, name: str, email: int, user: dict):
        user_id = await self._user_service.get_user_id_by_email(email)
        application_id = await self.get_id_by_name(name)
        sql = application_users.insert().values(
            user_id=user_id,
            application_id=application_id
        )
        await self._database.execute(sql)

        self._logger.info(
            user["email"] + f" insert new user({email}) into application({name})")

    async def remove_user(self, name: str, email: str, user: dict):
        user_id = await self._user_service.get_user_id_by_email(email)
        application_id = await self.get_id_by_name(name)
        sql = application_users.delete().where(
            application_users.c.user_id == user_id,
            application_users.c.application_id == application_id
        )
        await self._database.execute(sql)
        self._logger.info(
            user["email"] + f" remove user({email}) on application {name}")

    async def add_feature(self, name: str, feature: dict, user: dict):
        feature_name = feature["name"].replace(" ", "_")
        application_id = await self.get_id_by_name(name)
        environments = await self._environment_service.get_all()
        transaction = await self._database.transaction()
        try:
            sql = """ 
            INSERT INTO application_features (application_id, environment_id, name, enable, created_at, created_by, updated_at, updated_by)
            VALUES (:application_id, :environment_id, :name, :enable, created_at, created_by, updated_at, updated_by);
            """
            parameters = [{
                "application_id": application_id,
                "environment_id": environment["id"],
                "name": feature_name,
                "enable": feature["enable"],
                "created_at": datetime.now(),
                "created_by": user["id"],
                "updated_at": datetime.now(),
                "updated_by": user["id"]
            } for environment in environments]
            await self._database.execute_many(query=sql, values=parameters)

            sql = applications.update().where(applications.c.name == name).value(
                updated_at=datetime.now(), updated_by=user["id"])
            await self._database.execute(query=sql)

            transaction.commit()

            self._logger.info(
                user["id"] + "insert new feature({feature_name}) into application({name})")
        except Exception as e:
            transaction.rollback()
            self._logger.error(
                f"Error ocurred on insert new feature({feature_name}) into application({name}): {str(e)}")

            raise e

    async def remove_feature(self, name: str, feature_name: str, user: dict) -> dict:
        sql = application_features.delete().where(application_features.c.name == feature_name)
        await self._database.execute(query=sql)

        self._logger.info(
            user["email"] + f" remove feature({feature_name}) into application ({name})")

    async def activate_feature(self, name: str, environment_name: str, feature_name: str, user: dict):
        return await self.toggle_feature(name, environment_name, feature_name, True, user)

    async def inactivate_feature(self, name: str, environment_name: str, feature_name: str, user: dict):
        return await self.toggle_feature(name, environment_name, feature_name, False, user)

    async def toggle_feature(self, name: str, environment_name: str, feature_name: str, status: bool, user: dict):
        environment_id = await self._environment_service.get_id_by_name(environment_name)
        sql = application_features.update().where(
            application_features.c.feature_name == feature_name,
            application_features.c.environment_id == environment_id
        ).values(enable=status)
        await self._database.execute(query=sql)

        self._logger.info(user["email"] + f" toggle({feature_name}) for({status}) into application({name})")

    async def activate_all_feature(self, name: str, user: dict) -> dict:
        return await self.toggle_all_features(name, True, user)

    async def inactivate_all_feature(self, name: str, user: dict) -> dict:
        return await self.toggle_all_features(name, False, user)

    async def toggle_all_features(self, feature_name: str, status: bool, user: dict) -> dict:
        sql = application_features.update().where(
            application_features.c.feature_name == feature_name
        ).values(enable=status)
        await self._database.execute(query=sql)

        self._logger.info(user["email"] + f" toggle({feature_name}) for({status})")

