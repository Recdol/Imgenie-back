from fastapi import APIRouter, Depends, Response

from .dependencies.service import get_auth_service
from ..dto.response.auth import NewUserResponse
from ..services.auth import AuthService


router = APIRouter()


@router.post("/newUser")
async def new_user(
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> NewUserResponse:
    user = auth_service.new_user()

    response.set_cookie(key="user_id", value=user.id)
    return NewUserResponse(user_id=user.id)
