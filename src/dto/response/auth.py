from pydantic import BaseModel


class NewUserResponse(BaseModel):
    user_id: str
