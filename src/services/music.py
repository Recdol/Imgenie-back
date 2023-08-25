from fastapi import UploadFile
from logging import Logger
from PIL import Image
import os

from ..infer.playlist import PlaylistIdExtractor
from ..infer.song import SongExtractor
from ..dto.response import RecommendMusicResponse, RecommendMusic
from ..dto.request import RecommendMusicRequest
from ..db import (
    User,
    Playlist,
    Song,
    PlaylistRepository,
    InferenceRepository,
    NotFoundPlaylistException,
)
from ..config import AppConfig


top_k = 6  # song_k must be more than 6 or loop of silder must be False
IMG_PATH = "outputs/userImgs/"


class MusicService:
    def __init__(
        self,
        config: AppConfig,
        logger: Logger,
        playlist_repository: PlaylistRepository,
        inference_respository: InferenceRepository,
        playlist_id_ext: PlaylistIdExtractor,
        song_ext: SongExtractor,
    ) -> None:
        self.config = config
        self.user_logger = logger
        self.playlist_repository = playlist_repository
        self.inference_repository = inference_respository
        self.playlist_id_ext = playlist_id_ext
        self.song_ext = song_ext

    def recommend_music(
        self, user: User, image: UploadFile, data: RecommendMusicRequest
    ) -> RecommendMusicResponse:
        img_path = self._save_query_image(user.id, image)

        playlists, pl_scores = self._extract_playlists(img_path)
        songs = self._extract_songs(data.genres, playlists, pl_scores, top_k)

        songs = [
            RecommendMusic(
                song_id=song.id,
                song_title=song.title,
                artist_name=song.artist.name,
                album_title=song.album.name,
                music_url=song.spotify_url,
            )
            for song in songs
        ]

        self.inference_repository.create_inference(
            user=user,
            query_image_url=img_path,
            query_genres=data.genres,
            output_playlists=playlists,
            output_songs=songs,
        )

        return RecommendMusicResponse(user_id=user.id, songs=songs)

    def _extract_playlists(self, img_path: str) -> tuple[list[Playlist], list[float]]:
        pl_scores, pl_ids = [], []

        weather_scores, weather_ids = self.playlist_id_ext.get_weather_playlist_id(
            img_path
        )
        sit_scores, sit_ids = self.playlist_id_ext.get_mood_playlist_id(img_path)
        mood_scores, mood_ids = self.playlist_id_ext.get_sit_playlist_id(img_path)

        pl_scores.extend(weather_scores)
        pl_scores.extend(sit_scores)
        pl_scores.extend(mood_scores)
        pl_ids.extend(weather_ids)
        pl_ids.extend(sit_ids)
        pl_ids.extend(mood_ids)

        playlists = [self._find_pl_by_genie_id(str(pl_id)) for pl_id in pl_ids]
        return playlists, pl_scores

    def _extract_songs(
        self,
        genres: list[str],
        playlists: list[Playlist],
        pl_scores: list[float],
        top_k: int,
    ) -> list[Song]:
        songs = self.song_ext.extract_songs(playlists, pl_scores, genres)
        return songs[:top_k]

    def _find_pl_by_genie_id(self, genie_id: str):
        found = self.playlist_repository.find_by_genie_id(genie_id)
        if found is None:
            raise NotFoundPlaylistException(
                f"DB에서 genie_id={genie_id}인 playlist를 찾을 수 없습니다!"
            )
        return found

    def _save_query_image(self, user: User, image: UploadFile) -> str:
        os.makedirs(IMG_PATH, exist_ok=True)

        img_path = os.path.join(IMG_PATH, f"{user.id}.jpg")
        with open(img_path, "wb+") as file_object:
            file_object.write(image.file.read())

        self._resize_query_image(img_path)

        return img_path

    def _resize_query_image(self, img_path: str) -> None:
        with Image.open(img_path) as im:
            resized = im.resize((self.config.image_size, self.config.image_size))
            resized.save(img_path)
