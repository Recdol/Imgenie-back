import pytest
from unittest.mock import MagicMock

from src.services.auth import AuthService
from src.config import AppConfig
from src.db import User, UserRepository
from src.exceptions.common import UnauthorizedException


@pytest.fixture
def new_user(user: User) -> User:
    # 회원가입하는 유저
    return user


@pytest.fixture
def auth_service(
    mock_config: AppConfig,
    mock_user_repository: UserRepository | MagicMock,
    user: User,
    new_user: User,
) -> AuthService:
    mock_user_repository.find_by_id.return_value = user
    mock_user_repository.create_user.return_value = new_user

    return AuthService(
        config=mock_config,
        user_repository=mock_user_repository,
    )


def test_find_user(auth_service: AuthService, user: User):
    found = auth_service.find_user(user.id)

    assert found == user


def test_find_user__when_invalid_user_id_then_throw_UnauthorizedException(
    auth_service: AuthService,
    mock_user_repository: UserRepository | MagicMock,
):
    mock_user_repository.find_by_id.return_value = None

    with pytest.raises(UnauthorizedException):
        auth_service.find_user("invalid_user_id")
