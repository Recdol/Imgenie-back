from fastapi import APIRouter, Depends, Response
from datetime import datetime

from .dependencies.service import get_auth_service
from .dependencies.auth import get_current_user
from ..services.auth import AuthService


router = APIRouter()


@router.get("/newUser")
async def new_user(
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = auth_service.new_user()

    response.set_cookie(
        key="user_id",
        value=user.id,
        secure=True,
        httponly=True,
        expires=datetime(year=10),
    )


@router.get("/checkUser", dependencies=[Depends(get_current_user)])
async def check_user():
    pass
