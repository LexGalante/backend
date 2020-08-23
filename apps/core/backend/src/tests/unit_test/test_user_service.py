from pytest_mock import MockerFixture

from resources.dbcontext import DbContext
from services.user_service import UserService
from models.user import User

from tests.tools.fake_dbcontext import FakeDbContext
from tests.mocks.user_mocks import get_mock_users, get_mock_single_user


def test_get_all_should_return_and_paginate_users(mocker: MockerFixture):
    # ARRANGE
    mock_users = get_mock_users()
    dbcontext: DbContext() = DbContext()
    dbcontext.session = mocker.MagicMock(return_value=object)
    service: UserService = UserService(dbcontext)
    service._repository.get_all = mocker.MagicMock(return_value=mock_users)
    # ACT
    users = service.get_all(1, 10)
    # ASSERT
    assert len(users) == len(mock_users)


def test_get_by_email_should_return_user(mocker: MockerFixture):
    # ARRANGE
    mock_user = get_mock_single_user()
    dbcontext: DbContext() = DbContext()
    dbcontext.session = mocker.MagicMock(return_value=object)
    service: UserService = UserService(dbcontext)
    service._repository.get_by_email = mocker.MagicMock(return_value=mock_user)
    # ACT
    user = service.get_by_email(mock_user.email)
    # ASSERT
    assert user == mock_user


def test_create_should_create_user(mocker: MockerFixture):
    # ARRANGE
    user_mock = get_mock_single_user()
    dbcontext: FakeDbContext = FakeDbContext()
    service: UserService = UserService(dbcontext)
    # ACT
    user: User = service.create(user_mock.__dict__)
    # ASSERT
    assert user.id == user_mock.id
    assert user.email == user_mock.email
    assert user.active == user_mock.active
