from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.authentication.oauth2 import generate_access_token
from app.database import get_db
from app.models import User
from app.schema.authenticate import LoginRespone
from app.util.password import verify_hash

router = APIRouter(prefix="/login", tags=["authentication"])


@router.post("/", response_model=LoginRespone)
async def authenticate_user(
    payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == payload.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentails!",
        )

    if not verify_hash(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentails!",
        )

    access_token = generate_access_token({"id": user.id, "email": payload.username})

    return {"success": True, "access_token": f"Bearer {access_token}"}
