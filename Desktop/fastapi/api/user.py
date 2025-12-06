from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from core.db import get_session
from crud import crud_user
from schema import UserCreate, UserPublic

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    user = await crud_user.get_user_by_username(username=user_data.username, session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"A user with {user_data.username} already exists")
    new_user = await create_user(user_data=user_data, session=session)
    return new_user