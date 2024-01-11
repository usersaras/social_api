from pydantic import BaseModel, EmailStr


class AuthRequest(BaseModel):
    token: str


class JWTPAYLOAD(BaseModel):
    id: int
    email: EmailStr


class LoginRespone(BaseModel):
    success: bool
    access_token: str
