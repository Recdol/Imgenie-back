from fastapi import APIRouter, Depends

from .dependencies.service import get_auth_service
from ..dto.response.auth import NewUserResponse
from ..services.auth import AuthService


router = APIRouter()


@router.post("/newUser")
async def new_user(
    auth_service: AuthService = Depends(get_auth_service),
) -> NewUserResponse:
    user = auth_service.new_user()
    return NewUserResponse(user_id=user.id)
