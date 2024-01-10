from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from app.schema.user import CreatedUserResponse, CreateUser
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .util.password import hash
from .routers import posts, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
