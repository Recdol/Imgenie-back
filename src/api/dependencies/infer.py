from fastapi import Depends
from functools import cache

from ...infer.playlist import PlaylistIdExtractor
from ...infer.song import SongExtractor
from ...config import AppConfig, get_app_config


@cache
def get_playlist_id_extractor(
    config: AppConfig = Depends(get_app_config),
    is_data_pull: bool = False,
) -> PlaylistIdExtractor:
    return PlaylistIdExtractor(config, is_data_pull)


@cache
def get_song_extractor() -> SongExtractor:
    return SongExtractor()
