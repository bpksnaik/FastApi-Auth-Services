from pydantic import BaseModel


class UserResponse(BaseModel):
    body: str
    status_code: str


class Movie(BaseModel):
    title: str
    genres: str
    overview: str
    runtime: str
    spoken_languages: str


class RecommendationResponse(BaseModel):
    result: list[Movie]
    source: str
