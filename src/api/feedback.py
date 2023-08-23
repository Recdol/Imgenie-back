from fastapi import APIRouter, Depends

from .dependencies.service import get_feedback_service
from .dependencies.auth import get_current_user
from ..dto.request import UserFeedbackRequest
from ..services.feedback import FeedbackService
from ..db import User

router = APIRouter()


@router.post("/userFeedback")
async def user_feedback(
    data: UserFeedbackRequest,
    user: User = Depends(get_current_user),
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> None:
    feedback_service.log_user_feedback(user, data)
