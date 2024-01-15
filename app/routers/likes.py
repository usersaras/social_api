from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from app.schemas import LikeRequest
from app.models import Like
from app.authentication.oauth2 import get_current_user
from app.database import get_db

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/")
def like_post(
    payload: LikeRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    post_id, is_like = payload.model_dump().values()
    if not is_like:
        like_query = db.query(Like).filter(
            Like.post_id == post_id and Like.user_id == current_user.id
        )
        if not like_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, message="User has not liked post"
            )
        like_query.delete()
        db.commit()
        return {
            "success": True,
            "like": f"Unliked post with id {post_id}",
        }
    try:
        new_like = Like(post_id=post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"This post has already been liked by user with id {current_user.id}",
        )

    return {
        "success": True,
        "like": f"Liked post with id {post_id}",
    }
