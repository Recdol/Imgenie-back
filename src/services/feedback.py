from ..dto.request import UserFeedbackRequest
from ..db import User, Inference, InferenceRepository, SongRepository
from ..exceptions.common import ForbiddenException
from ..exceptions.error_type import ErrorType


class FeedbackService:
    def __init__(
        self,
        inference_repository: InferenceRepository,
        song_repository: SongRepository,
    ) -> None:
        self.inference_repository = inference_repository
        self.song_repository = song_repository

    def user_feedback(self, user: User, request: UserFeedbackRequest) -> None:
        inference = self.inference_repository.find_by_id(request.inference_id)
        FeedbackService._validate_user(user, inference)

        song = self.song_repository.find_by_id(request.song_id)

        if request.is_like:
            self.inference_repository.add_feedback_like_song_by_id(inference.id, song)
        else:
            self.inference_repository.delete_feedback_like_song(inference.id, song)

    @staticmethod
    def _validate_user(user: User, inference: Inference) -> None:
        print(user, inference)

        if inference.user != user:
            raise ForbiddenException(error_type=ErrorType.FORBIDDEN_USER)
