from typing import List

from pydantic import BaseModel, EmailStr


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True  # default value


class EditPost(CreatePost):
    published: bool


class User(BaseModel):
    id: int
    email: EmailStr


class PostResponseSchema(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    user: User


class BaseGetListResponse(BaseModel):
    success: bool
    count: int


class BaseGetDictResponse(BaseModel):
    success: bool


class GetPostsResponse(BaseGetListResponse):
    data: List[PostResponseSchema]

    class Config:
        orm_mode = True


class GetPostResponse(BaseGetDictResponse):
    data: PostResponseSchema

    class Config:
        orm_mode = True
