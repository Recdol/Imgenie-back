from fastapi import Depends, Security
from fastapi.security import APIKeyCookie
from starlette.exceptions import HTTPException
from starlette.requests import Request

from .service import get_auth_service
from ...exceptions.common import UnauthorizedException
from ...exceptions.error_type import ErrorType
from ...services.auth import AuthService
from ...db import User

COOKIE_KEY = "user_id"


class AuthAPIKeyCookie(APIKeyCookie):
    async def __call__(self, request: Request) -> str | None:
        try:
            return await super().__call__(request)
        except HTTPException:
            raise UnauthorizedException(error_type=ErrorType.NOT_AUTHENTICATED)


def _get_user_id_cookie(
    user_id: str = Security(AuthAPIKeyCookie(name="user_id")),
) -> str:
    return user_id


async def get_current_user(
    user_id: str = Depends(_get_user_id_cookie),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    return auth_service.find_user(user_id)


async def get_current_user_optional(
    user_id: str = Depends(_get_user_id_cookie),
    auth_service: AuthService = Depends(get_auth_service),
) -> User | None:
    if user_id:
        return get_current_user(user_id, auth_service)

    return None
