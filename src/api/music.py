from fastapi import APIRouter, UploadFile, File, Depends

from .dependencies.service import get_music_service
from .dependencies.auth import get_current_user
from ..dto.response import RecommendMusicResponse
from ..dto.request import RecommendMusicRequest
from ..services.music import MusicService
from ..db import User


router = APIRouter()


@router.post("/recommendMusic")
async def recommend_music(
    image: UploadFile = File(...),
    data: RecommendMusicRequest = Depends(RecommendMusicRequest.as_form),
    user: User = Depends(get_current_user),
    music_service: MusicService = Depends(get_music_service),
) -> RecommendMusicResponse:
    return music_service.recommend_music(user, image, data)
