import pytest
from logging import Logger
from unittest.mock import MagicMock

from src.config import AppConfig


@pytest.fixture
def mock_config() -> AppConfig:
    return AppConfig(
        db_host="db_host",
        db_name="db_name",
        db_username="db_username",
        db_password="db_password",
    )


@pytest.fixture
def mock_logger() -> Logger:
    return MagicMock(spec=Logger)
