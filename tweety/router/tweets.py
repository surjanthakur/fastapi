from fastapi import APIRouter, HTTPException, status, Depends, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from database.database import get_session
from validation.pydantic_schema import pydantic_tweet, response_tweets
from database.sql_model import Tweet, User
from sqlmodel import select
from typing import List

tweet_router = APIRouter(tags=["tweets"], prefix="/tweets")


# get all tweets
@tweet_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[response_tweets]
)
async def get_all_tweet(db: AsyncSession = Depends(get_session)):
    result = await db.exec(select(Tweet).options(selectinload(Tweet.user)))
    tweets = result.all()
    if not tweets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="db has no tweets right now !!",
        )
    return tweets


# create new tweet for your user
@tweet_router.post("/{user_id}/create", status_code=status.HTTP_201_CREATED)
async def create_new_tweet(
    tweet_data: pydantic_tweet,
    user_id: str = Path(..., description="enter [user_id] to create your own tweets"),
    db: AsyncSession = Depends(get_session),
):
    # fetch all users
    result = await db.exec(select(User).where(User.id == user_id))
    my_user = result.first()
    if not my_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    new_tweet = Tweet(content=tweet_data.content, user_id=user_id)
    db.add(new_tweet)
    await db.commit()
    await db.refresh(new_tweet)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content="👻 tweet created successfully!"
    )


# get tweet by their [id]
@tweet_router.get(
    "/{tweet_id}", status_code=status.HTTP_302_FOUND, response_model=response_tweets
)
async def get_tweet_by_id(tweet_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.exec(
        select(Tweet).options(selectinload(Tweet.user)).where(Tweet.id == tweet_id)
    )
    my_tweet = result.first()
    if not my_tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tweet with id {tweet_id} not found",
        )
    return my_tweet


# update tweet
@tweet_router.put(
    "/{tweet_id}/update", status_code=status.HTTP_200_OK, response_model=pydantic_tweet
)
async def update_tweet(
    tweet_data: pydantic_tweet,
    tweet_id: str,
    db: AsyncSession = Depends(get_session),
):
    result = await db.exec(select(Tweet).where(Tweet.id == tweet_id))
    my_tweet = result.first()
    if not my_tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tweet with id {tweet_id} not found cant update!!",
        )
    updated_dict = tweet_data.model_dump(exclude_unset=True)
    for k, v in updated_dict.items():
        setattr(my_tweet, k, v)
    db.add(my_tweet)
    await db.commit()
    await db.refresh(my_tweet)
    return my_tweet


# delete tweet
@tweet_router.delete("/{tweet_id}/delete")
async def delete_tweet(tweet_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.exec(select(Tweet).where(Tweet.id == tweet_id))
    my_tweet = result.first()
    if not my_tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tweet with id {tweet_id} not found cant delete!!",
        )
    await db.delete(my_tweet)
    await db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"user with {tweet_id} is deleted!!"
    )
