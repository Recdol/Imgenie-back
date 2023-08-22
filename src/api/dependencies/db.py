from typing import Type, TypeVar

from ...db import (
    AlbumRepository,
    ArtistRepository,
    PlaylistRepository,
    SongRepository,
    UserRepository,
    AuthRepository,
)

Repository = TypeVar(
    "Repository",
    AlbumRepository,
    ArtistRepository,
    PlaylistRepository,
    SongRepository,
    UserRepository,
    AuthRepository,
)


def get_repository(repo_type: Type[Repository]) -> Repository:
    return repo_type()
