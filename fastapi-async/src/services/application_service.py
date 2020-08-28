import re
import logging
from datetime import datetime
from typing import List
from textwrap import shorten

from databases import Database
from databases.core import Transaction
from asyncpg.exceptions import UniqueViolationError

from services.user_service import UserService
from services.environment_service import EnvironmentService
from resources.database import (application_features, application_users,
                                applications)


class ApplicationService:
    def __init__(self, database: Database, user_service: UserService, environment_service: EnvironmentService):
        self._database = database
        self._user_service: UserService = user_service
        self._environment_service: EnvironmentService = environment_service
        self._logger = logging.getLogger(__name__)

    async def get_all_by_user(self, user: dict) -> List[dict]:
        sql = """
        SELECT a.*
        FROM applications a
        LEFT JOIN application_users au ON a.id = au.application_id
        WHERE au.user_id = :user_id
        """
        parameters = {"user_id": user["id"]}
        applications = await self._database.fetch_all(query=sql, values=parameters)

        return applications

    async def get_by_name(self, name: str, user: dict) -> dict:
        sql = """
        SELECT a.*
        FROM applications a
        LEFT JOIN application_users au ON a.id = au.application_id
        WHERE au.user_id = :user_id
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

        return await self._database.fetch_val(query=sql, values=parameters)

    async def get_application_users(self, name: str, user: dict) -> List[str]:
        application = await self.get_by_name(name, user)
        sql = """
        SELECT email
        FROM application_users au
        INNER JOIN users u on u.id = au.user_id
        WHERE au.application_id = :id
        """
        return await self._database.fetch_all(query=sql, values={"id": application["id"]})

    async def get_application_features(self, name: str, user: dict) -> List[dict]:
        application = await self.get_by_name(name, user)
        sql = """
        SELECT e.name AS environment, af.name, af.enable
        FROM application_features af
        INNER JOIN environments e ON e.id = af.environment_id
        WHERE application_id  = :id
        """
        return await self._database.fetch_all(query=sql, values={"id": application["id"]})

    async def create(self, application: dict, user: dict):
        transaction: Transaction = await self._database.transaction()
        try:
            if "details" not in application.keys():
                application["details"] = None
            if "active" not in application.keys():
                application["active"] = True
            name = self.generate_name(application["real_name"])
            sql = applications.insert().values(
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
            self._logger.info(user["email"] + f" created new application {name}")
        except UniqueViolationError:
            await transaction.rollback()
            raise ValueError(f"application {name} already exists")
        except Exception as e:
            await transaction.rollback()
            self._logger.error(f"Error ocurred on create new application {str(e)}")

            raise e
        else:
            await transaction.commit()

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
        await self.toggle_active(name, False, user)

    async def toggle_active(self, name: str, active: bool, user):
        sql = applications.update().where(applications.c.name == name).values(
            updated_at=datetime.now(),
            updated_by=user["id"],
            active=active
        )
        await self._database.execute(query=sql)
        self._logger.info(user["email"] + f" activate application {name}")

    async def delete(self, name: str, user: dict):
        await self.toggle_active(name, False, user)

    def generate_name(self, application_name: str) -> str:
        """
        Genarate unique name for dict
        """
        application_name = application_name.lower().replace(" ", "_")
        application_name = re.sub(r"[^a-zA-Z0-9]", "", application_name)
        application_name = shorten(application_name, width=30, placeholder="_")

        return application_name

    async def add_user(self, name: str, email: int, user: dict):
        try:
            new_user = await self._user_service.get_by_email(email)
            application = await self.get_by_name(name, user)
            sql = application_users.insert().values(
                user_id=new_user["id"],
                application_id=application["id"]
            )
            await self._database.execute(sql)

            self._logger.info(
                user["email"] + f" insert new user({email}) into application({name})")
        except UniqueViolationError:
            raise ValueError(f"user {email} already exists in application {name}")

    async def remove_user(self, name: str, email: str, user: dict):
        remove_user = await self._user_service.get_by_email(email)
        application = await self.get_by_name(name, user)
        sql = "DELETE FROM application_users WHERE user_id = :user_id AND application_id = :application_id"
        parameters = {"user_id": remove_user["id"], "application_id": application["id"]}
        await self._database.execute(query=sql, values=parameters)
        self._logger.info(user["email"] + f" remove user({email}) on application {name}")

    async def add_feature(self, name: str, feature: dict, user: dict):
        feature_name = feature["name"].replace(" ", "_")
        application = await self.get_by_name(name, user)
        environments = await self._environment_service.get_all()
        transaction = await self._database.transaction()
        try:
            sql = """ 
            INSERT INTO application_features
                (application_id, environment_id, name, enable, created_at, created_by, updated_at, updated_by)
            VALUES
                (:application_id, :environment_id, :name, :enable, :created_at, :created_by, :updated_at, :updated_by);
            """
            parameters = [{
                "application_id": application["id"],
                "environment_id": environment["id"],
                "name": feature_name,
                "enable": feature["enable"],
                "created_at": datetime.now(),
                "created_by": user["id"],
                "updated_at": datetime.now(),
                "updated_by": user["id"]
            } for environment in environments]
            await self._database.execute_many(query=sql, values=parameters)

            sql = applications.update().where(applications.c.name == name).values(
                updated_at=datetime.now(), updated_by=user["id"])
            await self._database.execute(query=sql)
            self._logger.info(user["email"] + f"insert new feature({feature_name}) into application({name})")
        except UniqueViolationError:
            await transaction.rollback()
            raise ValueError(f"this feature already exists in application {name}")
        except Exception as e:
            await transaction.rollback()
            self._logger.error(
                f"Error ocurred on insert new feature({feature_name}) into application({name}): {str(e)}")

            raise e
        else:
            await transaction.commit()

    async def remove_feature(self, name: str, feature_name: str, user: dict):
        application = await self.get_by_name(name, user)
        sql = application_features.delete().where(
            application_features.c.name == feature_name
        ).where(application_features.c.application_id == application["id"])
        await self._database.execute(query=sql)

        self._logger.info(user["email"] + f" remove feature({feature_name}) into application ({name})")

    async def activate_feature(self, name: str, environment_name: str, feature_name: str, user: dict):
        return await self.toggle_feature(name, environment_name, feature_name, True, user)

    async def inactivate_feature(self, name: str, environment_name: str, feature_name: str, user: dict):
        return await self.toggle_feature(name, environment_name, feature_name, False, user)

    async def toggle_feature(self, name: str, environment_name: str, feature_name: str, status: bool, user: dict):
        environment = await self._environment_service.get_by_name(environment_name)
        sql = application_features.update().where(
            application_features.c.name == feature_name
        ).where(
            application_features.c.environment_id == environment["id"]
        ).values(enable=status)
        await self._database.execute(query=sql)

        self._logger.info(user["email"] + f" toggle({feature_name}) for({status}) into application({name})")

    async def activate_all_feature(self, name: str, user: dict):
        return await self.toggle_all_features(name, True, user)

    async def inactivate_all_feature(self, name: str, user: dict):
        return await self.toggle_all_features(name, False, user)

    async def toggle_all_features(self, name: str, status: bool, user: dict):
        application = await self.get_by_name(name, user)
        sql = "UPDATE application_features SET enable = :enable WHERE application_id = :application_id"
        parameters = {"enable": status, "application_id": application["id"]}
        await self._database.execute(query=sql, values=parameters)

        self._logger.info(user["email"] + f" toggle({name}) for({status})")
