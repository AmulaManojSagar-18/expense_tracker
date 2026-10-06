from database.models import User

from repositories.expense_repository import (
    create_expense,
    get_all_expenses,
    get_expense_by_id,
    get_expenses_by_user,
    get_expenses_by_user_paginated,
    update_expense,
    delete_expense
)


def create_expense_service(db, expense_data, user_id):

    if expense_data.amount <= 0:
        raise ValueError("Amount must be greater than 0")

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise ValueError("User does not exist")

    return create_expense(db, expense_data, user_id)


def get_all_expenses_service(db):
    return get_all_expenses(db)


def get_expense_service(db, expense_id):

    expense = get_expense_by_id(db, expense_id)

    if not expense:
        raise ValueError("Expense not found")

    return expense


def get_user_expenses_service(db, user_id):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise ValueError("User not found")

    return get_expenses_by_user(db, user_id)


def get_user_expenses_paginated_service(db, user_id, page=1, page_size=10):

    if page < 1:
        raise ValueError("Page must be at least 1")

    if page_size < 1:
        raise ValueError("Page size must be at least 1")

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise ValueError("User not found")

    expenses, total = get_expenses_by_user_paginated(
        db,
        user_id,
        page,
        page_size
    )

    total_pages = (total + page_size - 1) // page_size if total else 0

    return {
        "items": expenses,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def update_expense_service(db, expense_id, expense_data):

    if expense_data.amount <= 0:
        raise ValueError("Amount must be greater than 0")

    expense = update_expense(
        db,
        expense_id,
        expense_data
    )

    if not expense:
        raise ValueError("Expense not found")

    return expense


def delete_expense_service(db, expense_id):

    expense = delete_expense(db, expense_id)

    if not expense:
        raise ValueError("Expense not found")

    return expense