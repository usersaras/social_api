from fastapi import APIRouter, Depends, HTTPException, Response, status
import json
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.authentication.oauth2 import get_current_user
from app.schemas import GetPostResponse

from app.models import Like
from .. import models
from ..database import get_db
from ..schemas import CreatePost, EditPost, GetPostsResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get(
    "/",
)
async def get_all_posts(
    db: Session = Depends(get_db), limit: int = 10, offset: int = 0
):
    posts_count = db.query(models.Post).count()

    posts_alchemy = (
        db.query(models.Post, func.count(models.Like.post_id).label("likes"))
        .join(models.Like, models.Like.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .order_by(models.Post.created_at.asc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    return {
        "success": True,
        "count": posts_count,
        "posts": [post._asdict() for post in posts_alchemy],
    }


@router.get("/{id}", response_model=GetPostResponse)  # path parameter
async def get_one_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist!",
        )
    return {"success": True, "data": post}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(
    payload: CreatePost,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),  # authentication
):
    new_post = models.Post(**payload.model_dump(), user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retrieving

    return {
        "success": True,
        "created_post": new_post,
    }


@router.put("/{id}")
async def update_post(
    id: int,
    payload: EditPost,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.one()

        if current_user.id != post.user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to update this post!",
            )
        post_query.update({**payload.model_dump()})
        db.commit()

        return {"message": "Post edited successfully!", "id": id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    try:
        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.one()

        if current_user.id != post.user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to delete this post!",
            )

        post_query.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
