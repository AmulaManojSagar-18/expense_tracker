from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.user_schema import UserCreate, UserResponse

from services.user_service import (
    create_user_service,
    get_all_users_service,
    get_user_service
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_user_service(db, user)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    return get_all_users_service(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        return get_user_service(db, user_id)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )