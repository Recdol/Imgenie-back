from pydantic import BaseModel


class UserFeedbackRequest(BaseModel):
    song_id: str
    inference_id: str
    is_like: bool
