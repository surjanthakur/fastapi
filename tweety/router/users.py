from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlalchemy.orm import selectinload
from database.database import get_session
from sqlmodel import select
from database.sql_model import User
from validation.pydantic_schema import pydantic_user, response_user
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(tags=["users"], prefix="/users")


# get user by their id
@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=response_user)
async def get_user_by_id(
    user_id: str = Path(
        ...,
        title="enter user_id",
        description="enter the user id to access information !!",
    ),
    db: AsyncSession = Depends(get_session),
):
    result = await db.exec(
        select(User).options(selectinload(User.tweets)).where(User.id == user_id)
    )
    user = result.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invalid user_id enter the valid user id !!",
        )
    return user


# create new user
@router.post("/create")
async def create_users(
    user_data: pydantic_user,
    db: AsyncSession = Depends(get_session),
):
    new_user = User(name=user_data.name, email=user_data.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=f"user: {new_user.email} created successfullt !!",
    )


# update user by id
@router.put("/{user_id}/update")
async def update_user_by_id(
    update_data: pydantic_user,
    user_id: str = Path(
        ...,
        title="enter user_id",
        description="enter the user id to update information !!",
    ),
    db: AsyncSession = Depends(get_session),
):
    result = await db.exec(select(User).where(User.id == user_id))
    user = result.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invalid user_id enter the valid user id !!",
        )
    updated_dict = update_data.model_dump(exclude_unset=True)
    for key, value in updated_dict.items():
        setattr(user, key, value)
    user.updated_at = datetime.now()
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=f"user: {user_id} updated successfully !!",
    )


# delete user by id
@router.delete("/{user_id}/delete")
async def delete_user_by_id(
    user_id: str = Path(..., description="enter the user id to update information !!"),
    db: AsyncSession = Depends(get_session),
):
    result = await db.exec(select(User).where(User.id == user_id))
    user = result.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invalid user_id enter the valid user id !!",
        )
    await db.delete(user)
    await db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=f"user: {user_id} deleted successfully !!",
    )
