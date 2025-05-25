from contextlib import asynccontextmanager
from http.client import HTTPException

from fastapi import APIRouter, Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from project.routers import movie_router, review_router, user_router
from project.database import User, database as connection
from project.common import create_access_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    if connection.is_closed():
        connection.connect
    yield
    if not connection.is_closed():
        connection.close


app = FastAPI(
    lifespan=lifespan,
    title="Mi Increíble API de Reseñas",
    description="Una API para gestionar reseñas de películas, usuarios y más.",
    version="1.0.0",
    debug=True,
)

api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(user_router)
api_v1.include_router(movie_router)
api_v1.include_router(review_router)


@api_v1.post("/auth")
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(data.username, data.password)

    if user:
        return {
            'access_token': create_access_token(user),
            'token_type': 'Bearer'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username o Password incorrectos",
            headers={"WWW-Autenticate": "Beraer"},
        )


app.include_router(api_v1)
