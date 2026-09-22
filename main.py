from unicodedata import name

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi.middleware.cors import CORSMiddleware

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

    name: str
    email: str

    # Used for outbound data responses


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


class Config:
    from_attributes = True  # Modern standard replacement for orm_mode = True


# FastAPI instance setup
app = FastAPI()

# Define allowed origins for CORS
origins = [

    "http://localhost:3000",  # React frontend
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # Allows GET, POST, PUT, DELETE
    allow_headers=["*"],   # Allows all standard request headers
)

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
    # if db.query(User).filter(User.id == user.id).first():
       # raise HTTPException(status_code=400, detail="User ID already exists")

    # 3. Correctly aligned block to save user data
    new_db_user = User(name=user.name, email=user.email)
    db.add(new_db_user)
    db.commit()
    db.refresh(new_db_user)
    return new_db_user

# Endpoint to retrieve a user by their ID


@app.get("/users/{user_id}", response_model=list[UserResponse])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Read all users endpoint


@app.get("/users/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Delete user endpoint


@app.delete("/users/{user_id}", response_model=UserResponse)
# look up user in database by ID and delete if found
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = {"name": db_user.name, "email": db_user.email,
                 "id": db_user.id}  # Store user data before deletion
   # if user is found, delete from database and commit changes
    db.delete(db_user)
    db.commit()
    return user_data

# Update user endpoint


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # check if the new email is already taken by another user
    if db.query(User).filter(User.email == user.email, User.id != user_id).first():
        raise HTTPException(
            status_code=400, detail="Email already registered by another user")

    # Update user fields
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user
