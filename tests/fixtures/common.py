import pytest
from logging import Logger
from unittest.mock import MagicMock

from src.config import AppConfig


@pytest.fixture
def mock_config() -> AppConfig:
    return AppConfig(
        spotify_pwd="spotify_pwd",
        spotify_cid="spotify_cid",
        db_host="db_host",
        db_name="db_name",
        db_username="db_username",
        db_password="db_password",
        jwt_secret="jwt_secret",
    )


@pytest.fixture
def mock_logger() -> Logger:
    return MagicMock(spec=Logger)
