from datetime import datetime
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel,EmailStr, Field
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class userOut(BaseModel):
    id: int
    email: EmailStr
    created_at:datetime
    class Config:
        #orm_mode
        from_attributes = True

class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:userOut
    class Config:
        #orm_mode
        from_attributes = True

class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserLogin(BaseModel):
    email :EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]