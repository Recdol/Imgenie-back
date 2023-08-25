import pytest
from unittest.mock import MagicMock

from datetime import datetime
from src.services.auth import AuthService
from src.config import AppConfig
from src.dto.auth import AccessTokenPayload, RefreshTokenPayload
from src.db import User, Auth, UserRepository, AuthRepository
from src.exceptions.auth import InvalidTokenException


@pytest.fixture
def logged_in_user(user: User) -> User:
    # 로그인 대상이 되는 유저
    return user


@pytest.fixture
def new_user(user: User) -> User:
    # 회원가입하는 유저
    return user


@pytest.fixture
def auth_service(
    mock_config: AppConfig,
    mock_user_repository: UserRepository | MagicMock,
    mock_auth_repository: AuthRepository,
    logged_in_user: User,
    new_user: User,
    auth: Auth,
) -> AuthService:
    mock_user_repository.find_by_id.return_value = logged_in_user
    mock_user_repository.create_user.return_value = new_user
    mock_auth_repository.find_by_refresh_token.return_value = auth

    return AuthService(
        config=mock_config,
        user_repository=mock_user_repository,
        auth_repository=mock_auth_repository,
    )


@pytest.fixture
def valid_access_token(auth_service: AuthService, logged_in_user: User) -> str:
    access_token_payload = AccessTokenPayload(user_id=logged_in_user.id)
    return auth_service._AuthService__encode_access_token(access_token_payload)


@pytest.fixture
def invalid_access_token() -> str:
    return "invalid"


@pytest.fixture
def valid_refresh_token(auth_service: AuthService, logged_in_user: User) -> str:
    refresh_token_payload = RefreshTokenPayload(user_id=logged_in_user.id)
    return auth_service._AuthService__encode_refresh_token(refresh_token_payload)


@pytest.fixture
def invalid_refresh_token() -> str:
    return "invalid"


@pytest.fixture
def auth(logged_in_user: User) -> Auth:
    return Auth(
        id="auth",
        user=logged_in_user,
        refresh_token="refresh_token",
        created_at=datetime.now(),
    )


def test_logged_in_user(
    auth_service: AuthService, logged_in_user: User, valid_access_token: str
):
    user = auth_service.logged_in_user(valid_access_token)

    assert user == logged_in_user


def test_logged_in_user__if_the_access_token_is_not_valid_then_should_raise_InvalidTokenException(
    auth_service: AuthService, invalid_access_token: str
):
    with pytest.raises(InvalidTokenException):
        auth_service.logged_in_user(invalid_access_token)


def test_signin(auth_service: AuthService, logged_in_user: User):
    access_token, refresh_token = auth_service.signin()

    auth_service._AuthService__decode_access_token(access_token)
    auth_service._AuthService__decode_refresh_token(refresh_token)


def test_re_login(
    auth_service: AuthService,
    logged_in_user: User,
    valid_refresh_token: str,
    auth: Auth,
):
    auth.refresh_token = valid_refresh_token

    access_token, new_refresh_token = auth_service.re_login(valid_refresh_token)
    access_token_payload = auth_service._AuthService__decode_access_token(access_token)

    assert access_token_payload.user_id == logged_in_user.id

    new_refresh_token_payload = auth_service._AuthService__decode_refresh_token(
        new_refresh_token
    )
    assert new_refresh_token_payload.user_id == logged_in_user.id


def test_re_login__if_the_refresh_token_is_not_valid_then_should_raise_InvalidTokenException(
    auth_service: AuthService, invalid_refresh_token: str
):
    with pytest.raises(InvalidTokenException):
        auth_service.re_login(invalid_refresh_token)
