from fastapi import APIRouter, HTTPException, Path, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from db.db_connection import get_session
from db.db_tables import Profile, User
from sqlmodel import desc, select
from validation.pydantic_schema import profile_schema, request_profile

profile_router = APIRouter(tags=["profile"], prefix="/profile")


# get all profiles
@profile_router.get("/", status_code=status.HTTP_200_OK, response_model=profile_schema)
async def get_all_profiles(db: AsyncSession = Depends(get_session)):
    try:
        result = await db.exec(select(Profile).options(selectinload(Profile.posts)))
        profiles = result.all()
        if not profiles:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT, detail="profiles not found !!"
            )
        return profiles
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"something went wrong: {err}",
        )


# get profiles by id
@profile_router.get(
    "/{profile_id}", status_code=status.HTTP_200_OK, response_model=profile_schema
)
async def get_profile_by_id(profile_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.exec(
        select(Profile)
        .options(selectinload(Profile.posts))
        .where(Profile.id == profile_id)
    )
    profile = result.first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"profile id: {profile_id} not found !!",
        )
    return profile


# create new profile
@profile_router.post("/create/{user_id}")
async def create_profile(
    profile_data: request_profile,
    user_id: str = Path(..., title="enter your user id"),
    db: AsyncSession = Depends(get_session),
):
    result = await db.exec(select(User).where(User.id == user_id))
    user = result.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user id: {user_id} not found !!",
        )
    new_profile = Profile(user_id=user_id, bio=profile_data.bio)
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=f"profile with id:{new_profile.id} create successfuly!",
    )


# update profile
@profile_router.put("/{profile_id}/update")
async def update_profile(
    profile_id: str = Path(..., title="enter profile id to update bio field"),
    bio: str = Path(title="enter your bio"),
    db: AsyncSession = Depends(get_session),
):
    result = await db.exec(select(Profile).where(Profile.id == profile_id))
    my_profile = result.first()
    if not my_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"profile id: {profile_id} not found !!",
        )
    if len(bio) < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"enter content to update profile!",
        )
    my_profile.bio = bio
    db.add(my_profile)
    await db.commit()
    await db.refresh(my_profile)


# delete profile
@profile_router.delete("/{profile_id}/delete")
async def delete_profile(
    db: AsyncSession = Depends(get_session),
    profile_id: str = Path(..., title="enter profile id"),
):
    result = await db.exec(select(Profile).where(Profile.id == profile_id))
    my_profile = result.first()
    if not my_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"profile id: {profile_id} not found !!",
        )
    await db.delete(my_profile)
    await db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK, content="profile deleted successfuly!"
    )
