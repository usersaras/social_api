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


class PostsResponseSchema(BaseModel):
    Post: PostResponseSchema
    likes: int


class BaseGetListResponse(BaseModel):
    success: bool
    count: int


class BaseGetDictResponse(BaseModel):
    success: bool


class GetPostsResponse(BaseGetListResponse):
    data: PostsResponseSchema

    class Config:
        orm_mode = True


class GetPostResponse(BaseGetDictResponse):
    posts: List[PostResponseSchema]
    count: int

    class Config:
        orm_mode = True


class LikeRequest(BaseModel):
    post_id: int
    is_like: bool
