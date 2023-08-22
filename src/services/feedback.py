from ..dto.request import UserFeedbackRequest
from logging import Logger


class FeedbackService:
    def __init__(self, feedback_logger: Logger) -> None:
        self.feedback_logger = feedback_logger

    def log_user_feedback(self, data: UserFeedbackRequest) -> None:
        self.feedback_logger.info(
            {
                "session Id": data.session_id,
                "song Id": data.song_id,
                "is like": data.is_like,
            }
        )
