from fastapi import APIRouter, Depends

from .dependencies.service import get_feedback_service
from ..dto.request import UserFeedbackRequest
from ..services.feedback import FeedbackService

router = APIRouter()


@router.post("/userFeedback")
async def user_feedback(
    data: UserFeedbackRequest,
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> None:
    feedback_service.log_user_feedback(data)
