from sqlalchemy.orm import Session

from database.models import User


def create_user(
    db: Session,
    name: str,
    email: str,
    password_hash: str
):

    user = User(
        name=name,
        email=email,
        password_hash=password_hash
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def get_user_by_email(
    db: Session,
    email: str
):

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_id(
    db: Session,
    user_id: int
):

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_all_users(db: Session):

    return db.query(User).all()