from fastapi import Depends, Security
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException
from starlette.requests import Request

from .service import get_auth_service
from ...exceptions.auth import RequiredTokenException
from ...exceptions.error_type import ErrorType
from ...services.auth import AuthService
from ...db import User

HEADER_KEY = "Authorization"


class JWTAPIKeyHeader(APIKeyHeader):
    async def __call__(self, request: Request) -> str | None:
        try:
            return await super().__call__(request)
        except HTTPException:
            raise RequiredTokenException(error_type=ErrorType.NOT_AUTHENTICATED)


def _get_authorization_header(
    api_key: str = Security(JWTAPIKeyHeader(name=HEADER_KEY)),
) -> str:
    return api_key


async def get_current_user(
    token: str = Depends(_get_authorization_header),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    return auth_service.logged_in_user(token)


async def get_current_user_optional(
    token: str = Depends(_get_authorization_header),
    auth_service: AuthService = Depends(get_auth_service),
) -> User | None:
    if token:
        return get_current_user(token, auth_service)

    return None
