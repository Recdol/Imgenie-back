from pydantic import BaseModel


class UserFeedbackRequest(BaseModel):
    song_id: int
    is_like: bool
