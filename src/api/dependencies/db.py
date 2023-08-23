from typing import Type, TypeVar, Callable

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


def get_repository(repo_type: Type[Repository]) -> Callable[[], Repository]:
    def _get_repo() -> Repository:
        return repo_type()

    return _get_repo
