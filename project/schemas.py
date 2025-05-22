from typing import Any
from pydantic import BaseModel, Field, field_validator


def custom_getter(obj: Any, field: str) -> Any:
    return getattr(obj, field, None)


class ResponseModel(BaseModel):
    model_config = {"from_attributes": True}


class ReviewValidator:
    score: int = Field(
        ..., ge=1, le=5, description="Calificación de la película (1 a 5)."
    )


class UserRequestModel(BaseModel):
    username: str
    password: str

    @field_validator("username")
    def username_validator(cls, username):
        if len(username) < 4 or len(username) > 50:
            raise ValueError("La longitud minima es 4, y la maxima 50")

        return username


class UserResponseModel(ResponseModel):
    id: int
    username: str


class MovieRequestModel(BaseModel):
    title: str

    @field_validator("title")
    def title_validator(cls, title):
        if len(title) < 1:
            raise ValueError("El título no puede estar vacío")
        if len(title) > 200:
            raise ValueError("El título es demasiado largo")
        return title


class MovieResponseModel(ResponseModel):
    id: int
    title: str


class ReviewRequestModel(BaseModel, ReviewValidator):
    user_id: int
    movie_id: int
    review: str
    score: int


class ReviewResponseModel(ResponseModel):
    id: int
    movie_id: int
    review: str
    score: int


class ReviewRequestPutModel(BaseModel, ReviewValidator):
    review: str
    score: int
