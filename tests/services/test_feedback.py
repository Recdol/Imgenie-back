import pytest
from unittest.mock import MagicMock

from src.services.feedback import FeedbackService
from src.db import User, Song, Inference, InferenceRepository, SongRepository
from src.dto.request import UserFeedbackRequest


@pytest.fixture
def feedback_service(
    mock_inference_repository: InferenceRepository,
    mock_song_repository: SongRepository,
    song: Song,
) -> FeedbackService:
    mock_song_repository.find_by_id.return_value = song
    return FeedbackService(
        inference_repository=mock_inference_repository,
        song_repository=mock_song_repository,
    )


@pytest.fixture
def like_user_feedback_request(
    feedback_song: Song, inference: Inference
) -> UserFeedbackRequest:
    return UserFeedbackRequest(
        song_id=feedback_song.id, inference_id=inference.id, is_like=True
    )


@pytest.fixture
def dislike_user_feedback_request(
    feedback_song: Song, inference: Inference
) -> UserFeedbackRequest:
    return UserFeedbackRequest(
        song_id=feedback_song.id, inference_id=inference.id, is_like=False
    )


@pytest.fixture
def feedback_song(inference: Inference) -> Song:
    # 피드백 받을 대상 노래
    return inference.output.songs[0]


def test_user_feedback__should_add_song_in_like_songs_when_is_like_is_true(
    feedback_service: FeedbackService,
    user: User,
    feedback_song: Song,
    inference: Inference,
    like_user_feedback_request: UserFeedbackRequest,
    mock_inference_repository: MagicMock | InferenceRepository,
):
    feedback_service.user_feedback(user, request=like_user_feedback_request)

    mock_inference_repository.add_feedback_like_song_by_id.assert_called_once_with(
        inference.id, feedback_song
    )


def test_user_feedback__should_add_song_in_like_songs_when_is_like_is_false(
    feedback_service: FeedbackService,
    user: User,
    feedback_song: Song,
    inference: Inference,
    dislike_user_feedback_request: UserFeedbackRequest,
    mock_inference_repository: MagicMock | InferenceRepository,
):
    feedback_service.user_feedback(user, request=dislike_user_feedback_request)

    mock_inference_repository.delete_feedback_like_song.assert_called_once_with(
        inference.id, feedback_song
    )
