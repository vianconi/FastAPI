from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from database import database as connection, User, Movie, UserReview
# Schemas Request
from schemas import (
    UserRequestModel,
    ReviewRequestModel,
    MovieRequestModel,
    ReviewRequestPutModel,
)
# Schemas Response
from schemas import UserResponseModel, ReviewResponseModel, MovieResponseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    if connection.is_closed():
        connection.connect

    print("Coneccion iniciada")

    yield
    if not connection.is_closed():
        connection.close
    print("Connecion apagada")


# 2. Instancia tu aplicación FastAPI con múltiples argumentos
app = FastAPI(
    lifespan=lifespan, # <-- Tu argumento lifespan existente
    title="Mi Increíble API de Reseñas", # <-- Título para la documentación Swagger/Redoc
    description="Una API para gestionar reseñas de películas, usuarios y más.", # <-- Descripción
    version="1.0.0", # <-- Versión de tu API
    debug=True, # <-- Activa el modo debug (útil en desarrollo)
    # docs_url="/documentacion", # <-- Cambia la URL de Swagger UI
    # redoc_url=None, # <-- Deshabilita Redoc si no lo necesitas
    # Puedes añadir aún más argumentos aquí
)


@app.post("/users", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    if User.select().where(User.username == user.username).exists():
        return HTTPException(409, "Username en uso")

    hash_password = User.create_password(user.password)
    user = User.create(username=user.username, password=hash_password)

    return user


@app.post("/movies", response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):
    if Movie.select().where(Movie.title == movie.title).exists():
        raise HTTPException(status_code=409, detail="La pelicula ya existe")

    movie = Movie.create(title=movie.title)

    return movie
    # Opción 2 (más explícita y recomendada):
    # return MovieResponseModel(id=movie.id, title=movie.title)


@app.post("/reviews", response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):
    user_exists = await run_in_threadpool(
        lambda: User.select().where(User.id == user_review.user_id).first()
    )
    if user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    movie_exists = await run_in_threadpool(
        lambda: Movie.select().where(Movie.id == user_review.movie_id).first()
    )
    if movie_exists is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Para la creación también
    created_review = await run_in_threadpool(
        lambda: UserReview.create(
            user_id=user_review.user_id,
            movie_id=user_review.movie_id,
            review=user_review.review,
            score=user_review.score,
        )
    )

    return created_review

    # if User.select().where(User.id == user_review.user_id).first() is None:
    #     raise HTTPException(status_code=404, detail='User not found')

    # if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
    #     raise HTTPException(status_code=404, detail='Movie not found')

    # user_review = UserReview.create(
    #     user_id=user_review.user_id,
    #     movie_id=user_review.movie_id,
    #     review=user_review.review,
    #     score=user_review.score,
    # )

    # return user_review


@app.get("/reviews", response_model=List[ReviewResponseModel])
async def get_reviews():
    reviews = UserReview.select()

    return reviews


@app.get("/reviews/{review_id}", response_model=ReviewResponseModel)
async def get_review(review_id: int):
    user_review = await run_in_threadpool(
        lambda: UserReview.select().where(UserReview.id == review_id).first()
    )

    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    return user_review


@app.put("/reviews/{review_id}", response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    user_review.review = review_request.review
    user_review.score = review_request.score

    user_review.save()

    return user_review
