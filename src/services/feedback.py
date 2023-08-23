from logging import Logger

from ..dto.request import UserFeedbackRequest
from ..db import User


class FeedbackService:
    def __init__(self, feedback_logger: Logger) -> None:
        self.feedback_logger = feedback_logger

    def log_user_feedback(self, user: User, data: UserFeedbackRequest) -> None:
        self.feedback_logger.info(
            {
                "User Id": user.id,
                "song Id": data.song_id,
                "is like": data.is_like,
            }
        )
