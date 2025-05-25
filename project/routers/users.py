from http import HTTPStatus
from typing import List
from fastapi import Depends, HTTPException, APIRouter, Response
from fastapi.security import HTTPBasicCredentials 
from project.database import User
from project.schemas import (
    ReviewResponseModel, UserRequestModel, UserResponseModel
)
from project.common import oauth2_schema, get_current_user

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    if User.select().where(User.username == user.username).exists():
        return HTTPException(409, "Username en uso")

    hash_password = User.create_password(user.password)

    user = User.create(username=user.username, password=hash_password)

    return user


@router.post("/login", response_model=UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username == credentials.username).first()

    if user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    if user.password != User.create_password(credentials.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid credentials"
        )

    response.set_cookie(key="user_id", value=user.id)
    return user


@router.get('/reviews', response_model=List[ReviewResponseModel])
async def get_review(user: User = Depends(get_current_user)):
    
    return [ user_review for user_review in user.reviews ]
