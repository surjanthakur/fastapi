from sqlmodel import select
from fastapi import APIRouter, HTTPException, Path, Depends, status
from fastapi.responses import JSONResponse
from db.db_connection import get_session
from validation.pydantic_schema import user_schema 
from sqlmodel.ext.asyncio.session import AsyncSession
from db.db_tables import User

user_router = APIRouter(prefix="/users", tags=["user"])


# create new user ---------------------->
@user_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=user_schema,
)
async def create_new_user(
    user_data: user_schema,
    db: AsyncSession = Depends(get_session),
):
    try:
        new_user = User(**user_data.model_dump())
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as err:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {err} !!",
        )


# get user by id ------------------>
@user_router.get(
    "/{user_id}", status_code=status.HTTP_302_FOUND, response_model=user_schema
)
async def get_user_by_id(
    user_id: str = Path(
        ..., description="add user id to see you user and their profiles"
    ),
    db: AsyncSession = Depends(get_session),
):
    try:
        result = await db.exec(select(User).where(User.id == user_id))
        user = result.first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"cant find user with : {user_id} enter a valid id 📍",
            )
        return user
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"something went wrong: {err}",
        )


# update user by id --------------->
@user_router.put("/{user_id}/update")
async def update_user(
    update_data: user_schema,
    user_id: str = Path(
        ..., description="add user id to see you user and their profiles"
    ),
    db: AsyncSession = Depends(get_session),
):
    result = await db.exec(select(User).where(User.id == user_id))
    my_user = result.first()
    if not my_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"cant find user with : {user_id} enter a valid id 📍",
        )
    updated_dic = update_data.model_dump(exclude_unset=True)
    for k, v in updated_dic.items():
        setattr(my_user, k, v)
    try:
        db.add(my_user)
        await db.commit()
        await db.refresh(my_user)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=f"user: {user_id} updated successfully",
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"something went wrong: {err}",
        )


# delete user ----------------->
@user_router.delete("/{user_id}/delete")
async def delete_user(
    user_id: str = Path(
        ..., description="add user id to see you user and their profiles"
    ),
    db: AsyncSession = Depends(get_session),
):
    result = await db.exec(select(User).where(User.id == user_id))
    my_user = result.first()
    if not my_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"cant find user with : {user_id} enter a valid id 📍",
        )
    try:
        await db.delete(my_user)
        await db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=f"user {user_id} deleted successfully!!",
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"something went wrong: {err}",
        )
