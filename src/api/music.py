from fastapi import APIRouter, UploadFile, File, Depends

from .dependencies.service import get_music_service
from ..dto.response import RecommendMusicResponse
from ..dto.request import RecommendMusicRequest
from ..services.music import MusicService


router = APIRouter()


@router.post("/recommendMusic")
async def recommend_music(
    image: UploadFile = File(...),
    data: RecommendMusicRequest = Depends(RecommendMusicRequest.as_form),
    music_service: MusicService = Depends(get_music_service),
) -> RecommendMusicResponse:
    return music_service.recommend_music(image, data)
