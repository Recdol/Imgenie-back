from typing import Iterable
from functools import cache
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    db_host: str
    db_name: str
    db_username: str
    db_password: str

    # model
    hub_path: str = "hub"
    model_repo: str = "Recdol/PL_Multilabel"

    # model
    weather_model_version: str = "weather-25_150958"
    sit_model_version: str = "sit-25_133334"
    mood_model_version: str = "mood-25_144428"

    # plyalist dataset
    weather_dataset_versions: Iterable[str] = (
        "playlists_0709_v2_resized",
        "selected_playlist_0714_resized",
    )
    sit_dataset_versions: Iterable[str] = (
        "playlists_0709_v2_resized",
        "selected_playlist_0714_resized",
    )
    mood_dataset_versions: Iterable[str] = (
        "playlists_0709_v2_resized",
        "selected_playlist_0714_resized",
    )

    # index
    weather_index_version: str = "weather-25_150958"
    sit_index_version: str = "sit-25_133334"
    mood_index_version: str = "mood-25_144428"

    playlist_k: int = 6
    is_playlist_data_pull: bool = False

    # image
    image_size: int = 224

    is_dev: bool

    class Config:
        frozen = True
        env_file = ".env"


@cache
def get_app_config() -> AppConfig:
    return AppConfig()
