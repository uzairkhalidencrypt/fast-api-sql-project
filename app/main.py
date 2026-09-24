from fastapi import FastAPI
from app.data.database import init_db
from app.api.v1 import users

app = FastAPI(title="FastAPI Enterprise Project")

# Automatically spin up database tables when starting


@app.on_event("startup")
def on_startup():
    init_db()


# Include your user management router paths
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"status": "Server running smoothly!"}
