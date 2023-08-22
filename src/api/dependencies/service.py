from fastapi import Depends
from logging import Logger

from .db import get_repository
from .infer import get_playlist_id_extractor, get_song_extractor
from ...services.auth import AuthService
from ...services.feedback import FeedbackService
from ...services.music import MusicService
from ...infer.playlist import PlaylistIdExtractor
from ...infer.song import SongExtractor
from ...db import UserRepository, AuthRepository, PlaylistRepository
from ...config import AppConfig, get_app_config
from ...log.logger import get_feedback_logger, get_user_logger


def get_auth_service(
    config: AppConfig = Depends(get_app_config),
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
    auth_repository: AuthRepository = Depends(get_repository(AuthRepository)),
) -> AuthService:
    return AuthService(config, user_repository, auth_repository)


def get_feedback_service(
    feedback_logger: Logger = Depends(get_feedback_logger),
) -> FeedbackService:
    return FeedbackService(feedback_logger)


def get_music_service(
    user_logger: Logger = Depends(get_user_logger),
    playlist_repository: PlaylistRepository = Depends(
        get_repository(PlaylistRepository)
    ),
    playlist_id_ext: PlaylistIdExtractor = Depends(get_playlist_id_extractor),
    song_ext: SongExtractor = Depends(get_song_extractor),
) -> MusicService:
    return MusicService(user_logger, playlist_repository, playlist_id_ext, song_ext)
