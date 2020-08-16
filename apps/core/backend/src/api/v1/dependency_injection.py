from typing import Generator

from fastapi import Depends

from resources.dbcontext import DbContext
from services.user_service import UserService
from repositories.user_repository import UserRepository


def get_dbcontext() -> Generator:
    try:
        dbcontext = DbContext()

        yield dbcontext
    finally:
        dbcontext.session.close()


def get_user_repository(dbcontext: DbContext = Depends(get_dbcontext)) -> UserRepository:
    return UserRepository(dbcontext)


def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository)

