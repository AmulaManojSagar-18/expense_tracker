from sqlalchemy.orm import Session
from database.models import Expense


def create_expense(db: Session, expense_data, user_id: int):
    expense = Expense(
        title=expense_data.title,
        amount=expense_data.amount,
        category=expense_data.category,
        user_id=user_id
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


def get_all_expenses(db: Session):
    return db.query(Expense).all()


def get_expense_by_id(db: Session, expense_id: int):
    return (
        db.query(Expense)
        .filter(Expense.id == expense_id)
        .first()
    )


def get_expenses_by_user(db: Session, user_id: int):
    return (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .all()
    )


def get_expenses_by_user_paginated(db: Session, user_id: int, page: int, page_size: int):
    query = (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .order_by(Expense.id)
    )

    total = query.count()
    expenses = query.offset((page - 1) * page_size).limit(page_size).all()

    return expenses, total


def update_expense(db: Session, expense_id: int, expense_data):
    expense = get_expense_by_id(db, expense_id)

    if expense:
        expense.title = expense_data.title
        expense.amount = expense_data.amount
        expense.category = expense_data.category

        db.commit()
        db.refresh(expense)

    return expense


def delete_expense(db: Session, expense_id: int):
    expense = get_expense_by_id(db, expense_id)

    if expense:
        db.delete(expense)
        db.commit()

    return expense