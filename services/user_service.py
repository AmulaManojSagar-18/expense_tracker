from database.models import User

from repositories.user_repository import (
    create_user,
    get_all_users,
    get_user_by_id
)


def create_user_service(db, user_data):

    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise ValueError("Email already exists")

    return create_user(db, user_data)


def get_all_users_service(db):
    return get_all_users(db)


def get_user_service(db, user_id):

    user = get_user_by_id(db, user_id)

    if not user:
        raise ValueError("User not found")

    return user