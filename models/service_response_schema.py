from pydantic import BaseModel


class UserResponse(BaseModel):
    body: str
    status_code: str
