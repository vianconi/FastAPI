from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from database import database as connection, User, Movie, UserReview
from schemas import UserRequestModel, UserResponseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta al iniciar
    if connection.is_closed():
        connection.connect

    connection.create_tables([User, Movie, UserReview])
    print("Coneccion iniciada")

    yield
    # Código que se ejecuta al apagar
    if not connection.is_closed():
        connection.close
    print("Connecion apagada")


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def index():
    return 'Hello world!'


@app.post('/users', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        return HTTPException(409, 'Username en uso')

    hash_password = User.create_password(user.password)
    user = User.create(username=user.username, password=hash_password)

    return UserResponseModel(id=user.id, username=user.username)
