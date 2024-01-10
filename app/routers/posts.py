from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter

from ..schemas import CreatePost, EditPost, GetPostsResponse
from .. import models
from ..database import get_db

router = APIRouter()


@router.get("/posts", response_model=GetPostsResponse)
async def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    posts_count = db.query(models.Post).count()
    return {"success": True, "data": posts, "count": posts_count}


@router.get("/posts/{id}")  # path parameter
async def get_one_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return {"data": post}


@router.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_postPostsResponseSchema(
    payload: CreatePost, db: Session = Depends(get_db)
):
    new_post = models.Post(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retrieving

    return {
        "success": True,
        "created_post": new_post,
    }


@router.put("/posts/{id}")
async def update_post(id: int, payload: EditPost, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id)
        post.one()
        post.update({**payload.model_dump()})
        db.commit()

        return {"message": "Post edited successfully!", "id": id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id)
        post.one()
        post.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))