from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class CreatedUserValue(BaseModel):
    email: EmailStr


class CreatedUserResponse(BaseModel):
    success: bool
    created_user: CreatedUserValue
