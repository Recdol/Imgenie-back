from fastapi import Depends
from functools import cache

from ...infer.playlist import PlaylistIdExtractor
from ...infer.song import SongExtractor
from ...config import AppConfig, get_app_config


pl_k = 15


@cache
def get_playlist_id_extractor(
    config: AppConfig = Depends(get_app_config),
    pl_k: int = pl_k,
    is_data_pull: bool = False,
) -> PlaylistIdExtractor:
    return PlaylistIdExtractor(config, pl_k, is_data_pull)


@cache
def get_song_extractor() -> SongExtractor:
    return SongExtractor()
