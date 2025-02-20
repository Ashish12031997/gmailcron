from pydantic import BaseModel


class DeleteEmail(BaseModel):
    email: str
    user_id: int


class DeleteEmailList(BaseModel):
    email: list[DeleteEmail]
