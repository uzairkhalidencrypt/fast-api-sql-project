from sqlalchemy.orm import Session
from app.data.models.user import UserModel
from app.schemas.users import UserCreate


def get_user_by_id(db: Session, user_id: int) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_all_users(db: Session) -> list[UserModel]:
    return db.query(UserModel).all()


def create_user(db: Session, user_data: UserCreate, hashed_pass: str) -> UserModel:
    new_user = UserModel(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pass,
        role=user_data.role,
        department=user_data.department
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user_fields(db: Session, db_user: UserModel, update_data: UserCreate) -> UserModel:
    db_user.name = update_data.name
    db_user.email = update_data.email
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_record(db: Session, db_user: UserModel):
    db.delete(db_user)
    db.commit()

# Fetch data for get/users/count endpoint


# db:Session tells the function to accept the active database connection
def get_user_count(db: Session) -> int:
    # db.query(UserModel) tells sqlAlchemy to look at user table and count() is built in helper that translates directly to the SQL command: SELECT COUNT(*) FROM users
    return db.query(UserModel).count()
    # ->int means the function give back a plain number
