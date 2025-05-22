from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from database import database as connection, User, Movie, UserReview
from schemas import UserRequestModel, ReviewRequestModel, MovieRequestModel
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


app = FastAPI(lifespan=lifespan)


@app.post('/users', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        return HTTPException(409, 'Username en uso')

    hash_password = User.create_password(user.password)
    user = User.create(username=user.username, password=hash_password)

    return user


@app.post('/movies', response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):

    if Movie.select().where(Movie.title == movie.title).exists():
        raise HTTPException(
            status_code=409,
            detail='La pelicula ya existe'
        )
    
    movie = Movie.create(title=movie.title)

    return movie
    # Opción 2 (más explícita y recomendada):
    # return MovieResponseModel(id=movie.id, title=movie.title)
    

@app.post('/reviews', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):
    
    user_review = UserReview.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score
    )

    return user_review
