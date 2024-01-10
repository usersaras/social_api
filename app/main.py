from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True  # default value


class EditPost(BaseModel):
    title: str
    content: str
    published: bool


@app.get("/posts")
async def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    posts_count = db.query(models.Post).count()
    return {"success": True, "data": posts, "count": posts_count}


@app.get("/posts/{id}")  # path parameter
async def get_one_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(payload: CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retrieving

    return {
        "success": True,
        "created_post": new_post,
    }


@app.put("/posts/{id}")
async def update_post(id: int, payload: EditPost, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id)
        post.one()
        post.update({**payload.model_dump()})
        db.commit()

        return {"message": "Post edited successfully!", "id": id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id)
        post.one()
        post.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
