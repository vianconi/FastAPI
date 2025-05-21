from pydantic import BaseModel, field_validator, ValidationError


class User(BaseModel):
    username: str
    password: str
    email: str
    age: int

    @field_validator("username")
    def username_validation_lenght(cls, username):
        if len(username) < 3:
            raise ValueError("La longitud minima es de 4 caracteres.")

        if len(username) > 50:
            raise ValueError("La longitud maxima es de 50 caracteres.")

        return username


try:
    user1 = User(username="Cody", password="pass123", email="info@gmail.com", age=10)

    print(user1)
except ValidationError as e:
    print(e.json())
