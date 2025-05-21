from pydantic import BaseModel, field_validator


class UserRequestModel(BaseModel):
    username: str
    password: str

    @field_validator("username")
    def username_validator(cls, username):
        if len(username) < 4 or len(username) > 50:
            raise ValueError("La longitud minima es 4, y la maxima 50")

        return username
    

class UserResponseModel(BaseModel):
    id: int
    username: str
