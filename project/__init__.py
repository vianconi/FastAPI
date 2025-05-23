from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from project.routers import movie_router, review_router, user_router
from project.database import database as connection


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

app.include_router(api_v1)
