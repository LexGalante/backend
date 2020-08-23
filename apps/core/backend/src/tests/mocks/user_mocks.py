from typing import List
from random import randint

from models.user import User


def get_mock_single_user(number: int = None) -> User:
    if number is None:
        number = randint(1, 100)
    user = User()
    user.id = number
    user.email = f"{number}@iggle.com"
    user.password = f"{str(number).zfill(10)}"
    user.active = True if number % 2 == 0 else False

    return user


def get_mock_users(number_of_users: int = 20, **kwargs) -> List[User]:
    users = []
    for index in range(1, 20):
        users.append(get_mock_single_user(index))

    return users[1: number_of_users]
