import pytest
from logging import Logger
from unittest.mock import MagicMock, Mock, patch

from src.services.music import MusicService
from src.config import AppConfig
from src.db import (
    PlaylistRepository,
    InferenceRepository,
    Song,
    Playlist,
    User,
    Inference,
)
from src.infer.playlist import PlaylistIdExtractor
from src.infer.song import SongExtractor
from src.dto.request import RecommendMusicRequest


@pytest.fixture
def mock_playlist_id_extractor(playlist: Playlist) -> PlaylistIdExtractor:
    mock = MagicMock()
    mock.get_weather_playlist_id.return_value = ([0.1], playlist.id)
    mock.get_mood_playlist_id.return_value = ([0.1], playlist.id)
    mock.get_sit_playlist_id.return_value = ([0.1], playlist.id)

    return mock


@pytest.fixture
def mock_song_extractor(song: Song) -> SongExtractor:
    mock = MagicMock()
    mock.extract_songs.return_value = [song]

    return mock


@pytest.fixture
def music_service(
    mock_config: AppConfig,
    mock_logger: Logger,
    mock_playlist_repository: PlaylistRepository,
    mock_inference_repository: InferenceRepository,
    mock_playlist_id_extractor: PlaylistIdExtractor,
    mock_song_extractor: SongExtractor,
    inference: Inference,
) -> MusicService:
    mock_inference_repository.create_inference.return_value = inference

    with patch.object(MusicService, "_save_query_image"), patch.object(
        MusicService, "_resize_query_image"
    ):
        yield MusicService(
            config=mock_config,
            logger=mock_logger,
            playlist_repository=mock_playlist_repository,
            inference_respository=mock_inference_repository,
            playlist_id_ext=mock_playlist_id_extractor,
            song_ext=mock_song_extractor,
        )


@pytest.fixture
def recommend_music_reqesut() -> RecommendMusicRequest:
    return RecommendMusicRequest(genres=["POP", "락"])


def test_recommend_music(
    user: User,
    music_service: MusicService,
    recommend_music_reqesut: RecommendMusicRequest,
):
    image = Mock()
    response = music_service.recommend_music(user, image, recommend_music_reqesut)

    assert response.inference_id is not None
    assert response.songs is not None
