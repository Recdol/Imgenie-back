import pytest
from unittest.mock import MagicMock
from datetime import datetime, date

from src.db import (
    User,
    Artist,
    Album,
    Song,
    Playlist,
    Inference,
    InferenceQuery,
    InferenceOutput,
    InferenceFeedback,
    InferenceRepository,
    SongRepository,
    UserRepository,
    AuthRepository,
    PlaylistRepository,
)


@pytest.fixture
def user() -> User:
    return User(id="user")


@pytest.fixture
def artist() -> Artist:
    return Artist(
        id="artist",
        genie_id="g_artist",
        name="주혜인",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def album() -> Album:
    return Album(
        id="album",
        genie_id="g_album",
        name="민석05의 앨범",
        img_url="http://img.png",
        released_date=date.today(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def song(artist: Artist, album: Album) -> Song:
    return Song(
        id="song",
        genie_id="g_song",
        title="찬미송",
        lyrics="가사는 어디까지 길어질 수 있을까?를 시험해보고 싶지만 그냥 귀찮아서 여기까지 적는다. 유후후~",
        album=album,
        artist=artist,
        like_cnt=10,
        listener_cnt=20,
        play_cnt=100,
        genres=["POP"],
        spotify_url="http://spotify.com/123.mp3",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def playlist(song: Song) -> Playlist:
    return Playlist(
        id="playlist",
        genie_id="g_playlist",
        title="동맘의 뽕짝 1선",
        subtitle="동여니가 젤 좋아하는 노래로 준비했어요~ ^^",
        song_cnt=1,
        like_cnt=99,
        view_cnt=100,
        tags=["행복"],
        songs=[song],
        img_url="http://img/img.jpg",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def inference(user: User, song: Song, playlist: Playlist) -> Inference:
    return Inference(
        id="inference",
        user=user,
        query=InferenceQuery(image_url="http://img/query.jpg", genres=["POP"]),
        output=InferenceOutput(playlists=[playlist], songs=[song]),
        feedback=InferenceFeedback(like_songs=[]),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def mock_inference_repository(inference: Inference) -> InferenceRepository:
    mock = MagicMock(spec=InferenceRepository)
    mock.create_inference.return_value = inference
    return mock


@pytest.fixture
def mock_song_repository(song: Song) -> SongRepository:
    mock = MagicMock(spec=SongRepository)
    mock.find_by_genie_id.return_value = song
    return mock


@pytest.fixture
def mock_user_repository() -> UserRepository:
    return MagicMock(spec=UserRepository)


@pytest.fixture
def mock_auth_repository() -> AuthRepository:
    return MagicMock(spec=AuthRepository)


@pytest.fixture
def mock_playlist_repository() -> PlaylistRepository:
    return MagicMock(spec=PlaylistRepository)
