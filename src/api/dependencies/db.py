from typing import Type, TypeVar, Callable

from ...db import (
    AlbumRepository,
    ArtistRepository,
    PlaylistRepository,
    SongRepository,
    UserRepository,
    AuthRepository,
    InferenceRepository,
)

Repository = TypeVar(
    "Repository",
    AlbumRepository,
    ArtistRepository,
    PlaylistRepository,
    SongRepository,
    UserRepository,
    AuthRepository,
    InferenceRepository,
)


def get_repository(repo_type: Type[Repository]) -> Callable[[], Repository]:
    def _get_repo() -> Repository:
        return repo_type()

    return _get_repo
