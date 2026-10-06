from auth.dependencies import get_current_user
from database.models import User
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.connection import get_db

from schemas.expense_schema import (
    ExpenseCreate,
    ExpenseResponse
)

from services.expense_service import (
    create_expense_service,
    get_all_expenses_service,
    get_expense_service,
    get_user_expenses_paginated_service,
    get_user_expenses_service,
    update_expense_service,
    delete_expense_service
)


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.post("/")
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try:

        return create_expense_service(
            db,
            expense,
            current_user.id
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.get("/")
def get_expenses(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try:
        return get_user_expenses_paginated_service(
            db,
            current_user.id,
            page=page,
            page_size=page_size
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get("/{expense_id}")
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    expense = get_expense_service(
        db,
        expense_id
    )

    if expense.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="You cannot access this expense"
        )

    return expense

@router.get(
    "/user/{user_id}",
    response_model=list[ExpenseResponse]
)
def get_user_expenses(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        return get_user_expenses_service(db, user_id)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.put("/{expense_id}")
def update_expense(
    expense_id: int,
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    existing_expense = get_expense_service(
        db,
        expense_id
    )

    if existing_expense.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="You cannot modify this expense"
        )

    updated = update_expense_service(
        db,
        expense_id,
        expense
    )

    return updated

@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    expense = get_expense_service(
        db,
        expense_id
    )

    if expense.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="You cannot delete this expense"
        )

    delete_expense_service(
        db,
        expense_id
    )

    return {
        "message": "Expense deleted successfully"
    }