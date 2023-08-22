from fastapi import APIRouter, Depends

from .dependencies.service import get_auth_service
from ..dto.request import ReLoginRequest
from ..dto.response import SigninResponse, ReLoginResponse
from ..services.auth import AuthService


router = APIRouter()


@router.post("/signin")
async def signin(
    auth_service: AuthService = Depends(get_auth_service),
) -> SigninResponse:
    access_token, refresh_token = auth_service.signin()
    return SigninResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/relogin")
async def relogin(
    re_login_request: ReLoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> ReLoginResponse:
    access_token, refresh_token = auth_service.re_login(re_login_request.refresh_token)
    return ReLoginResponse(access_token=access_token, refresh_token=refresh_token)
