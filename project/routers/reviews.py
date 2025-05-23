from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from project.database import Movie, User, UserReview
from project.schemas import (
    ReviewRequestModel,
    ReviewRequestPutModel,
    ReviewResponseModel,
)

router = APIRouter(prefix="/reviews")


@router.post("/", response_model=ReviewResponseModel)
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

    created_review = await run_in_threadpool(
        lambda: UserReview.create(
            user_id=user_review.user_id,
            movie_id=user_review.movie_id,
            review=user_review.review,
            score=user_review.score,
        )
    )

    return created_review


@router.get("/", response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10):
    reviews = UserReview.select().paginate(page, limit)

    return [user_review for user_review in reviews]


@router.get("/{review_id}", response_model=ReviewResponseModel)
async def get_review(review_id: int):
    user_review = await run_in_threadpool(
        lambda: UserReview.select().where(UserReview.id == review_id).first()
    )

    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    return user_review


@router.put("/{review_id}", response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    user_review.review = review_request.review
    user_review.score = review_request.score

    user_review.save()

    return user_review


@router.delete("/{review_id}", response_model=ReviewResponseModel)
async def delete_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    user_review.delete_instance()

    return user_review
