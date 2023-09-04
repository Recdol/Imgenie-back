from ..dto.request import UserFeedbackRequest
from ..db import User, InferenceRepository, SongRepository


class FeedbackService:
    def __init__(
        self,
        inference_repository: InferenceRepository,
        song_repository: SongRepository,
    ) -> None:
        self.inference_repository = inference_repository
        self.song_repository = song_repository

    def user_feedback(self, user: User, request: UserFeedbackRequest) -> None:
        song = self.song_repository.find_by_genie_id(request.song_id)

        if request.is_like:
            self.inference_repository.add_feedback_like_song_by_id(
                request.inference_id, song
            )
        else:
            self.inference_repository.delete_feedback_like_song(
                request.inference_id, song
            )
