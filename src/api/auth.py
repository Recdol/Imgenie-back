from fastapi import APIRouter, Depends, Response
from datetime import datetime, timedelta, timezone

from .dependencies.service import get_auth_service
from .dependencies.auth import get_current_user
from ..config import AppConfig, get_app_config
from ..services.auth import AuthService


router = APIRouter()


@router.get("/newUser")
async def new_user(
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
    config: AppConfig = Depends(get_app_config),
):
    user = auth_service.new_user()

    if config.is_dev:
        response.set_cookie(
            key="user_id",
            value=user.id,
            httponly=True,
            expires=datetime.now(timezone.utc) + timedelta(days=365),
        )
    else:
        response.set_cookie(
            key="user_id",
            value=user.id,
            httponly=True,
            secure=True,
            expires=datetime.now(timezone.utc) + timedelta(days=365),
        )


@router.get("/checkUser", dependencies=[Depends(get_current_user)])
async def check_user():
    pass
