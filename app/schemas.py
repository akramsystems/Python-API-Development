"""
Pydantic Models are used as Schema Validation
for request and responses parameters
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr  # from pydantic
    created_at: datetime

    class Config():
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int  # will let the logic retrieve id from token
    owner: UserResponse  # return pydantic model type

    # in order to use as response_model
    # otherwise will receive error
    class Config():
        orm_mode = True  # convert sql model to pydantic model


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config():
        orm_mode = True
