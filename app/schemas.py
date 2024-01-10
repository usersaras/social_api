from pydantic import BaseModel
from typing import List


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True  # default value


class EditPost(CreatePost):
    published: bool


class PostsResponseSchema(BaseModel):
    id: int
    title: str
    content: str
    published: bool


class BaseGetResponse(BaseModel):
    success: bool
    count: int


class GetPostsResponse(BaseGetResponse):
    data: List[PostsResponseSchema]

    class Config:
        orm_mode = True
