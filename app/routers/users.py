from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from app.schema.user import CreatedUserResponse, CreateUser
from .. import models
from ..database import get_db
from ..util.password import hash

router = APIRouter(prefix="/user", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CreatedUserResponse
)
def create_user(payload: CreateUser, db: Session = Depends(get_db)):
    payload_dict = payload.model_dump()

    hashed_password_payload = {
        **payload_dict,
        "password": hash(payload.password),
    }

    try:
        user = models.User(**hashed_password_payload)
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Duplicate Entry! User with email '{payload.email}' already exists!",
        )

    return {"success": True, "created_user": user}
