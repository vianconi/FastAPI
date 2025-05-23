from fastapi import APIRouter, HTTPException
from project.database import Movie
from project.schemas import MovieRequestModel, MovieResponseModel

router = APIRouter(prefix="/movies")


@router.post("/", response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):
    if Movie.select().where(Movie.title == movie.title).exists():
        raise HTTPException(status_code=409, detail="La pelicula ya existe")

    movie = Movie.create(title=movie.title)

    return movie
