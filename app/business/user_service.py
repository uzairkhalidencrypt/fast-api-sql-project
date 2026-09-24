from sqlalchemy.orm import Session
from app.data.repository import user_repo
from app.schemas.users import UserCreate


def create_new_user(db: Session, user: UserCreate):
    return user_repo.create_user(db, user)


def get_user(db: Session, user_id: int):
    return user_repo.get_user_by_id(db, user_id)


def get_total_users(db: Session) -> int:
    return user_repo.get_user_count(db)
