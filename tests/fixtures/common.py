import pytest
from logging import Logger
from unittest.mock import MagicMock

from src.config import AppConfig


@pytest.fixture
def mock_config() -> AppConfig:
    return AppConfig()


@pytest.fixture
def mock_logger() -> Logger:
    return MagicMock(spec=Logger)
