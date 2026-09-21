from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Database configuration and connection
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy model for the User table


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

# Pydantic model for API request and response validation


class UserCreate(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True  # Modern standard replacement for orm_mode = True


# FastAPI instance setup
app = FastAPI()

# Dependency to yield database session per request


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoint to create a new user in the database


@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Check if email already exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Check if the explicit ID already exists to avoid database crash
    if db.query(User).filter(User.id == user.id).first():
        raise HTTPException(status_code=400, detail="User ID already exists")

    # 3. Correctly aligned block to save user data
    new_db_user = User(name=user.name, email=user.email, id=user.id)
    db.add(new_db_user)
    db.commit()
    db.refresh(new_db_user)
    return new_db_user

# Endpoint to retrieve a user by their ID


@app.get("/users/{user_id}", response_model=UserCreate)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
